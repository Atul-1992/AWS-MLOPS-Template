# ./src/execute/push_server_image.py
from omegaconf import DictConfig

from processes.setup_process import setup_aws
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig) -> None:
    aws = setup_aws(cfg)
    aws.push_on_ecr(
        dockerfile_name=cfg.docker.server.dockerfile,
        image_name=cfg.docker.server.image_name,
        tag=cfg.docker.server.tag,
        repository_name=cfg.docker.server.ecr.repository_name,
    )


if __name__ == "__main__":
    main()
