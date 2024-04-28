import docker
import os

project_dir =os.getcwd()

class DockerHelper:
	def __init__(self, project_dir, dockerdir_rel_path) -> None:
		self.project_dir = project_dir
		self.client = docker.from_env()
		self.dockerdir_rel_path = dockerdir_rel_path
		self.docker_compose_file = None

	def build_image(self, dockerfile_name, image_name, tag):
		dockerfile_path = os.path.join(self.project_dir, self.dockerdir_rel_path, dockerfile_name)
		print("dockerfile path: ", dockerfile_path)
        # Check if Dockerfile exists
		if not os.path.isfile(dockerfile_path):
			raise FileNotFoundError(f"Dockerfile '{dockerfile_name}' not found in '{self.dockerdir_rel_path}'")
		
		image, _ = self.client.images.build(path=self.dockerdir_rel_path, dockerfile=dockerfile_name, tag=f"{image_name}:{tag}")
		return image

	def run_container(self, image_name, container_name, tag='latest'):
		container = self.client.containers.run(f"{image_name}:{tag}", 
													detach=True, 
													ports={'8000/tcp': 8000}, 
													name=container_name)
		return container

	def stop_container(self, container_name):
		container = self.client.containers.get(container_name)
		container.stop()
		print(f"Container {container_name} stopped.")

	def get_container_info(self):
		containers = self.client.containers.list()

		for container in containers:
			print(f"Container ID: {container.id}")
			print(f"Container Name: {container.name}")
			print(f"Container Status: {container.status}")
			print(f"Container Image: {container.image.tags[0]}")
			print("-----------------------")

	def run_command_in_container(self, container_name, command):
		
		try:
			container = self.client.containers.get(container_name)
			exec_response = container.exec_run(command)
			exit_code = exec_response.exit_code
			output = exec_response.output.decode('utf-8').strip()
			print(f"Command executed with exit code {exit_code}")
			print(f"Output:\n{output}")
		except docker.errors.NotFound as e:
			print(f"Container '{container_name}' not found: {e}")
		except docker.errors.APIError as e:
			print(f"Error executing command in container: {e}")


	def run_docker_compose(self, docker_version="1.29.2", project_name='docker_compose_project'):
		compose_file = f"{self.dockerdir_rel_path}/docker-compose.yml"

		if not os.path.isfile(compose_file):
			raise FileNotFoundError(f"Docker Compose file ('docker-compose.yml') not found in '{self.dockerdir_rel_path}'")
		# Run Docker Compose project
		containers = self.client.containers.run(
			f'docker/compose:{docker_version}',
			command=f"-f {compose_file} up -d"
		)

		print("Docker Compose project started successfully.")
		
	def stop_docker_compose(self, project_name='docker_compose_project'):
		compose_file = f"{self.dockerdir_rel_path}/docker-compose.yml"
		project_name = project_name

		if not os.path.isfile(compose_file):
			raise FileNotFoundError(f"Docker Compose file ('docker-compose.yml') not found in '{self.dockerdir_rel_path}'")
		
		# Run Docker Compose command to stop the project
		containers = self.client.containers.run(
			'docker/compose:1.29.2',
			command=f"-f {compose_file} down"
		)

		print("Docker Compose project stopped successfully.")