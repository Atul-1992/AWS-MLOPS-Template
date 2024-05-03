import os
import boto3


class IAMHelper:
    def __init__(self, session) -> None:
        self.working_directory = os.getcwd()
        self.session = session
        self.iam = boto3.client("iam")

    def check_role_exists(self, role_name):
        try:
            self.iam.get_role(RoleName=role_name)
            return True
        except self.iam.exceptions.NoSuchEntityException:
            return False

    def create_role(self, role_name, assume_role_policy_document):
        response = self.iam.create_role(
            RoleName=role_name, AssumeRolePolicyDocument=assume_role_policy_document
        )
        return response["Role"]["Arn"]

    def attach_policies_to_role(self, role_name, policy_arns):
        for policy_arn in policy_arns:
            try:
                self.iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
            except self.iam.exceptions.NoSuchEntityException:
                print(f"Policy '{policy_arn}' not found.")

    def get_policy_arn(self, policy_name):
        paginator = self.iam.get_paginator("list_policies")
        for page in paginator.paginate():
            for policy in page["Policies"]:
                if policy["PolicyName"] == policy_name:
                    return policy["Arn"]
        return None

    def create_or_get_role(
        self, role_name, assume_role_policy_document, policy_names=None
    ):
        if self.check_role_exists(role_name):
            print(f"IAM role '{role_name}' already exists.")
            return self.get_role_arn(role_name)
        else:
            print(f"IAM role '{role_name}' does not exist. Creating...")
            role_arn = self.create_role(role_name, assume_role_policy_document)
            print(f"IAM role '{role_name}' created with ARN: {role_arn}")
            if policy_names:
                policy_arns = [
                    self.get_policy_arn(policy_name) for policy_name in policy_names
                ]
                self.attach_policies_to_role(role_name, policy_arns)
                print("Policies attached to the role.")
            return role_arn

    def get_role_arn(self, role_name):
        response = self.iam.get_role(RoleName=role_name)
        return response["Role"]["Arn"]

    def create_instance_profile(self, instance_profile_name):
        try:
            instance_profile_response = self.iam.create_instance_profile(
                InstanceProfileName=instance_profile_name
            )
            instance_profile_arn = instance_profile_response["InstanceProfile"]["Arn"]
            print(
                f"IAM instance profile '{instance_profile_name}' created with ARN: {instance_profile_arn}"
            )
            return instance_profile_arn
        except self.iam.exceptions.EntityAlreadyExistsException:
            print(f"IAM instance profile '{instance_profile_name}' already exists.")
            instance_profile_response = self.iam.get_instance_profile(
                InstanceProfileName=instance_profile_name
            )
            instance_profile_arn = instance_profile_response["InstanceProfile"]["Arn"]
            print(
                f"IAM instance profile '{instance_profile_name}' ARN: {instance_profile_arn}"
            )
            return instance_profile_arn
        except Exception as e:
            print(f"Error creating IAM instance profile '{instance_profile_name}': {e}")
            return None

    def add_roles_to_instance_profile(self, instance_profile_name, role_names):
        try:
            # Get the instance profile ARN
            instance_profile_response = self.iam.get_instance_profile(
                InstanceProfileName=instance_profile_name
            )
            # instance_profile_arn = instance_profile_response['InstanceProfile']['Arn']

            # Add roles to the instance profile
            for role_name in role_names:
                try:
                    self.iam.add_role_to_instance_profile(
                        InstanceProfileName=instance_profile_name, RoleName=role_name
                    )
                    print(
                        f"IAM role '{role_name}' added to instance profile '{instance_profile_name}'."
                    )
                except self.iam.exceptions.EntityAlreadyExistsException:
                    print(
                        f"IAM role '{role_name}' is already associated with instance profile '{instance_profile_name}'."
                    )
                except Exception as e:
                    print(
                        f"Error adding IAM role '{role_name}' to instance profile '{instance_profile_name}': {e}"
                    )
            return instance_profile_response["InstanceProfile"]["Arn"]
        except self.iam.exceptions.NoSuchEntityException:
            print(f"IAM instance profile '{instance_profile_name}' not found.")
        except Exception as e:
            print(f"Error getting IAM instance profile '{instance_profile_name}': {e}")
