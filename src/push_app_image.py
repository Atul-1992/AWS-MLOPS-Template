# ./src/execute/push_app_image.py
from omegaconf import DictConfig

from processes.setup_process import setup_aws
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig) -> None:
    aws = setup_aws(cfg.app)
    aws.push_on_ecr(
        dockerfile_name=cfg.app.docker.dockerfile_name,
        image_name=cfg.app.docker.image_name,
        tag=cfg.app.docker.tag,
        repository_name=cfg.app.docker.repository_name,
    )


if __name__ == "__main__":
    main()
