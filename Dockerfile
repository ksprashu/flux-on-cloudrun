# syntax=docker/dockerfile:1.4  # Use the latest syntax

# Choose a suitable base image
FROM python:3.12-slim

# Update apt package lists
RUN apt-get update

# Upgrade existing packages
RUN apt-get upgrade -y 

# Upgrade pip
RUN pip install --upgrade pip

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your model code and any necessary files
COPY . .

# Set the HF access token via args
# ARG HF_TOKEN="none"

# Download the Hugging Face model (using an access token if needed)
# RUN python -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='black-forest-labs/FLUX.1-dev', filename='model_index.json', token='$HF_TOKEN')"
RUN --mount=type=secret,id=hf_token,target=/run/secrets/hf_token \
    python -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='black-forest-labs/FLUX.1-dev', filename='model_index.json', token=open('/run/secrets/hf_token').read().strip())"
    
# Expose the port Streamlit uses
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
