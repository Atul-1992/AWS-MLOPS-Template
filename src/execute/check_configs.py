import hydra
from omegaconf import DictConfig, OmegaConf

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

sys.path.append(project_root)

@hydra.main(config_path="../../configs", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    # Access the configuration
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    main()