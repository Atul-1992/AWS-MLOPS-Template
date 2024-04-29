from src.CloudUtils.aws import AWSHelper
from src.CloudUtils.login import AWSCredentialManager
import json


class S3Helper(AWSHelper):
    def __init__(self, cwd) -> None:
        super().__init__(cwd)
        self.session = AWSCredentialManager().get_aws_session()
        self.s3 = self.session.client("s3")
        # self.current_bucket_name = None

    def list_buckets(self):
        buckets = self.s3.list_buckets()
        return [bucket["Name"] for bucket in buckets["Buckets"]]

    def create_bucket(self, bucket_name, **kwargs):
        """
        bucket_name: S3 Bucket Name
        version: True for Enabling versioning
        """
        self.s3.create_bucket(Bucket=bucket_name)
        if kwargs.get("version", False):
            self.s3.put_bucket_versioning(
                Bucket=bucket_name, VersioningConfiguration={"Status": "Enabled"}
            )
        policy = {
            [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:ListBucketVersions",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                },
            ]
        }

        policy_str = json.dumps(policy)

        try:
            self.s3.put_bucket_policy(Bucket=bucket_name, Policy=policy_str)
            return True
        except Exception as e:
            print(f"Error updating bucket policy: {e}")
            return False

        return True

    def upload_in_bucket(self, bucket_name, local_source_path, target_path):
        self.s3.upload_file(local_source_path, bucket_name, target_path)
        return True

    def list_objects_in_bucket(self, bucket_name):
        response = self.s3.list_objects_v2(Bucket=bucket_name)
        return [obj["Key"] for obj in response["Contents"]]

    def download_objects(
        self, bucket_name, local_dest_path, object_key, version_id=None
    ):
        download_params = {
            "Bucket": bucket_name,
            "Key": object_key,
            "FileName": local_dest_path,
        }
        if version_id is not None:
            download_params["VersionId"] = version_id

        self.s3.download_file(**download_params)
        return True

    def allow_bucket_download(self, bucket_name, principle_name_ids=None):
        if not principle_name_ids:
            principle_name_ids = "*"

        principal_arns = [
            f"arn:aws:iam::{account_id}:root" for account_id in principle_name_ids
        ]

        policy = {
            # "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": principal_arns},
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                },
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:ListBucketVersions",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                },
            ]
        }

        policy_str = json.dumps(policy)

        try:
            self.s3.put_bucket_policy(Bucket=bucket_name, Policy=policy_str)
            return True
        except Exception as e:
            print(f"Error updating bucket policy: {e}")
            return False

    def list_bucket_versions(self, bucket_name):
        # List object versions in the bucket
        response = self.s3.list_object_versions(Bucket=bucket_name)

        # Access version information
        return {
            version["VersionId"]: version["Key"] for version in response["Versions"]
        }
