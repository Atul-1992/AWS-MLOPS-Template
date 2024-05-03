# ./src/execute/push_app_image.py
from omegaconf import DictConfig
from src.processes.setup_process import setup_aws
from src.Utils.utils import config_initializer


@config_initializer()
def main(cfg: DictConfig) -> None:
    aws = setup_aws(cfg)
    aws.push_on_ecr(
        dockerfile_name=cfg.app.docker.dockerfile,
        image_name=cfg.app.docker.image_name,
        tag=cfg.app.docker.tag,
        repository_name=cfg.app.docker.ecr.repository_name,
    )


if __name__ == "__main__":
    main()
