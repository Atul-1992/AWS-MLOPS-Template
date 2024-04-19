import os
import sys
from src.processes.combine import GeneralProcess

# Add project directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


sys.path.append(project_root)

processes = GeneralProcess(local_data_dir='data_dir', 
						   dvc_remote_name='gdrive', 
						   dvc_remote_url='https://drive.google.com/drive/folders/1YQKvAM4mhU688OBwIDJYfuz2SOAZqk8c?usp=sharing', 
						   git_remote_name='origin', 
						   git_remote_url="git@github.com:Atulsain7/AWS-MLOPS-Template.git", 
						   current_git_branch='main', 
						   docker_folder='docker_dir', 
						   s3_bucket_path=None)