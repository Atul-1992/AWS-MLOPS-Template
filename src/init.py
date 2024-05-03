# ./src/execute/init.py
from omegaconf import DictConfig

from processes import setup_process
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig):
    setup_process.setup_version_control(cfg=cfg)


if __name__ == "__main__":
    main()
