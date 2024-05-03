# ./src/execute/push_trainer_image.py
from omegaconf import DictConfig
from src.processes.setup_process import setup_aws
from src.Utils.utils import config_initializer


@config_initializer()
def main(cfg: DictConfig) -> None:
    aws = setup_aws(cfg)

    aws.push_on_ecr(
        dockerfile_name=cfg.trainer.docker.dockerfile,
        image_name=cfg.trainer.docker.image_name,
        tag=cfg.trainer.docker.tag,
        repository_name=cfg.trainer.docker.ecr.repository_name,
    )


if __name__ == "__main__":
    main()
