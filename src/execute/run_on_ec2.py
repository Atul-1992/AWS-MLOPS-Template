# ./src/execute/run_on_ec2.py
import os
import sys
import hydra
from omegaconf import DictConfig

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

sys.path.append(project_root)
from src.processes.setup_process import setup_general_process

@hydra.main(config_name='config', config_path='../../configs', version_base=None)
def main(cfg: DictConfig)-> None:
	processes = setup_general_process(cfg)
	processes.create_instance(image_id=cfg['aws']['ec2']['image_id'], 
						   instance_name=cfg['aws']['ec2']['instance_name'],
						   instance_type=cfg['aws']['ec2']['instance_type'],
						   group_name=cfg['aws']['ec2']['group_name'],
						   key_pair=cfg['aws']['ec2']['key_pair'],
						   ingress_rules=cfg['aws']['ec2']['ingress_rules'], 
						   userdata_script=cfg['aws']['ec2']['userdata_script']['script'])


if __name__=='__main__':
	main()