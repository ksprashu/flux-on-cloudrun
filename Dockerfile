# syntax=docker/dockerfile:1.4

# Use NVIDIA CUDA base image with Ubuntu 24.04
FROM nvidia/cuda:12.6.3-base-ubuntu24.04

# Install Python and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the HF cache directory and set permissions
# RUN mkdir -p /models/hf-cache && chmod -R 777 /models    

# Copy the pre-downloaded models
# COPY ./models /models

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Set Env vars and cache directory for Hugging Face
ENV PATH="/opt/venv/bin:$PATH"
ENV APP_DIR=/app
ENV HF_HOME=/models/hf-cache

# Set the working directory
WORKDIR $APP_DIR

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the download script
# COPY download_models.py .

# Download the model using Hugging Face token (secret during build)
# RUN --mount=type=secret,id=hf_token \
#     HF_TOKEN=$(cat /run/secrets/hf_token) python3 download_models.py

# Copy the application file as the last layer
COPY app.py .

# Expose the port Streamlit uses
EXPOSE 8080

# Set the Streamlit command to use the Cloud Run port
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

