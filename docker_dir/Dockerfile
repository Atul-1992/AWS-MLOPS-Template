# Use Python 3.8 slim image as the base
FROM python:3.8-slim

# Update package lists and install Bash
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /src

# Copy application files into the container
COPY . /src

# Set Bash as the entry point
ENTRYPOINT ["/bin/bash"]
# docker build -t remove_me:v01 -f ./docker_dir/Dockerfile . (use to build from root folder, dont change context)