import boto3
from src.CloudUtils.aws import AWSHelper


class IAMHelper(AWSHelper):
    def __init__(self, cwd) -> None:
        super().__init__(cwd)
        self.iam = boto3.client('iam')


    def check_role_exists(self, role_name):
        """
        Check if the given IAM role exists.
        
        Args:
        - role_name (str): The name of the IAM role to check.
        
        Returns:
        - bool: True if the role exists, False otherwise.
        """
        try:
            self.iam.get_role(RoleName=role_name)
            return True
        except self.iam.exceptions.NoSuchEntityException:
            return False

    def create_role(self, role_name, assume_role_policy_document):
        """
        Create an IAM role with the given name and assume role policy document.
        
        Args:
        - role_name (str): The name of the IAM role to create.
        - assume_role_policy_document (dict): The assume role policy document for the IAM role.
        
        Returns:
        - str: The ARN of the created IAM role.
        """
        response = self.iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy_document
        )
        return response['Role']['Arn']

    def attach_policies_to_role(self, role_name, policy_arns):
        """
        Attach policies to the given IAM role.
        
        Args:
        - role_name (str): The name of the IAM role to attach policies to.
        - policy_arns (list): List of ARNs of the policies to attach.
        
        Returns:
        - None
        """
        for policy_arn in policy_arns:
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )

    def create_or_get_role(self, role_name, assume_role_policy_document, policy_arns=None):
        """
        Check if the IAM role exists, if not create it.
        Attach policies to the role if provided.
        
        Args:
        - role_name (str): The name of the IAM role to create or get.
        - assume_role_policy_document (dict): The assume role policy document for the IAM role.
        - policy_arns (list): List of ARNs of the policies to attach. Default is None.
        
        Returns:
        - str: The ARN of the created or existing IAM role.
        """
        if self.check_role_exists(role_name):
            print(f"IAM role '{role_name}' already exists.")
            return self.get_role_arn(role_name)
        else:
            print(f"IAM role '{role_name}' does not exist. Creating...")
            role_arn = self.create_role(role_name, assume_role_policy_document)
            print(f"IAM role '{role_name}' created with ARN: {role_arn}")
            if policy_arns:
                self.attach_policies_to_role(role_name, policy_arns)
                print("Policies attached to the role.")
            return role_arn

    def get_role_arn(self, role_name):
        """
        Get the ARN of an existing IAM role.
        
        Args:
        - role_name (str): The name of the IAM role.
        
        Returns:
        - str: The ARN of the IAM role.
        """
        response = self.iam.get_role(RoleName=role_name)
        return response['Role']['Arn']

# Example usage:
# if __name__ == "__main__":
#     role_name = "MyCustomRole"
#     assume_role_policy_document = {
#         "Version": "2012-10-17",
#         "Statement": [
#             {
#                 "Effect": "Allow",
#                 "Principal": {
#                     "Service": "ec2.amazonaws.com"
#                 },
#                 "Action": "sts:AssumeRole"
#             }
#         ]
#     }
#     policy_arns = [
#         "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
#         "arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess"
#     ]
    