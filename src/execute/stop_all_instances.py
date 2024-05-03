# ./src/execute/stop_all_instance.py
from omegaconf import DictConfig
from src.processes.setup_process import setup_aws
from src.Utils.utils import config_initializer


@config_initializer()
def main(cfg: DictConfig) -> None:
    aws = setup_aws(cfg)
    aws.ec2_helper.stop_all_running_instances()


if __name__ == "__main__":
    main()
