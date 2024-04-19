import os
import subprocess

class GitHelper:
    def __init__(self, repo_dir, branch, remote_name=None, remote_url=None):
        self.repo_dir = os.path.abspath(repo_dir)
        self.remote_name = remote_name
        self.remote_url = remote_url
        self.branch = branch
        self.version = 0
        if not self.is_git_repo():
            self.init()
        self.remote_url = remote_url
        self.remote_name = remote_name

    def is_git_repo(self):
        """
        Check if a Git repository exists in the specified directory.
        """
        return os.path.exists(os.path.join(self.repo_dir, ".git"))

    def init(self):
        """
        Initialize a new Git repository in the specified directory.
        """
        if not self.is_git_repo():
            subprocess.run(["git", "init", self.repo_dir])
            subprocess.run(["git", "-C", self.repo_dir, "checkout", "-b", "main"])
            print(f"Initialized Git repository in: {self.repo_dir}")
        else:
            print("This repo is already initialized!")

    def add(self, file_paths):
        """
        Stage specified files in a Git repository for the next commit.
        """
        file_paths = [os.path.abspath(file_path) for file_path in file_paths]
        subprocess.run(["git", "-C", self.repo_dir, "add"] + file_paths)

    def commit(self, commit_message=''):
        """
        Commit changes in a local Git repository.
        """
        if self.needs_commit():
            subprocess.run(["git", "-C", self.repo_dir, "commit", "-m", commit_message])
            print(f"Committed changes to repository '{self.repo_dir}' with message: {commit_message}")
            return True
        else:
            print(f"No changes to commit in repository '{self.repo_dir}'")
            return False

    def push(self, remote_name='origin'):
        """
        Push commits to the specified branch of the remote repository.
        """
        if not self.remote_url:
            print(f"No remote URL found for remote '{remote_name}'")
            return False
        subprocess.run(["git", "-C", self.repo_dir, "push", "--set-upstream", remote_name, self.branch])
        print(f"Pushed commits to {remote_name}/{self.branch} from repository: {self.repo_dir}")
        return True

    def create_remote(self):
        """
        Create a new remote repository in a local Git repository.
        """
        if not self.remote_url:
            print("Remote URL not provided.")
            return False
        subprocess.run(["git", "-C", self.repo_dir, "remote", "add", self.remote_name, self.remote_url])
        print(f"Successfully created remote '{self.remote_name}' ({self.remote_url}) in repository: {self.repo_dir}")
        return True

    def needs_commit(self):
        """
        Check if there are changes to commit in the local Git repository.
        """
        result = subprocess.run(["git", "-C", self.repo_dir, "status", "--porcelain"], capture_output=True)
        return bool(result.stdout.strip())

    def get_remote_url(self, remote_name):
        """
        Get the URL of a specified remote in the local Git repository.
        """
        result = subprocess.run(["git", "-C", self.repo_dir, "remote", "get-url", remote_name], capture_output=True)
        return result.stdout.strip().decode("utf-8")

    def version_code(self):
        """
        Create an annotated tag with the version number.
        """
        tag_name = f"version-{self.version}"
        subprocess.run(["git", "-C", self.repo_dir, "tag", "-a", tag_name, "-m", f"Version {self.version}"])
        self.version += 1
        print("Successfully versioned code")
        return True

    def tag(self, tags):
        """
        Create tags with messages in the local Git repository.
        """
        for key, value in tags.items():
            subprocess.run(["git", "-C", self.repo_dir, "tag", "-a", key, "-m", value])
        return True

    def needs_update(self):
        """
        Check if the local Git repository needs to be updated.
        """
        result = subprocess.run(["git", "-C", self.repo_dir, "status", "--porcelain"], capture_output=True)
        return bool(result.stdout.strip())

    def add_to_gitignore(self, directory_name):
        """
        Add a directory to .gitignore in the local Git repository.
        """
        gitignore_path = os.path.join(self.repo_dir, ".gitignore")
        with open(gitignore_path, "a") as gitignore_file:
            gitignore_file.write(f"\n{directory_name}\n")
        subprocess.run(["git", "-C", self.repo_dir, "add", gitignore_path])
        subprocess.run(["git", "-C", self.repo_dir, "commit", "-m", f"Ignore {directory_name}"])
        return True
