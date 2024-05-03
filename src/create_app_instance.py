# ./src/execute/run_on_ec2.py
from omegaconf import DictConfig

from processes.setup_process import setup_aws
from utils.utils import config_initializer


@config_initializer(__file__)
def main(cfg: DictConfig) -> None:
    aws = setup_aws(cfg.docker_dir)
    aws.create_instance(
        instance_name=cfg.app.aws.instance_name,
        group_name=cfg.app.aws.group_name,
        key_pair=cfg.app.aws.key_pair,
        image_id=cfg.app.aws.image_id,
        instance_type=cfg.app.aws.instance_type,
        ingress_rules=cfg.app.aws.ingress_rules,
        userdata_script=cfg.app.aws.userdata_script,
        environment_variables=cfg.app.aws.environment_variables,
        instance_profile_name=cfg.app.aws.intance_profile.instance_profile_name,
        role_name=cfg.app.aws.intance_profile.role_name,
        assume_role_policy_document=cfg.app.aws.intance_profile.assume_role_policy_document,
        policy_names=cfg.app.aws.intance_profile.policy_names,
    )


if __name__ == "__main__":
    main()
