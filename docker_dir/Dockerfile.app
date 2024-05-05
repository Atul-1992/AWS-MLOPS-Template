FROM python:3.12-slim

# Copy the application code into the image
COPY ./app /app

# Set the working directory
WORKDIR /app

# Set up a virtual environment and install dependencies
RUN python3 -m venv .venv && \
    .venv/bin/pip install -r /app/requirements.txt --no-cache-dir

# Set the entrypoint to use the Python interpreter from the virtual environment
ENTRYPOINT [ ".venv/bin/python3" ]
