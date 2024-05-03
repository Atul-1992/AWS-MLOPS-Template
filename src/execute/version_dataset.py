# ./src/execute/version_dataset.py
from omegaconf import DictConfig
from src.processes.setup_process import setup_version_control
from src.Utils.utils import config_initializer


@config_initializer()
def main(cfg: DictConfig) -> None:
    version_control = setup_version_control(cfg)
    version_control.version_dataset()


if __name__ == "__main__":
    main()
