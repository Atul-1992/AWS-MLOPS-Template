# ENV_FILE := env_files/aws.env

# include $(ENV_FILE)
# export

# export_aws_secrets:
# 	@echo "Exporting AWS credentials..."
# 	@set AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID); \
# 	@set AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY); \
# 	@set AWS_DEFAULT_REGION=$(AWS_DEFAULT_REGION); \
# 	@echo "AWS credentials exported successfully.

init:
	python ./src/execute/init.py

push_on_ecr:
	python ./src/execute/push_docker_image.py

run_on_ec2:
	python ./src/execute/run_on_ec2.py

version_dataset:
	python ./src/execute/version_dataset.py

version_code:
	python ./src/execute/version_code.py

stop_all_instances:
	python ./src/execute/stop_all_instances.py

check_configs:
	python ./src/execute/check_configs.py
