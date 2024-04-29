import subprocess


class GitHelper:
    def __init__(self, working_directory) -> None:
        self.working_directory = working_directory
        self.version = 0

    def run_git_command(self, command: str):
        command = command.split(" ")
        try:
            result = subprocess.run(
                stdin=command,
                cwd=self.working_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == "0":
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        except subprocess.CalledProcessError as e:
            return False, str(e)

    def create_repository(self, directory):
        success, output = self.run_git_command("git init", working_directory=directory)
        if success:
            self.run_git_command("git branch -m master main")
            return True, "Git repository created successfully."
        else:
            return False, f"Failed to create git repository: {output}"

    def add_remote(self, remote_url):
        success, output = self.run_git_command(f"git remote add origin {remote_url}")
        if success:
            return True, "Remote repository added successfully."
        else:
            return False, f"Failed to add remote repository: {output}"

    def push_to_remote(self):
        self.run_git_command("git add .")
        self.version_code()
        success, output = self.run_git_command(f"git push -u origin main")
        self.version = self.version - 1
        if success:
            return True, "Local changes pushed to remote repository."
        else:
            return False, f"Failed to push to remote repository: {output}"

    def version_code(self):
        success, output = self.run_git_command(
            f'git tag -a version -m "{self.version}"'
        )
        if success:
            self.version = self.version + 1
            return True, str(self.version)
        else:
            return False, f"Failed to version: {self.version + 1}: {output}"


class DVCHelper:
    def __init__(self, working_directory):
        self.working_directory = working_directory
        self.data_version = 0

    def run_command(self, command: str):
        command = command.split(" ")
        try:
            result = subprocess.run(
                stdin=command,
                cwd=self.working_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == "0":
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        except subprocess.CalledProcessError as e:
            return False, str(e)

    def initialize(self, data_dir):
        self.data_dir = data_dir
        self.run_command("dvc init")
        self.run_command(f"dvc add {str(data_dir)}")
        self.run_command("git add .")
        self.run_command(f"git commit -m 'Add {data_dir} with DVC'")
        self.run_command("dvc commit")
        return True

    def dvc_push(self, local_storage_path):
        self.local_storage_path = local_storage_path
        self.run_command(f"dvc add {local_storage_path}")
        self.run_command("dvc push")
        success, _ = self.run_command(
            f"git commit {local_storage_path} -m 'Dataset updates with {self.data_version}'"
        )
        if success == True:
            self.data_version += 1
        return True

    def set_remote_storage(self, storage_path, remote_name="myremote"):
        self.run_commnad(f"dvc remote add -d {remote_name} {storage_path}")
        return True

    def create_stage(
        self, name: str, parameters: list, dependencies: list, outputs: list
    ):
        self.run_command(
            f"dvc stage add {name} -p {' '.join(parameters)} -d {' '.join(dependencies)} -o {' '.join(outputs)}"
        )
        self.run_command("git add .")
        self.run_command(f"git commit -m {name} stage defined")
        return True

    def pull(self):
        self.run_command("dvc pull")
        return True
