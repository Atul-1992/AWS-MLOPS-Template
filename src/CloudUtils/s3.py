import json
import os


class S3Helper:
    def __init__(self, session) -> None:
        self.session = session
        self.s3 = self.session.client("s3")

    def list_buckets(self):
        buckets = self.s3.list_buckets()
        return [bucket["Name"] for bucket in buckets["Buckets"]]

    def create_bucket(self, bucket_name, **kwargs):
        self.s3.create_bucket(Bucket=bucket_name)
        if kwargs.get("version", False):
            self.s3.put_bucket_versioning(
                Bucket=bucket_name, VersioningConfiguration={"Status": "Enabled"}
            )
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:ListBucketVersions",
                    "Resource": f"arn:aws:s3:::{bucket_name}",
                },
            ],
        }
        policy_str = json.dumps(policy)
        try:
            self.s3.put_bucket_policy(Bucket=bucket_name, Policy=policy_str)
            return True
        except Exception as e:
            print(f"Error updating bucket policy: {e}")
            return False

    def upload_in_bucket(self, bucket_name, local_source_path, target_path):
        self.s3.upload_file(local_source_path, bucket_name, target_path)
        return True

    def list_objects_in_bucket(self, bucket_name):
        response = self.s3.list_objects_v2(Bucket=bucket_name)
        return [obj["Key"] for obj in response.get("Contents", [])]

    def download_objects(
        self, bucket_name, local_dest_path, object_key, version_id=None
    ):
        download_params = {
            "Bucket": bucket_name,
            "Key": object_key,
            "Filename": local_dest_path,
        }
        if version_id is not None:
            download_params["VersionId"] = version_id

        self.s3.download_file(**download_params)
        return True

    def allow_bucket_download(self, bucket_name, principle_name_ids=None):
        if not principle_name_ids:
            principle_name_ids = ["*"]

        principal_arns = [
            f"arn:aws:iam::{account_id}:root" for account_id in principle_name_ids
        ]

        policy = {
            "Version": "2012-10-17",
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
                    "Resource": f"arn:aws:s3:::{bucket_name}",
                },
            ],
        }

        policy_str = json.dumps(policy)

        try:
            self.s3.put_bucket_policy(Bucket=bucket_name, Policy=policy_str)
            return True
        except Exception as e:
            print(f"Error updating bucket policy: {e}")
            return False

    def list_bucket_versions(self, bucket_name):
        response = self.s3.list_object_versions(Bucket=bucket_name)
        return {
            version["VersionId"]: version["Key"]
            for version in response.get("Versions", [])
        }
