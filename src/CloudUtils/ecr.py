from src.CloudUtils.aws import AWSHelper
import base64
from src.CloudUtils.login import AWSCredentialManager
import docker
from botocore.exceptions import ClientError

class ECRHelper(AWSHelper):
	def __init__(self, cwd):
		super().__init__(cwd)
		self.session = AWSCredentialManager().get_aws_session()
		self.ecr = self.session.client('ecr')
		self.docker_client = docker.from_env()

	def create_repository(self, repository_name):
		self.repository_name = repository_name

		if not self.check_repository_exists(repository_name):
			response = self.ecr.create_repository(repositoryName=repository_name)
			self.repository_uri = response['repository']['repositoryUri']
			self.repository_arn = response['repository']['repositoryArn']
		else:
			self.get_registry_info()
		return True, {'Repo URI': self.repository_uri, "Repo ARN": self.repository_arn}
    
	def set_repository_name(self, repository_name):
		self.repository_name = repository_name
		return True
    
	def push_image(self, image_name, tag):
		self.tag_image(image_name, tag)
		# self.login()
		self.docker_client.images.push(self.repository_uri, tag=tag)
		# self.logout()
		return True

	def tag_image(self, image_name, tag):
		self.get_registry_info()
		old_image_name = f"{image_name}:{tag}"
		new_image_name = f"{self.repository_uri}:{tag}"
		print("Old Image Name: ", old_image_name)
		print("New Image Name: ", new_image_name)
		tagged_image = self.docker_client.images.get(old_image_name)
		print(f"\n Repsitory URI: {self.repository_uri}\n")
		tagged_image.tag(f"{self.repository_uri}/{new_image_name}")
		return True
    
	def get_registry_info(self):
		try:
			response = self.ecr.describe_repositories(repositoryNames=[self.repository_name])
			self.repository_uri = response['repositories'][0]['repositoryUri']
			self.repository_arn = response['repositories'][0]['repositoryArn']
			self.registry_endpoint = self.repository_uri.split('/')[0]
			return {"Repository URI": self.repository_uri, 
		   		"Registry Endpoint": self.registry_endpoint,
				"Registry ARN": self.repository_arn}
		
		except Exception as e:
			print(f"Can not get repository name: {e}")
		return False
    
	def login(self):
		try:
			# Get authorization token from Amazon ECR
			response = self.ecr.get_authorization_token()
			authorization_data = response['authorizationData'][0]
			
			# Extract token and registry endpoint from authorization data
			token = authorization_data['authorizationToken']
			registry = authorization_data['proxyEndpoint']
			
			# Decode token and extract username and password
			decoded_token = base64.b64decode(token).decode()
			username, password = decoded_token.split(':')
			
			# Log in to Docker registry using extracted credentials
			self.docker_client.login(username, password, registry=registry)
			
			return True

		except Exception as e:
			print(f"Error occurred during login: {e}")
			return False
    
	def logout(self):
		repo_info = self.get_registry_info()
		self.docker_client.logout(repo_info['Registry Endpoint'])
		return True
    
	def check_repository_exists(self, repository_name):
		try:
            # Describe the repository to check if it exists
			self.ecr.describe_repositories(repositoryNames=[repository_name])
			return True  # Repository exists
		except ClientError as e:
			if e.response['Error']['Code'] == 'RepositoryNotFoundException':
				return False  # Repository does not exist
			else:
                # Handle other errors as needed
				print(f"Error: {e}")
				return False  # Error occurred