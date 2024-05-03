# ./src/execute/init.py
from omegaconf import DictConfig
from src.processes import setup_process
from src.Utils.utils import config_initializer


@config_initializer()
def main(cfg: DictConfig):
    setup_process.setup_version_control(cfg=cfg)


if __name__ == "__main__":
    main()
