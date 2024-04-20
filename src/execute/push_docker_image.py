import os
import sys
import hydra
from omegaconf import DictConfig

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from src.processes.setup_process import setup_general_process


@hydra.main(config_name='config', config_path='../../configs', version_base=None)
def main(cfg: DictConfig) -> None:
	processes = setup_general_process(cfg)
	processes.push_on_ecr(dockerfile_name=cfg['docker']['dockerfile_name'], 
					   image_name=cfg['docker']['image_name'], 
					   tag=cfg['docker']['tag'], 
					   repository_name=cfg['aws']['ecr']['repository_name'])
	


if __name__=='__main__':
	main()