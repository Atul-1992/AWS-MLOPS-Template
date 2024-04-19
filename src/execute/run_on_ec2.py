# ./src/execute/run_on_ec2.py
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

sys.path.append(project_root)
from src.execute.ActSetup import processes

image_id = 'ami-001843b876406202a'
instance_type = 't2.micro'
ingress_rules = [
			{
				'IpProtocol': 'tcp',
				'FromPort': 22,
				'ToPort': 22,
				'IpRanges': [{'CidrIp': '0.0.0.0/0'}],  # Allow SSH from anywhere
			}
]
userdata_script = '''#!/bin/bash
	yum update -y
	yum install -y httpd
	systemctl start httpd
	systemctl enable httpd
	echo "<html><body><h1>Welcome to My Website</h1></body></html>" > /var/www/html/index.html
	'''


if __name__=='__main__':
	processes.create_instance(image_id=image_id, instance_type=instance_type, ingress_rules=ingress_rules, userdata_script=userdata_script)