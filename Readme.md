# AWS Project Template

This repository aims to provide a machine learning pipeline with all necessary functionality to train and evaluate models in a cloud environment through a single entry point.

## Project Overview

- **Development Environment Setup:**
  - Includes Data Versioning, Code Versioning, Containerization, and deployment of containers to AWS for training in the cloud.
  - Utilizes [DVC](https://dvc.org/), Git, Docker, and AWS/Boto3 for streamlined development processes.

- **Experimentation Features:**
  - Provides Tracking and Model Registry functionality using [MLflow](https://mlflow.org/) and [Hydra](https://hydra.cc/) for Configuration Management.

- **Simplified CLI:**
  - Utilizes Makefile and Python scripts to automate processes, providing a single entry point for complex workflows.

- **Deployment Strategy:**
  - Deploys a Containerized Flask Application in a cloud environment for seamless deployment and scaling.

## Tasks for Template Creation

This template can be reused multiple times. Below are the building blocks of this template for better understanding:

1. **VersionControlUtils (GIT, DVC):**
   - Provides classes to execute common Git and DVC commands necessary for version control of data and codebase.
   - Commands can be run using the CLI with `make command-tag` or integrated into more complex scripts for streamlined execution.

2. **CloudUtils (AWS/Boto3):**
   - Simplifies the handling of cloud resources using Python classes, automatable through CLI or other scripts.

3. **Configs (Hydra):**
   - Manages configuration using Hydra, allowing for experimentation with different parameters without modifying code.
   - Configuration parameters can be specified in YAML files and enforced using Python scripts for consistency.

4. **MLflow:**
   - Offers tools for shared model tracking, model registry, project management, and experiment logging.

5. **env_files:**
   - Stores system and project configurations in `.env` files. Ensure these are added to `.gitignore` to prevent sharing sensitive information.

6. **Makefile:**
   - Converts lengthy commands or sequences of commands into concise representative commands for ease of use.

7. **container (Docker):**
   - Provides a standardized and reproducible containerized environment, ensuring application reproducibility across different systems.

8. **Processes:**
   - Contains scripts to perform various tasks using the building blocks mentioned above.
   - These processes are simplified and automated through the Makefile, enabling complex operations to be executed with simple commands.

9. **Execute:**
   - executes are our final python scripts which will be called in makefile to run specific processes.
   - It includes, `init.py` which starts the project with provided aws, git, dvc configuration.
   - `push_docker_image.py` It containerize our code in docker image and push to provided configuration.
   - `version_code.py` It version contol our code in standard format with git.
   - `version_dataset.py` It version contol our dataset in standard format with dvc and git.
   - we can further add more scripts to it using our building block in very easy by adding more functions to `GeneralProcess` class in combine directory and the calling it in script. 

---

Refer to this guide for understanding the structure and purpose of this project template. Customize and utilize the provided building blocks to create robust and scalable machine learning pipelines in a cloud environment.

## Setting up the Project

1. **Git Configuration:**
   - Ensure Git is installed and configured on your machine.
   - Create a remote repository on GitHub (or another Git hosting service) without adding any files.
   - Provide the repository URL for configuration.

2. **AWS CLI Configuration:**
   - Make sure the AWS Command Line Interface (CLI) is installed and configured.
   - Set AWS credentials using environment variables or a `.env` file (`./env_files/aws.env`):
     ```plaintext
     AWS_ACCESS_KEY_ID=your_aws_access_key_id
     AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
     AWS_DEFAULT_REGION=your_aws_default_region
     ```
     Ensure `./env_files/aws.env` is added to `.gitignore` to avoid committing sensitive information.

3. **Docker Setup:**
   - Ensure Docker Engine is installed and running on your machine.

## CLI (How to use it?):
This part is our objective to create. We can alway add more cli command to create more processes as per our requirements.

   1. `export_aws_secrets`: set credentials set in `./env_files/aws.env` as environment variables. (You can delete this file after setting credentials, it will not affect functionality.)

   2. `make init`: start dvc, git, version dataset and git, add remote and push our code and dataset to git and remote storage.

   3. `make version_dataset`: It tag version to current dataset if there is any change in it and syc it with remote repo.

   4. `make version_code`: It tag version to our code and syc it with remote repo. It will auto increment version of code and push it to repo with tag.

   5. `make push_on_ecr`: containerize our code and push it AWS ECR.

   6. `make run_on_ec2`: launches ec2 instance on aws and pull docker container from ecr then run our container.