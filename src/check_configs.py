# ./src/execute/check_configs.py

from omegaconf import DictConfig, OmegaConf

from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    main()
