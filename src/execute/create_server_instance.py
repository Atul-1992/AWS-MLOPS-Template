# ./src/execute/run_on_ec2.py
from omegaconf import DictConfig
from src.processes.setup_process import setup_aws
from src.Utils.utils import config_initializer


@config_initializer()
def main(cfg: DictConfig) -> None:
    aws = setup_aws(cfg.docker_dir)
    aws.create_instance(
        instance_name=cfg.server.aws.instance_name,
        group_name=cfg.server.aws.group_name,
        key_pair=cfg.server.aws.key_pair,
        image_id=cfg.server.aws.image_id,
        instance_type=cfg.server.aws.instance_type,
        ingress_rules=cfg.server.aws.ingress_rules,
        userdata_script=cfg.server.aws.userdata_script,
        environment_variables=cfg.server.aws.environment_variables,
        instance_profile_name=cfg.server.aws.intance_profile.instance_profile_name,
        role_name=cfg.server.aws.intance_profile.role_name,
        assume_role_policy_document=cfg.server.aws.intance_profile.assume_role_policy_document,
        policy_names=cfg.server.aws.intance_profile.policy_names,
    )


if __name__ == "__main__":
    main()
