# ./src/execute/stop_all_instance.py
from omegaconf import DictConfig

from processes.setup_process import setup_aws
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig) -> None:
    aws = setup_aws(cfg)
    aws.ec2_helper.stop_all_running_instances()


if __name__ == "__main__":
    main()
