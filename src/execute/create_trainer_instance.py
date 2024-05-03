# ./src/execute/run_on_ec2.py
from omegaconf import DictConfig
from src.processes.setup_process import setup_aws
from src.Utils.utils import config_initializer


@config_initializer()
def main(cfg: DictConfig) -> None:
    aws = setup_aws(cfg.docker_dir)
    aws.create_instance(
        instance_name=cfg.trainer.aws.instance_name,
        group_name=cfg.trainer.aws.group_name,
        key_pair=cfg.trainer.aws.key_pair,
        image_id=cfg.trainer.aws.image_id,
        instance_type=cfg.trainer.aws.instance_type,
        ingress_rules=cfg.trainer.aws.ingress_rules,
        userdata_script=cfg.trainer.aws.userdata_script,
        environment_variables=cfg.trainer.aws.environment_variables,
        instance_profile_name=cfg.trainer.aws.intance_profile.instance_profile_name,
        role_name=cfg.trainer.aws.intance_profile.role_name,
        assume_role_policy_document=cfg.trainer.aws.intance_profile.assume_role_policy_document,
        policy_names=cfg.trainer.aws.intance_profile.policy_names,
    )


if __name__ == "__main__":
    main()
