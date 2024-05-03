# ./src/execute/pull_trainer_image_in_ec2.py
from omegaconf import DictConfig
from src.processes.setup_process import setup_aws
from src.Utils.utils import config_initializer


@config_initializer()
def main(cfg: DictConfig):
    aws = setup_aws(cfg.docker.docker_dir)
    aws.ec2_helper.command_instance_with_ssh(
        instance_name=cfg.trainer.aws.instance_name,
        private_key_path=cfg.trainer.aws.intance_key_path,
        username=cfg.trainer.aws.username,
        port=cfg.trainer.aws.port,
        command=cfg.trainer.aws.commands.pull_image,
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
