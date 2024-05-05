# ./src/execute/pull_app_image_in_ec2.py
from omegaconf import DictConfig

from processes.setup_process import setup_aws
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig):
    aws = setup_aws(cfg['app'])
    aws.ec2_helper.command_instance_with_ssh(
        instance_name=cfg['app']['aws']['instance_name'],
        private_key_path=cfg['app']['aws']['key_pair'],
        # username=cfg['app']['aws']['username'],
        username=cfg['trainer']['aws']['username'],
        port=cfg['app']['aws']['Ingress_rules']['rules'][0]['ToPort'],
        command=cfg['app']['aws']['commands']['pull_image'],
    )
    print("Command run")


if __name__ == "__main__":
    main()
