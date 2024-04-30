# AWS MLOPS Project Template

This repository aims to provide a machine learning pipeline with all necessary functionality to train and evaluate models in a cloud environment through a single entry point.
This project is created in very modular structure so that we can add and remove any functionality easily as per our need.

**Documentation Structure:**

- [AWS MLOPS Project Template](#aws-mlops-project-template)
  - [Project Overview](#project-overview)
  - [Template Structure](#template-structure)
  - [Project Setup](#project-setup)
  - [CLI (How to use this template?):](#cli-how-to-use-this-template)

## <a id="project-overview">Project Overview</a>

- **Development Environment Setup:**
  - Includes Data Versioning, Code Versioning, Containerization, and deployment of containers to AWS for training in the cloud.
  - Utilizes [DVC](https://dvc.org/), Git, Docker, and AWS/Boto3 for streamlined development processes.

- **Configuration Management:**
   - With [Hydra](https://hydra.cc/docs/intro/), we manage our configuration of setup and Machine Learning Experiment separately. It helps us keep our code clean and untouched unless we really need to change it.

- **Experimentation Features:**
  - Provides Tracking and Model Registry functionality using [MLflow](https://mlflow.org/) and [Hydra](https://hydra.cc/) for Configuration Management.

- **Simplified CLI:**
  - Utilizes Makefile and Python scripts to automate processes, providing a single entry point for complex workflows.

- **Deployment Strategy:**
  - Deploys a Containerized Flask Application in a cloud environment for seamless deployment and scaling.

## <a id="template-structure">Template Structure</a>

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

10. **app (Flask):**
   - Flask app with user registration and authentication feature, it includes it's own sqlite database for user information.

---

Refer to this guide for understanding the structure and purpose of this project template. Customize and utilize the provided building blocks to create robust and scalable machine learning pipelines in a cloud environment.

## <a id="project-setup">Project Setup</a>

1. **Installations:**
   You need to install and setup Git, DVC, Hydra, AWS CLI & boto3, gcc (for makefile), Mlflow and Docker before preceding with this template.

2. **Git Configuration:**
   - Ensure Git is installed and configured on your machine.
   - Create a remote repository on GitHub (or another Git hosting service) without adding any files.
   - Provide the repository URL for configuration.
   - To know more about git commands, please visit -> [Git Docs](https://git-scm.com/docs)

3. **AWS CLI Configuration:**
   - Make sure the AWS Command Line Interface (CLI) is installed and configured.
   - Set AWS credentials using environment variables or a `.env` file (`./env_files/aws.env`):
     ```plaintext
     AWS_ACCESS_KEY_ID=your_aws_access_key_id
     AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
     AWS_DEFAULT_REGION=your_aws_default_region
     ```
     Ensure `./env_files/aws.env` is added to `.gitignore` to avoid committing sensitive information.

4. **Docker Setup:**
   - Ensure Docker Engine is installed and running on your machine.
   - To know more about Docker, please visit -> [Docker Docs](https://docs.docker.com/)

5. **Hydra Config:**
   - This will be second most used functionality after `Makefile` cli. Basically we set all of our configuration separately in `configs` folder where we can change set our configuration and work on our code virtually independently. All the configurations are written in simple `.yaml` files.
   - Alternatively we can set our configuration pythonically as done in `config_schemas` folder. For simplicity and to keep code relevent with respect to warnings, I choose to change schemas `config_name` to `config_schema_node`. If we keep the same name as our main `config`.yaml it will validate schema of our `configs` directory. This feature is expected to depreciate due to complexity caused by it, therefore I am keeping my schema and configs different.
   - For more information on it, please visit -> [Hydra Docs](https://hydra.cc/docs/intro/)

6. **MLFLOW Config:**
   First make sure that path exists for the `backend store` and `artifact store`, you provided in your server.
   Second you need to be sure that current_user has read, write and execute permission for this project. Or Else No artifact or track records will be saved programmatically.
   I have added `remove_permission_issues.sh` as reference to solve this issue. Also added a sample local server, which will work exactly like remote server, store and pass artifacts and logs by itself, instead of using local environment for that (however that seems to be costlier than directly, anyways we can change that will change of line of code.).

## <a id="cli-how-to-use-this-template">CLI (How to use this template?):</a>
This part is our objective to create. We can alway add more cli command to create more processes as per our requirements.

   1. `export_aws_secrets`: set credentials set in `./env_files/aws.env` as environment variables. (You can delete this file after setting credentials, it will not affect functionality.)

   2. `make check_configs`: prints our current config defined in hydra `configs` folder, we can change it it `configs` folder. It is always good idea to check configuration before working with this templates. You can alway edit your configuration in `configs` folder.

   3. `make init`: start dvc, git, version dataset and git, add remote and push our code and dataset to git and remote storage.

   4. `make version_dataset`: It tag version to current dataset if there is any change in it and syc it with remote repo.

   5. `make version_code`: It tag version to our code and syc it with remote repo. It will auto increment version of code and push it to repo with tag.

   6. `make push_code_image_on_ecr`: containerize our code and push it on AWS ECR.It will name and tag our container as as per our configuration.
   
   7. `make push_app_image_on_ecr`: containerize our app and push it on AWS ECR.It will name and tag our container as as per our configuration.

   8. `make run_on_ec2`: launches ec2 instance on aws and pull docker container from ecr then run our container.
   It will create new instance as per our configuration and userdata or start old one with new userdata if instance with the same name already exists.It will also create a `key_pair` to ssh into instance if key_pair does not exits and `.gitignore` it. If you have lost old key_pair, Kindly download it manually and `.gitignore` it to make this code work.

   9. `make stop_all_instances`: Will stop all containers in your containers in your aws account, so use it carefully. You can always add or alter code to match your requirements.
   
   10. Other Tools:
      1.  `make write_env_files`:write `requirements.txt` files for `app`, `src` and `code` folder iteratively.
      2.  `make start_local_server`: start local mlflow server which determine backend store and artifact location. This is for local test only.
      3.  `make lint`: lint our code in `code`, `src` and `app` directory and returns errors, only.
      4.  `make score_lint`: returns pylint score
      5.  `make black_format`: format our code with black formatter in `code`, `src` and `app` folder.

**Note:** Commands like `run_on_ec2` and `stop_all_instances` may take time to respond, as they are configured to wait till instances are in `running` or all instances are in `stopped` state. Still It is always good idea to check these on your aws account manually which does not take much effort. Atleast always check status of your command.