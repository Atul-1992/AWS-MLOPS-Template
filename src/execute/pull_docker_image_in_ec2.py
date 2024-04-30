import os
import sys
import hydra
from omegaconf import DictConfig, OmegaConf

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
print(project_root)
sys.path.append(project_root)
from src.CloudUtils.ec2 import EC2Helper


@hydra.main(config_name="config", config_path="../../configs", version_base=None)
def main(cfg: DictConfig):
    helper = EC2Helper(os.getcwd())
    print(cfg['aws']['ec2']['username'])
    helper.command_instance_with_ssh(instance_name=cfg['aws']['ec2']['instance_name'], 
                                            # private_key_path=cfg['aws']['ec2']['private_key_path'], 
                                            private_key_path=os.path.join(os.getcwd(), "".join([cfg['aws']['ec2']['key_pair'], ".pem"])),
                                            port=cfg['aws']['ec2']['ingress_rules']['ToPort'], 
                                            username=cfg['aws']['ec2']['username'], 
                                            command="echo 'HEllo SSH'")
    print("Command run")
    
if __name__=="__main__":
    main()
    