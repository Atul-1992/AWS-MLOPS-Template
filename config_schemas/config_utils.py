from pydantic.dataclasses import dataclass
from hydra.core.config_store import ConfigStore
from hydra import TaskFunction
import hydra
from omegaconf import MISSING, DictConfig, OmegaConf
from typing import List, Optional, Any, Dict

@dataclass
class CidrIpConfig:
	CidrIp:str = '0.0.0.0/0'

@dataclass
class IngressConfig:
	IpRanges:List[CidrIpConfig]
	IpProtocol: str = 'tcp'
	FromPort: int = 80
	ToPort: int = 80

@dataclass
class UserdataConfig:
	script: str = '''#!/bin/bash
						yum update -y
						yum install -y httpd
						systemctl start httpd
						systemctl enable httpd
						echo "<html><body><h1>Welcome to My Website</h1></body></html>" > /var/www/html/index.html'''


@dataclass
class Ec2Config:
	ingress_rules: IngressConfig
	userdata_script: UserdataConfig
	image_id: str = 'ami-001843b876406202a'
	instance_type:str = 't2.micro'


@dataclass
class EcrConfig:
	repository_name: str = 'sample_repo_1'

@dataclass
class S3Config:
	storage_url:Optional[str]

@dataclass
class AwsConfig:
	ecr: EcrConfig
	ec2: Ec2Config
	s3: S3Config

@dataclass
class DockerConfig:
	docker_folder:str = 'docker_dir'
	dockerfile_name:str = 'Dockerfile'
	image_name:str = 'demo_image'
	tag:str = 'v01'

@dataclass
class DvcConfig:
	dvc_remote_url:Optional[str]
	dvc_remote_name:str = 'gdrive'
	local_data_dir:str = 'data_dir'

@dataclass
class GitConfig:
	git_remote_name:str = 'origin'
	git_remote_url:str = "git@github.com:Atulsain7/AWS-MLOPS-Template.git"
	current_git_branch:str = 'main'

@dataclass
class Config:
	aws: AwsConfig
	git: GitConfig
	dvc: DvcConfig
	docker: DockerConfig

def setup_config_schemas():
	cs = ConfigStore.instance()
	cs.store(name="config_schema_node", node=Config)
	cs.store(group="aws", name="ec2", node=Ec2Config)
	cs.store(group="aws", name="ecr", node=EcrConfig)
	cs.store(group="aws", name="s3", node=S3Config)
	cs.store(group="docker", name="docker", node=DockerConfig)
	cs.store(group="dvc", name="dvc", node=DvcConfig)
	cs.store(group="git", name="git", node=GitConfig)
	cs.store(group="ec2", name="ingress_rules", node=IngressConfig)
	cs.store(group='ec2', name='userdata_script', node=UserdataConfig)


def config_schema_decorator(config_path, config_name)->TaskFunction:
	setup_config_schemas()

	def main_decorator(task_function)->Any:

		@hydra.main(config_name=config_name, config_path=config_path, version_base=None)
		def decorated_main(dict_config: Optional[DictConfig]):
			config = OmegaConf.to_object(dict_config)
			return task_function(config)
		
		return decorated_main
	return main_decorator
