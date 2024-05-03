# ./src/execute/version_code.py
from omegaconf import DictConfig

from processes.setup_process import setup_version_control
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig) -> None:
    version_control = setup_version_control(cfg)
    version_control.version_code(cfg)


if __name__ == "__main__":
    main()
