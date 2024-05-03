import subprocess
import os

project_dir = os.getcwd()


class DockerHelper:
    def __init__(self, dockerdir_rel_path) -> None:
        self.dockerdir_rel_path = dockerdir_rel_path

    def build_image(self, dockerfile_name, image_name, tag):
        dockerfile_path = os.path.join(
            os.path.abspath(self.dockerdir_rel_path), dockerfile_name
        )
        print("dockerfile path: ", dockerfile_path)
        # Check if Dockerfile exists
        if not os.path.isfile(dockerfile_path):
            raise FileNotFoundError(
                f"Dockerfile '{dockerfile_name}' not found in '{self.dockerdir_rel_path}'"
            )

        command = [
            "docker",
            "build",
            "-t",
            f"{image_name}:{tag}",
            "-f",
            dockerfile_path,
            ".",
        ]
        subprocess.run(command, check=True)

    def run_container(self, image_name, container_name, tag="latest"):
        command = [
            "docker",
            "run",
            "-d",
            "-p",
            "8000:8000",
            "--name",
            container_name,
            f"{image_name}:{tag}",
        ]
        subprocess.run(command, check=True)

    def stop_container(self, container_name):
        command = ["docker", "stop", container_name]
        subprocess.run(command, check=True)
        print(f"Container {container_name} stopped.")

    def get_container_info(self):
        command = ["docker", "ps"]
        subprocess.run(command, check=True)

    def run_command_in_container(self, container_name, command):
        command = ["docker", "exec", container_name] + command.split()
        subprocess.run(command, check=True)

    def run_docker_compose(
        self, docker_version="1.29.2", project_name="docker_compose_project"
    ):
        compose_file = f"{self.dockerdir_rel_path}/docker-compose.yml"

        command = [
            "docker",
            "compose",
            "-f",
            compose_file,
            "up",
            "-d",
            "--project-name",
            project_name,
        ]
        subprocess.run(command, check=True)

    def stop_docker_compose(self, project_name="docker_compose_project"):
        compose_file = f"{self.dockerdir_rel_path}/docker-compose.yml"

        command = [
            "docker",
            "compose",
            "-f",
            compose_file,
            "down",
            "--project-name",
            project_name,
        ]
        subprocess.run(command, check=True)
