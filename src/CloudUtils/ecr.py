import base64
import docker
from botocore.exceptions import ClientError

class ECRHelper:
    def __init__(self, session):
        self.session = session
        self.ecr = self.session.client("ecr")
        self.docker_client = docker.from_env()
        self.repository_arn = None
        self.repository_uri = None

    def create_repository(self, repository_name):
        self.set_repository_name(repository_name=repository_name)
        if not self.check_repository_exists(repository_name):
            response = self.ecr.create_repository(repositoryName=repository_name)
            self.repository_uri = response["repository"]["repositoryUri"]
            self.repository_arn = response["repository"]["repositoryArn"]
        else:
            self.get_registry_info()
        return True, {"Repo URI": self.repository_uri, "Repo ARN": self.repository_arn}

    def set_repository_name(self, repository_name):
        self.repository_name = repository_name
        return True

    def push_image(self, image_name, tag):
        self.tag_image(image_name, tag)
        self.authenticate_with_ecr()
        try:
            self.docker_client.images.push(f"{self.repository_uri}", tag=tag)
            return True
        except Exception as e:
            print(f"Error pushing image: {e}")
            return False

    def tag_image(self, image_name, tag):
        self.get_registry_info()
        if self.repository_uri:
            old_image_name = f"{image_name}:{tag}"
            tagged_image = self.docker_client.images.get(old_image_name)
            tagged_image.tag(f"{self.repository_uri}:{tag}")
            print(f"{self.repository_uri}:{tag}")
            return True
        print("Repository URI is not set.")
        return False

    def get_registry_info(self):
        try:
            response = self.ecr.describe_repositories(
                repositoryNames=[self.repository_name]
            )
            repository_info = response["repositories"][0]
            self.repository_uri = repository_info.get("repositoryUri")
            self.repository_arn = repository_info.get("repositoryArn")
            self.registry_endpoint = repository_info.get("repositoryUri", "").split("/")[0]
            return {
                "Repository URI": self.repository_uri,
                "Registry Endpoint": self.registry_endpoint,
                "Registry ARN": self.repository_arn,
            }
        except Exception as e:
            print(f"Error getting repository info: {e}")
            return None

    def authenticate_with_ecr(self):
        registry_id = self.repository_uri.split('.')[0]
        region = self.repository_uri.split('.')[3]
        token = self.ecr.get_authorization_token(registryIds=[registry_id])
        username = 'AWS'
        password = token['authorizationData'][0]['authorizationToken']
        
        # Decode the base64-encoded password
        # password = password.decode('base64')
        
        # Authenticate with Docker
        docker_client = docker.from_env()
        docker_client.login(username=username, password=password, registry=f'{registry_id}.dkr.ecr.{region}.amazonaws.com')
        

    def check_repository_exists(self, repository_name):
        try:
            self.ecr.describe_repositories(repositoryNames=[repository_name])
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "RepositoryNotFoundException":
                return False
            else:
                print(f"Error checking repository existence: {e}")
                return False
