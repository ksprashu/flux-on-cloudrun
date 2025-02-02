# syntax=docker/dockerfile:1.4

# Step 1: Setup base linux image and install python dependencies
FROM nvidia/cuda:12.6.3-base-ubuntu24.04 as image

# Install Python and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3-pip gcsfuse fuse && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Step 2: Download model images

# Copy the Python script into the container
COPY download_models.py .

# Set cache directory for Hugging Face
RUN mkdir /mount
ENV HF_HOME=/models

# Use Docker BuildKit to securely pass the secret from hf_token.txt
RUN --mount=type=secret,id=hf_token \
    export HF_TOKEN=$(cat /run/secrets/hf_token) && \
    python download_models.py

# Step 3: Run the application

# Copy the application file
COPY app.py .

# Expose the port Streamlit uses
EXPOSE 8080

# Set the Streamlit command to use the Cloud Run port
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

