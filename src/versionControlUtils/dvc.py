import subprocess


class DVCHelper:
    def __init__(self, project_dir, data_dir, remote_name, remote_url):
        self.project_dir = project_dir
        self.data_version = 0
        self.data_dir = data_dir
        self.remote_name = remote_name
        self.remote_url = remote_url

        if not self.is_dvc_repo():
            self.init()
        self.add_remote()

    def is_dvc_repo(self):
        """
        Check if the project directory is a DVC repository.
        """
        command = ["dvc", "status"]
        try:
            subprocess.run(
                command,
                cwd=self.project_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def init(self):
        """
        Initialize a new DVC repository.
        """
        command = ["dvc", "init", "--no-scm"]
        try:
            if not self.is_dvc_repo():
                subprocess.run(command, cwd=self.project_dir, check=True)
                self.add_data(self.data_dir)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error initializing DVC repository: {e}")
            return False

    def add_data(self, data_dir):
        """
        Add data to the DVC repository.
        """
        command = ["dvc", "add", data_dir]
        try:
            subprocess.run(command, cwd=self.project_dir, check=True)
            if isinstance((self.data_dir), list):
                self.data_dir.append(data_dir)
            else:
                [self.data_dir].append(data_dir)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error adding data to DVC repository: {e}")
            return False

    def add_remote(self):
        """
        Add a remote to the DVC repository.
        """
        command = ["dvc", "remote", "add", "-d", self.remote_name, self.remote_url]
        try:
            if not self.does_remote_exist():
                subprocess.run(command, cwd=self.project_dir, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error adding remote to DVC repository: {e}")
            return False

    def import_data(self):
        """
        Add a remote to the DVC repository.
        """
        command = ["dvc", "import", "-o", "output", self.data_dir, self.remote_url]
        try:
            if not self.does_remote_exist():
                subprocess.run(command, cwd=self.project_dir, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error pulling data from remote repository {self.remote_url}: {e}")
            return False

    def push(self):
        """
        Push data tracked by DVC to the configured remote storage.
        """
        command = ["dvc", "push", "-r", self.remote_name]
        try:
            subprocess.run(command, cwd=self.project_dir, check=True)
            print("Data pushed to DVC remote successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error pushing data to DVC remote: {e}")
            return False

    def pull(self):
        """
        Pull data tracked by DVC from the configured remote storage.
        """
        command = ["dvc", "pull", "-r", self.remote_name]
        try:
            subprocess.run(command, cwd=self.project_dir, check=True)
            print("Data pulled from DVC remote successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error pulling data from DVC remote: {e}")
            return False

    def needs_update(self):
        """
        Check if the dataset tracked by DVC needs to be updated.
        """
        command = ["dvc", "status", self.data_dir]
        try:
            result = subprocess.run(
                command,
                cwd=self.project_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output = result.stdout.decode().strip()
            if (
                "changed_files: 0" in output
                and "added_files: 0" in output
                and "deleted_files: 0" in output
            ):
                print("Dataset is up to date.")
                return False

            print("Dataset needs to be updated.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error checking dataset status: {e}")
            return False

    def does_remote_exist(self):
        """
        Check if a remote exists in the DVC repository.

        Args:
            project_dir (str): Path to the DVC repository directory.
            remote_name (str): Name of the remote to check.

        Returns:
            bool: True if the remote exists, False otherwise.
        """
        try:
            # Execute 'dvc remote list' command to get the list of remotes
            command = ["dvc", "remote", "list"]
            result = subprocess.run(
                command,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse the output to check if the specified remote exists
            remotes = result.stdout.strip().split()
            return self.remote_name in remotes
        except subprocess.CalledProcessError:
            # Handle any errors (e.g., if DVC command fails)
            return False

    def update_dataset(self):
        """
        Pull data tracked by DVC from the configured remote storage.
        """
        command = ["dvc", "update", self.data_dir]
        try:
            subprocess.run(command, cwd=self.project_dir, check=True)
            print("Data pulled from DVC remote successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error pulling data from DVC remote: {e}")
            return False
