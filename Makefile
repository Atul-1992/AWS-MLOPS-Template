# ENV_FILE := env_files/aws.env

# include $(ENV_FILE)

# export_aws_secrets:
# 	@echo "Exporting AWS credentials..."
# 	@export AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID); \
# 	export AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY); \
# 	export AWS_DEFAULT_REGION=$(AWS_DEFAULT_REGION); \
# 	echo "AWS credentials exported successfully."

check_configs:
	python ./src/check_configs.py

init:
	python ./src/init.py

push_server_image_on_ecr:
	python ./src/push_server_image.py

push_trainer_image_on_ecr:
	python ./src/push_trainer_image.py

push_app_image_on_ecr:
	python ./src/push_app_image.py

push_all_images_on_ecr:
	python ./src/push_server_image.py;
	python ./src/push_trainer_image.py;
	python ./src/push_app_image.py;

create_server_instance:
	python ./src/create_server_instance.py

create_trainer_instance:
	python ./src/create_trainer_instance.py

create_app_instance:
	python ./src/create_app_instance.py

create_all_instances:
	python ./src/create_server_instance.py;
	python ./src/create_trainer_instance.py;
	python ./src/create_app_instance.py;

pull_server_image_in_ec2:
	python ./src/pull_server_image_in_ec2.py
	
pull_trainer_image_in_ec2:
	python ./src/pull_trainer_image_in_ec2.py
	
pull_app_image_in_ec2:
	python ./src/pull_app_image_in_ec2.py

pull_all_images_in_ec2s:
	python ./src/pull_server_image_in_ec2.py;
	python ./src/pull_trainer_image_in_ec2.py;
	python ./src/pull_app_image_in_ec2.py;

stop_all_instances:
	python ./src/stop_all_instances.py

version_code:
	python ./src/version_code.py

version_dataset:
	python ./src/version_dataset.py

ssh_instance:
	ssh -i my-key-pair.pem ec2-user@<public_ip>

start_local_server:
	mlflow server --backend-store-uri \
	sqlite:///$(PWD)/demo_sqlite_db/mlflow.db \
	--artifacts-destination file:$(PWD)/demo_aritifact_store/ \
	--host localhost \
	--port 5000

write_env_files:
	pipreqs --savepath ./src/requirements.txt ./src/;
	pipreqs --savepath ./code/requirements.txt ./code/;
	pipreqs --savepath ./app/requirements.txt ./app/

black_format:
	black ./src/ ./code/ ./app/

isort:
	isort ./src/ ./code/ ./app/

lint:
	# pylint ./src/ ./code/ ./app/ | tail -n 2 | head -n 1
	pylint ./src/ ./code/ ./app/ --errors-only --disable E1120

lint_score:
	pylint ./src/ ./code/ ./app/ | tail -n 2 | head -n 1