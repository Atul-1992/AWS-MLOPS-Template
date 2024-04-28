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
        if self.needs_commit(['.']):
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
        subprocess.run(["git", "-C", self.repo_dir, "push", "--tags"])
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

    def needs_commit(self, directories):
        """
        Check if there are changes to commit in specific directories of the local Git repository.

        Args:
        - directories (list of str): List of directory paths to check for changes.

        Returns:
        - bool: True if there are changes in any of the specified directories, False otherwise.
        """
        # Construct the git status command with pathspec options for specified directories
        git_command = ["git", "-C", self.repo_dir, "status", "--porcelain"]
        
        for directory in directories:
            git_command.extend(['--', directory])

        # Run git status command to check for changes in specified directories
        result = subprocess.run(git_command, capture_output=True, text=True)
        
        # Check if there is any output from git status (indicating changes)
        return bool(result.stdout.strip())

    def get_remote_url(self, remote_name):
        """
        Get the URL of a specified remote in the local Git repository.
        """
        result = subprocess.run(["git", "-C", self.repo_dir, "remote", "get-url", remote_name], capture_output=True)
        return result.stdout.strip().decode("utf-8")

    # def version_code(self):
    #     """
    #     Create an annotated tag with the version number.
    #     """
    #     tag_name = f"Cv{self.version}"
    #     subprocess.run(["git", "-C", self.repo_dir, "tag", "-a", tag_name, "-m", f"Code Version: v{self.version}"])
    #     self.version += 1
    #     print("Successfully versioned code")
    #     return True

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

    def version_code(self, tag_prefix='v'):
        # Retrieve the latest tag of the specified prefix to determine the next version number
        next_version = int(self.get_latest_tag(tag_prefix)) + 1

        if next_version:
            # Tag the current commit with the next version number
            tag_name = f"{tag_prefix}{next_version}"
            self.tag_commit(tag_name)

            print(f"Tagged current commit with version: {tag_name}")
        else:
            print("Error: Failed to increment version.")

    def get_latest_tag(self, tag_prefix):
        # Get the latest tag with the specified prefix in the repository
        try:
            result = subprocess.run(['git', "-C", self.repo_dir, 'tag', '--list', f'{tag_prefix}*'], capture_output=True, text=True)
            tags_list = result.stdout.strip().split('\n')

            if tags_list:
                tags_list = [int(self.parse_version(tag, tag_prefix=tag_prefix)) for tag in tags_list if self.parse_version(tag, tag_prefix=tag_prefix) is not None]
                # Find the latest tag based on semantic versioning (assuming tags are in format '{prefix}X.Y.Z')
                if not tags_list:
                    tags_list.append("0")
                latest_tag = max(tags_list)
                return latest_tag
            else:
                return None
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None

    def parse_version(self, version, tag_prefix):
        tag = version[len(tag_prefix):]
        if tag.isdigit():
            return tag

    def tag_commit(self, tag_name):
        # Tag the current commit with the specified tag name
        try:
            subprocess.run(['git', "-C", self.repo_dir, 'tag', tag_name])
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            
    def create_branch(self, branch_name):
        try:
            subprocess.run(['git', "-C", self.repo_dir, 'branch', branch_name])
            print(f"Created branch '{branch_name}'")
        except subprocess.CalledProcessError as e:
            print(f"Error creating branch: {e}")

    def switch_to_branch(self, branch_name):
        try:
            subprocess.run(['git', "-C", self.repo_dir, 'checkout', branch_name])
            self.branch = branch_name
            print(f"Switched to branch '{branch_name}'")
        except subprocess.CalledProcessError as e:
            print(f"Error switching to branch: {e}")

    def create_and_switch_to_branch(self, branch_name):
        self.create_branch(branch_name=branch_name)
        self.switch_to_branch(branch_name=branch_name)

    def list_branches(self):
        try:
            # Run 'git branch' command to list all branches
            result = subprocess.run(['git', "-C", self.repo_dir, 'branch'], capture_output=True, text=True)
            
            # Get the output from the command
            output = result.stdout.strip()
            
            # Split the output into lines to extract branch names
            branches = [line.lstrip('* ').strip() for line in output.split('\n')]
            
            # Print the list of branches
            if branches:
                print("List of branches:")
                for branch in branches:
                    print(branch)
            else:
                print("No branches found.")
        except subprocess.CalledProcessError as e:
            print(f"Error listing branches: {e}")
        
    def latest_branch_tag(self, prefix='ds-'):
        branch_names = self.list_branches()
        data_branches = [branch for branch in branch_names if prefix in branch]
        return max([int(branch[len(prefix):]) for branch in data_branches])
    
    def create_new_ds_branch(self):
        latest_tag = self.latest_branch_tag() + 1
        self.create_and_switch_to_branch(f'ds-{latest_tag}')
    
    def version_dataset(self):
        self.create_and_switch_to_branch()