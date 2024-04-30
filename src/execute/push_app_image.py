import hydra
from omegaconf import DictConfig


from src.processes.setup_process import setup_general_process


@hydra.main(config_name="config", config_path="../../configs", version_base=None)
def main(cfg: DictConfig) -> None:
    processes = setup_general_process(cfg)
    processes.push_on_ecr(
        dockerfile_name=cfg["docker"]["app"]["dockerfile_name"],
        image_name=cfg["docker"]['app']["image_name"],
        tag=cfg["docker"]['app']["tag"],
        repository_name=cfg["aws"]["ecr"]["app_repository_name"],
    )


if __name__ == "__main__":
    main()
