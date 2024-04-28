import subprocess
import boto3
import json


class AWSHelper:
    def __init__(self, cwd) -> None:
        self.working_directory = cwd

    def run_command(self, command:str):
        command = command.split(' ')
        try:
            result = subprocess.run(stdin=command, 
                           cwd=self.working_directory, 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE, 
                           text=True)
            if result.returncode == '0':
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        except subprocess.CalledProcessError as e:
                return False, str(e)
        
    def setup_env_variables(self):
        try:
            self.run_command('make export_aws_secrets')
            return True
        except Exception as e:
            print("./env_files/aws.env not found!")
            return False
