import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

sys.path.append(project_root)
from src.execute.ActSetup import processes

if __name__=='__main__':
	processes.version_dataset()