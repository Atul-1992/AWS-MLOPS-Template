import boto3


class AWSCredentialManager:
	def __init__(self) -> None:
		self.session = None

	def get_aws_session(self):
		# List of authentication methods to try
		authentication_methods = [
			self.try_with_aws_cli_configuration,
			self.try_with_environment_variables
		]

		# Try each authentication method
		for authenticate_method in authentication_methods:
			self.session = authenticate_method()
			if self.session is not None:
				return self.session
		print("AWS authentication failed!")
		return None  # Return None if all authentication methods failed

	def try_with_environment_variables(self):
		# Attempt to create a Boto3 session using environment variables
		try:
			session = boto3.Session()
			# Check if session is valid by making a simple API call
			session.client('sts').get_caller_identity()
			return session
		except Exception as e:
			print(f"Failed to authenticate with environment variables: {e}")
			return None

	def try_with_aws_cli_configuration(self):
		# Attempt to create a Boto3 session using AWS CLI configuration
		try:
			session = boto3.Session()
			# Check if session is valid by making a simple API call
			session.client('sts').get_caller_identity()
			return session
		except Exception as e:
			print(f"Failed to authenticate with AWS CLI configuration: {e}")
			return None

