# ./src/processes/setup_process.py
import os

from CloudUtils.ec2 import EC2Helper
from CloudUtils.ecr import ECRHelper
from CloudUtils.iam import IAMHelper
from CloudUtils.login import AWSCredentialManager
from CloudUtils.s3 import S3Helper
from container.docker_container import DockerHelper
from versionControlUtils.dvc import DVCHelper
from versionControlUtils.git import GitHelper


class AWSSetup:
    def __init__(self, docker_folder="docker_dir") -> None:
        self.project_dir = os.getcwd()
        session = AWSCredentialManager().get_aws_session()
        self.ec2_helper = EC2Helper(session)
        self.s3_helper = S3Helper(session)
        self.ecr_helper = ECRHelper(session)
        self.iam_helper = IAMHelper(session)
        self.container_helper = DockerHelper(docker_folder)

    def push_on_ecr(self, dockerfile_name, image_name, tag, repository_name=None):
        self.container_helper.build_image(dockerfile_name, image_name, tag)
        self.ecr_helper.create_repository(repository_name)
        self.ecr_helper.push_image(image_name, tag)
        return True

    def create_instance(
        self,
        instance_name,
        group_name,
        key_pair,
        image_id,
        instance_type,
        role_name,
        assume_role_policy_document,
        policy_names,
        instance_profile_name,
        ingress_rules,
        userdata_script,
        environment_variables=None,
    ):
        group_id1 = self.ec2_helper.create_security_group(
            group_name=group_name,
            description="This group is created in aws template with boto3",
            ingress_rules=ingress_rules,
        )
        key_name = self.ec2_helper.check_or_create_key_pair(key_pair_name=key_pair)
        self.iam_helper.create_or_get_role(
            role_name,
            assume_role_policy_document=assume_role_policy_document,
            policy_names=policy_names,
        )
        self.iam_helper.create_instance_profile(instance_profile_name)
        instance_profile_arn = self.iam_helper.add_roles_to_instance_profile(
            instance_profile_name=instance_profile_name, role_names=[role_name]
        )
        self.ec2_helper.create_or_start_ec2_instance_with_userdata(
            instance_name=instance_name,
            image_id=image_id,
            instance_type=instance_type,
            key_name=key_name,
            userdata_script=userdata_script,
            security_group_ids=[group_id1],
            instance_profile_arn=instance_profile_arn,
            environment_variables=environment_variables,
        )

    def stop_all_instances(self):
        self.ec2_helper.stop_all_running_instances()


class VersionControlSetup:
    def __init__(
        self,
        current_branch,
        remote_name,
        remote_url,
        local_data_dir,
        data_remote_name,
        data_remote_repo,
    ) -> None:
        self.repo_dir = os.getcwd()
        self.branch = current_branch
        self.remote_name = remote_name
        self.remote_url = remote_url
        self.git_helper = GitHelper(
            repo_dir=self.repo_dir,
            branch=self.branch,
            remote_name=self.remote_name,
            remote_url=self.remote_url,
        )
        self.local_data_dir = local_data_dir
        self.data_remote_name = data_remote_name
        self.data_remote_repo = data_remote_repo
        self.dvc_helper = DVCHelper(
            self.repo_dir,
            data_dir=self.local_data_dir,
            remote_name=self.data_remote_name,
            remote_url=self.data_remote_repo,
        )

    def initialize_project(self):
        self.git_helper.init()
        self.dvc_helper.init()
        self.dvc_helper.add_remote()
        self.git_helper.add_to_gitignore(f"/{self.local_data_dir}")
        self.git_helper.add_to_gitignore("/env_files")
        self.git_helper.add(["."])
        # self.git_helper.add(['.dvc', 'data_dir.dvc'])
        self.git_helper.commit(f"Initialized with code version: {self.version_code}")
        self.git_helper.version_code()
        self.git_helper.create_remote()
        self.dvc_helper.push()
        self.git_helper.push()
        return True

    def version_dataset(self):
        if self.dvc_helper.needs_update():
            self.dvc_helper.import_data()
            self.git_helper.add([f"{self.local_data_dir}.dvc"])
            tag = self.git_helper.version_code("d")
            self.git_helper.commit(f"Dataset Updated with Dataset Version: {tag}")
            self.git_helper.push()
            return True
        return False

    def version_code(self, message=""):
        if self.git_helper.needs_commit(["./src/", "./configs/"]):
            self.git_helper.add(["."])
            self.git_helper.commit(message)
            self.git_helper.version_code()
            self.git_helper.push()
            return True
        print("There is no change in `src` or `configs` folder to commit!")
        return False


def setup_aws(worker):
    return AWSSetup(docker_folder=worker.docker.docker_dir)


def setup_version_control(cfg):
    return VersionControlSetup(
        cfg.version_control.git.git_branch,
        cfg.version_control.git.git_remote_name,
        cfg.version_control.git.git_repo_url,
        cfg.version_control.dvc.local_data_dir,
        cfg.version_control.dvc.data_remote_name,
        cfg.version_control.dvc.data_remote_repo_url,
    )
