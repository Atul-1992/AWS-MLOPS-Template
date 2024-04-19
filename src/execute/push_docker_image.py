import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

sys.path.append(project_root)
from src.execute.ActSetup import processes

dockerfile_name = 'Dockerfile'
image_name = 'demo_image'
tag = 'v01'
repository_name = 'sample_repo_1'


if __name__=='__main__':
	processes.push_on_ecr(dockerfile_name=dockerfile_name, 
					   image_name=image_name, 
					   tag=tag, 
					   repository_name=repository_name)