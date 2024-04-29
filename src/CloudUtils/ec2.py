import boto3
import paramiko
import os
import time
from typing import List

import paramiko.client
from src.Utils.utils import Utils
from src.CloudUtils.aws import AWSHelper
from src.CloudUtils.login import AWSCredentialManager


class EC2Helper(AWSHelper):
    def __init__(self, cwd) -> None:
        super().__init__(cwd)
        self.session = AWSCredentialManager().get_aws_session()
        self.ec2 = self.session.client("ec2")
        self.vpc_id = self.get_vpc_id()[0]

    def get_vpc_id(self):
        try:
            # Retrieve information about all VPCs
            response = self.ec2.describe_vpcs()

            # Extract VPC IDs from the response
            vpc_ids = [vpc["VpcId"] for vpc in response["Vpcs"]]

            if vpc_ids:
                return vpc_ids
            else:
                print("No VPCs found in the account.")
                return None

        except Exception as e:
            print(f"Error occurred while retrieving VPCs: {e}")
            return None

    def create_security_group(
        self, group_name, description, ingress_rules: list = None
    ):
        # Define ingress (inbound) rules
        if ingress_rules is None:
            ingress_rules = [
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],  # Allow SSH from anywhere
                },
                {
                    "IpProtocol": "tcp",
                    "FromPort": 80,
                    "ToPort": 80,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],  # Allow HTTP from anywhere
                },
                {
                    "IpProtocol": "tcp",
                    "FromPort": 443,
                    "ToPort": 443,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],  # Allow HTTPS from anywhere
                },
            ]

        response = self.ec2.describe_security_groups(
            Filters=[
                {"Name": "group-name", "Values": [group_name]},
                {"Name": "vpc-id", "Values": [self.vpc_id]},
            ]
        )

        if response["SecurityGroups"]:
            # Security group already exists
            print(f"Security group '{group_name}' already exists.")
            return response["SecurityGroups"][0]["GroupId"]

        # Create a new security group if it doesn't exist
        security_group = self.ec2.create_security_group(
            GroupName=group_name, Description=description, VpcId=self.vpc_id
        )

        group_id = security_group["GroupId"]
        print(f"Security group '{group_name}' created with Group ID: {group_id}")

        # Add ingress rules to the security group
        self.ec2.authorize_security_group_ingress(
            GroupId=group_id, IpPermissions=ingress_rules
        )

        print("Ingress rules added to the security group.")

        return group_id

    def alter_security_group_permissions(self, group_id, ingress_rules):
        try:
            # Update ingress rules for the specified security group
            self.ec2.authorize_security_group_ingress(
                GroupId=group_id, IpPermissions=ingress_rules
            )

            print("Ingress rules updated for the security group.")

            return True

        except Exception as e:
            print(f"Error occurred while altering security group permissions: {e}")
            return False

    def list_security_groups_with_rules(self):
        try:
            # Retrieve information about all security groups in the VPC
            response = self.ec2.describe_security_groups(
                Filters=[{"Name": "vpc-id", "Values": [self.vpc_id]}]
            )

            if "SecurityGroups" in response:
                print("Security Groups with Rules:")
                for sg in response["SecurityGroups"]:
                    print(f"Security Group ID: {sg['GroupId']}")
                    print(f"Description: {sg['Description']}")

                    if "IpPermissions" in sg:
                        print("Ingress Rules:")
                        for rule in sg["IpPermissions"]:
                            protocol = rule["IpProtocol"]
                            from_port = rule["FromPort"]
                            to_port = rule["ToPort"]

                            if "IpRanges" in rule:
                                for ip_range in rule["IpRanges"]:
                                    cidr_ip = ip_range["CidrIp"]
                                    print(
                                        f"- {protocol} | Port Range: {from_port}-{to_port} | Source: {cidr_ip}"
                                    )
                            elif "UserIdGroupPairs" in rule:
                                for group_pair in rule["UserIdGroupPairs"]:
                                    source_group_id = group_pair["GroupId"]
                                    print(
                                        f"- {protocol} | Port Range: {from_port}-{to_port} | Source Group ID: {source_group_id}"
                                    )

                    print("")  # Print empty line for better readability

            else:
                print("No security groups found in the VPC.")

        except Exception as e:
            print(f"Error occurred while listing security groups: {e}")

    def check_instance_exists(self, instance_name):
        try:
            # Describe instances to check if instance with specified name exists
            response = self.ec2.describe_instances(
                Filters=[
                    {"Name": "tag:Name", "Values": [instance_name]},
                    {
                        "Name": "instance-state-name",
                        "Values": ["running", "pending", "stopped"],
                    },
                ]
            )

            if response["Reservations"]:
                print(f"Instance with name '{instance_name}' already exists.")
                return True
            else:
                print(f"No instance with name '{instance_name}' found.")
                return False

        except Exception as e:
            print(f"Error occurred while checking instance existence: {e}")
            return False

    def check_instance_running(self, instance_name):
        try:
            # Describe instances to check if instance with specified name exists
            response = self.ec2.describe_instances(
                Filters=[
                    {"Name": "tag:Name", "Values": [instance_name]},
                    {"Name": "instance-state-name", "Values": ["running"]},
                ]
            )

            if response["Reservations"]:
                print(f"Instance with name '{instance_name}' already exists.")
                return True
            else:
                print(f"No running instance with name '{instance_name}' found.")
                return False

        except Exception as e:
            print(f"Error occurred while checking instance existence: {e}")
            return False

    def create_or_start_ec2_instance_with_userdata(
        self,
        instance_name,
        image_id,
        instance_type,
        key_name,
        userdata_script,
        security_group_ids: list,
    ):
        try:
            # Check if instance with specified name already exists
            if self.check_instance_exists(instance_name):
                # Get the instance ID
                instance_id = self.get_instance_id_by_name(instance_name)
                if instance_id:
                    # Stop the instance
                    self.ec2.stop_instances(InstanceIds=[instance_id])
                    # Wait until the instance is stopped
                    waiter = self.ec2.get_waiter("instance_stopped")
                    waiter.wait(InstanceIds=[instance_id])
                    # Modify user data of the instance
                    self.ec2.modify_instance_attribute(
                        InstanceId=instance_id, Groups=security_group_ids
                    )
                    self.ec2.modify_instance_attribute(
                        InstanceId=instance_id, UserData={"Value": userdata_script}
                    )
                    # Start the instance
                    self.ec2.start_instances(InstanceIds=[instance_id])
                    waiter_running = self.ec2.get_waiter("instance_status_ok")
                    waiter_running.wait(InstanceIds=[instance_id])
                    print(
                        f"EC2 instance '{instance_name}' with ID '{instance_id}' started with new user data."
                    )
                    return instance_id
            else:
                # Create a new EC2 instance with user data (userdata_script)
                response = self.ec2.run_instances(
                    ImageId=image_id,
                    InstanceType=instance_type,
                    KeyName=key_name,
                    SecurityGroupIds=security_group_ids,
                    MinCount=1,
                    MaxCount=1,
                    UserData=userdata_script,
                    TagSpecifications=[
                        {
                            "ResourceType": "instance",
                            "Tags": [{"Key": "Name", "Value": instance_name}],
                        }
                    ],
                )
                instance_id = response["Instances"][0]["InstanceId"]
                waiter_running = self.ec2.get_waiter("instance_status_ok")
                waiter_running.wait(InstanceIds=[instance_id])
                print(
                    f"EC2 instance '{instance_name}' with ID '{instance_id}' created with user data."
                )
                return instance_id

        except Exception as e:
            print(f"Error occurred while creating or starting EC2 instance: {e}")
            return None

    def get_instance_id_by_name(self, instance_name):
        try:
            # Describe instances to retrieve the instance ID by name
            response = self.ec2.describe_instances(
                Filters=[
                    {"Name": "tag:Name", "Values": [instance_name]},
                    {
                        "Name": "instance-state-name",
                        "Values": ["running", "pending", "stopped"],
                    },
                ]
            )
            if response["Reservations"]:
                return response["Reservations"][0]["Instances"][0]["InstanceId"]
            else:
                print(f"No instance with name '{instance_name}' found.")
                return None
        except Exception as e:
            print(f"Error occurred while retrieving instance ID by name: {e}")
            return None

    def stop_instance(self, instance_id, timeout=300, wait=True):
        """
        Stop the specified EC2 instance and wait until its status is 'stopped'.

        Parameters:
        - instance_id (str): The ID of the EC2 instance to stop.
        - timeout (int): Maximum time in seconds to wait for the instance to reach 'stopped' status (default: 300 seconds).

        Returns:
        - bool: True if the instance's status becomes 'stopped' within the timeout period, False otherwise.
        """
        try:
            # Stop the EC2 instance
            response = self.ec2.stop_instances(InstanceIds=[instance_id])

            print(f"Stopping EC2 instance '{instance_id}'...")

            # Wait for the instance's status to become 'stopped'
            if wait:
                start_time = time.time()
                while True:
                    describe_response = self.ec2.describe_instances(
                        InstanceIds=[instance_id]
                    )
                    instance_state = describe_response["Reservations"][0]["Instances"][
                        0
                    ]["State"]["Name"]

                    if instance_state == "stopped":
                        print(f"Instance '{instance_id}' is now 'stopped'.")
                        return True

                    if time.time() - start_time >= timeout:
                        print(
                            f"Timeout occurred while waiting for instance '{instance_id}' to stop."
                        )
                        return False

                    time.sleep(15)  # Wait for 15 seconds before checking again

        except Exception as e:
            print(f"Error occurred while stopping EC2 instance '{instance_id}': {e}")
            return False

    def check_or_create_key_pair(self, key_pair_name):
        """
        Check if an AWS key pair exists with the specified name.
        If not, create a new key pair with the given name.

        Parameters:
        - key_pair_name (str): The name of the key pair to check/create.

        Returns:
        - str or None: The name of the existing or newly created key pair,
                    or None if an error occurred.
        """
        Utils.text_appender(f"{self.working_directory}/.gitignore", key_pair_name)
        try:
            response = self.ec2.describe_key_pairs(KeyNames=[key_pair_name])

            if response["KeyPairs"]:
                # Key pair already exists
                print(f"Key pair '{key_pair_name}' already exists.")
                return key_pair_name
        except:
            # Key pair does not exist, create a new one
            print(
                f"Key pair '{key_pair_name}' does not exist. Creating a new key pair..."
            )

            # Create the new key pair
            response = self.ec2.create_key_pair(KeyName=key_pair_name)
            try:
                # Save the private key to a file (optional)
                with open(f"{key_pair_name}.pem", "w") as f:
                    f.write(response["KeyMaterial"])
                print(f"New key pair '{key_pair_name}' created.")
                return key_pair_name
            except Exception as e:
                print(f"New Key could not be created!: {e}")
                return None

    def stop_all_running_instances(self):
        """
        Stop all running EC2 instances in the current AWS account and region.

        Returns:
        - bool: True if all instances were successfully stopped, False otherwise.
        """
        try:
            # Describe all running instances
            response = self.ec2.describe_instances(
                Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
            )

            # Iterate over reservations and stop each running instance
            instance_count = 0
            instance_stopped = []
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    instance_id = instance["InstanceId"]
                    # Stop the instance
                    if self.stop_instance(instance_id, wait=False):
                        instance_count += 1
                        instance_stopped.append(instance_id)

            if self.varify_instances_stopped(instance_stopped):
                print(f"Stopped {instance_count} running instances.")
                return True
            else:
                print("Could not stop all instance in time. Varify Manually")
                return False

        except Exception as e:
            print(f"Error occurred while stopping running instances: {e}")
            return False

    def varify_instances_stopped(self, instance_ids, timeout=300):
        """
        Verify that all specified EC2 instances have reached the 'stopped' state.

        Parameters:
        - instance_ids (list): List of instance IDs to verify.
        - timeout (int): Maximum time in seconds to wait for instances to reach 'stopped' state (default: 300 seconds).

        Returns:
        - bool: True if all instances are 'stopped' within the timeout period, False otherwise.
        """
        try:
            # Wait for each instance to reach 'stopped' state
            start_time = time.time()
            while True:
                describe_response = self.ec2.describe_instances(
                    InstanceIds=instance_ids
                )
                all_stopped = True

                for reservation in describe_response["Reservations"]:
                    for instance in reservation["Instances"]:
                        instance_id = instance["InstanceId"]
                        instance_state = instance["State"]["Name"]

                        if instance_state != "stopped":
                            all_stopped = False
                            break

                if all_stopped:
                    print("All instances are now 'stopped'.")
                    return True

                if time.time() - start_time >= timeout:
                    print("Timeout occurred while waiting for instances to stop.")
                    return False

                time.sleep(15)  # Wait for 15 seconds before checking again

        except Exception as e:
            print(f"Error occurred while verifying instance statuses: {e}")
            return False

    def describe_instance(self, instance_name):
        try:
            instance_id = self.get_instance_id_by_name(instance_name)
            instance = self.ec2.describe_instances(InstanceIds=[instance_id])[
                "Reservations"
            ][0]["Instances"][0]
            return instance
        except Exception as e:
            print(f"Excepation Raised in {self}:", e)
            return False

    def get_private_ip(self, instance_name):
        instance = self.describe_instance(instance_name)
        return instance["PrivateIpAddress"]

    def get_public_ip(self, instance_name):
        instance = self.describe_instance(instance_name)
        return instance["PublicIpAddress"]

    def command_instance_with_ssh(
        self, instance_name, private_key_path, port, username, command
    ):
        public_ip = self.get_public_ip(instance_name)
        ssh_client = paramiko.SSHClient()
        try:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
            ssh_client.connect(public_ip, port, username, pkey=private_key)
            _, stdout, _ = ssh_client.exec_command(command)
            # Read and print the output of the command
            print(f"Command executed: {command}")
            print("Output:")
            for line in stdout.readlines():
                print(line.strip())

            # Close the SSH connection
            ssh_client.close()
            return True
        except Exception as e:
            print(f"Error sending command with ssh: {e}")
            return False

    def command_multiple_instances_with_ssh(
        self, instance_names, private_key_path, port, username, command
    ):
        instance_status = [
            self.check_instance_running(instance_name)
            for instance_name in instance_names
        ]
        if all(instance_status):
            for instance_name in instance_names:
                self.command_instance_with_ssh(
                    instance_name, private_key_path, port, username, command
                )
            return True
        else:
            print("All listed instances are not in 'running' status.")
        return False
