# ./src/execute/check_configs.py
from omegaconf import DictConfig, OmegaConf
from src.Utils.utils import config_initializer


@config_initializer()
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    main()
