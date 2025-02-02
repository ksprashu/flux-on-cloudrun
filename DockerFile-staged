# syntax=docker/dockerfile:1.4

# Stage 1: Install dependencies
FROM nvidia/cuda:12.6.3-base-ubuntu24.04 as dependencies

# Install Python and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3-pip && \
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


# Stage 2: Final image
FROM nvidia/cuda:12.6.3-base-ubuntu24.04

# Install Python to support the virtual environment
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment with dependencies
COPY --from=dependencies /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set cache directory for Hugging Face
ENV HF_HOME=/models

# Copy the application file
WORKDIR /app
COPY app.py .

# Expose the port Streamlit uses
EXPOSE 8080

# Set the Streamlit command to use the Cloud Run port
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

