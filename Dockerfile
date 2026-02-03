# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Metadata
LABEL maintainer="Vadik Goel <vadikgoel1@gmail.com>"
LABEL version="2.0.2"
LABEL description="Official container for Easypy Language v2.0"

# Set the working directory directly to /app
WORKDIR /app

# Install system dependencies if needed (e.g. for Tkinter GUI support in headless envs)
# standard python-tk might be needed for the GUI module
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
# We don't have a requirements.txt in the root checked into git usually? 
# But we just created one in the previous turn!
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install the package itself in editable mode or standard mode
RUN pip install .

# Set the default command to run the Easypy CLI
# This means 'docker run easypy-lang' will act like the 'easypy' command
ENTRYPOINT ["easypy"]
CMD ["--help"]
