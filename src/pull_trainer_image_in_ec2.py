# ./src/execute/pull_trainer_image_in_ec2.py
from omegaconf import DictConfig

from processes.setup_process import setup_aws
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig):
    aws = setup_aws(cfg['trainer'])
    aws.ec2_helper.command_instance_with_ssh(
        instance_name=cfg['trainer']['aws']['instance_name'],
        private_key_path=cfg['trainer']['aws']['key_pair'],
        # username=cfg['trainer']['aws']['username'],
        username=cfg['trainer']['aws']['username'],
        port=cfg['trainer']['aws']['Ingress_rules']['rules'][0]['ToPort'],
        command=cfg['trainer']['aws']['commands']['pull_image'],
    )
    # aws.ec2_helper.command_instance_with_ssh(instance_name=cfg['aws']['ec2']['instance_name'],
    #                                         # private_key_path=cfg['aws']['ec2']['private_key_path'],
    #                                         private_key_path=os.path.join(os.getcwd(), "".join([cfg['aws']['ec2']['key_pair'], ".pem"])),
    #                                         port=cfg['aws']['ec2']['ingress_rules']['ToPort'],
    #                                         username=cfg['aws']['ec2']['username'],
    #                                         command="echo 'HEllo SSH'")
    print("Command run")


if __name__ == "__main__":
    main()
