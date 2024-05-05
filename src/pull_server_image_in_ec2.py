# ./src/execute/pull_server_image_in_ec2.py
from omegaconf import DictConfig

from processes.setup_process import setup_aws
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig):
    aws = setup_aws(cfg['server'])
    aws.ec2_helper.command_instance_with_ssh(
        instance_name=cfg['server']['aws']['instance_name'],
        private_key_path=cfg['server']['aws']['key_pair'],
        # username=cfg['server']['aws']['username'],
        username=cfg['trainer']['aws']['username'],
        port=cfg['server']['aws']['Ingress_rules']['rules'][0]['ToPort'],
        command=cfg['server']['aws']['commands']['pull_image'],
    )
    print("Command run")


if __name__ == "__main__":
    main()
