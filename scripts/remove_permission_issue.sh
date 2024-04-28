#!/bin/bash

# this script is to be run manually, it is written for reference only!
# Get the parent directory of the current working directory
parent_dir=$(dirname $(pwd))

# Change ownership recursively to the current user and group
sudo chown -R USER:$GROUP "$parent_dir"
