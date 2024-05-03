# ./src/execute/pull_server_image_in_ec2.py
from omegaconf import DictConfig

from processes.setup_process import setup_aws
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig):
    aws = setup_aws(cfg)
    aws.ec2_helper.command_instance_with_ssh(
        instance_name=cfg.app.aws.instance_name,
        private_key_path=cfg.app.aws.intance_key_path,
        username=cfg.app.aws.username,
        port=cfg.app.aws.port,
        command=cfg.app.aws.commands.pull_image,
    )
    print("Command run")


if __name__ == "__main__":
    main()
