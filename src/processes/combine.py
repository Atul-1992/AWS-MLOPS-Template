from src.CloudUtils.ec2 import EC2Helper
from src.CloudUtils.ecr import ECRHelper
# from src.CloudUtils.aws_config import AWSConfig
from src.CloudUtils.s3 import S3Helper
from src.container.docker_container import DockerHelper
from src.VersionControlUtils.dvc import DVCHelper
from src.VersionControlUtils.git import GitHelper
import os

class GeneralProcess:
	def __init__(self, 
			  local_data_dir, 
			  dvc_remote_name, 
			  dvc_remote_url, 
			  git_remote_name, 
			  git_remote_url, 
			  current_git_branch='main',
			  docker_folder='docker', 
			  s3_bucket_path= None) -> None:
		
		self.code_version = 0
		self.dataset_version = 0
		self.s3_bucket_path = s3_bucket_path
		self.data_dir = local_data_dir

		self.project_dir = os.getcwd()
		self.git_helper = GitHelper(repo_dir=self.project_dir, branch=current_git_branch, remote_name=git_remote_name, remote_url=git_remote_url)
		self.dvc_helper = DVCHelper(self.project_dir, data_dir=local_data_dir, remote_name=dvc_remote_name, remote_url=dvc_remote_url)
		self.ec2_helper = EC2Helper(self.project_dir)
		self.s3_helper = S3Helper(self.project_dir)
		self.ecr_helper = ECRHelper(self.project_dir)
		self.container_helper = DockerHelper(self.project_dir, docker_folder)

	def initialize_project(self):
		self.git_helper.init()
		self.dvc_helper.init()
		self.git_helper.add_to_gitignore(f'/{self.data_dir}')
		self.git_helper.add_to_gitignore('/env_files')
		self.git_helper.add(['.'])
		# self.git_helper.add(['.dvc', 'data_dir.dvc'])
		self.git_helper.commit(f'Initialized with code version: {self.code_version}')
		self.git_helper.version_code()
		self.git_helper.create_remote()
		self.dvc_helper.push()
		self.git_helper.push()
		return True

	def version_dataset(self):
		tags = {"Dataset Version": self.dataset_version}
		if self.dvc_helper.needs_update():
			self.dvc_helper.pull()
			self.git_helper.add(".dvc/*")
			self.git_helper.commit()
			self.git_helper.tag(tags)
			self.git_helper.push()
			self.dataset_version += 1
			return True
		return False

	def version_code(self):
		if self.git_helper.needs_commit():
			self.git_helper.add(["./src/"])
			self.git_helper.commit("Code updated with {}".format(self.code_version))
			self.git_helper.version_code()
			self.git_helper.push()
			return True
		return False

	def push_on_ecr(self, dockerfile_name, image_name, tag, repository_name=None):
		self.container_helper.build_image(dockerfile_name, image_name, tag)
		self.ecr_helper.create_repository(repository_name)
		self.ecr_helper.push_image(image_name, tag)
		return True

	def create_instance(self, image_id, instance_type, ingress_rules, userdata_script):
		group_id1 = self.ec2_helper.create_security_group(group_name="aws_template_1", description='This group is created in aws template with boto3', ingress_rules=ingress_rules)
		key_name = self.ec2_helper.check_or_create_key_pair('aws_template_key')
		self.ec2_helper.create_or_start_ec2_instance_with_userdata(instance_name='Instance_1', image_id=image_id, instance_type=instance_type, key_name=key_name, userdata_script=userdata_script, security_group_ids=[group_id1])

	def stop_all_instances(self):
		self.ec2_helper.stop_all_running_instances()
