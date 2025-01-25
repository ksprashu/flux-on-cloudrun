# 0. Pre-download all the models
`HF_TOKEN=$(cat hf_token.txt) HF_HOME=./models/hf-cache python3 download_models.py`

# 1. Build and tag the image

## Enable secrets
`export DOCKER_BUILDKIT=1`

## Typical build
`docker build -t flux-dev-cr .`

## Build for Artifact Registry push
`docker build -t us-central1-docker.pkg.dev/ksp-demos/docker-ai-images/flux-dev-cr:v1 .`

# 2. Create the Artifact Registry repository (if it doesn't exist)
```
gcloud artifacts repositories create docker-ai-images \
    --repository-format=docker \
    --location=us-central1 \
    --description="My Docker AI Images"
```

# 3. Configure Docker for authentication
`gcloud auth configure-docker us-central1-docker.pkg.dev`

# 4. Push the image
`docker push us-central1-docker.pkg.dev/ksp-demos/docker-ai-images/flux-dev-cr:v1`

# 5. Deploy to Cloud Run
```
gcloud beta run deploy flux-dev-cr \
  --image us-central1-docker.pkg.dev/ksp-demos/docker-ai-images/flux-dev-cr:v1 \
  --region=us-central1 \
  --cpu 8 \
  --memory 32Gi \
  --no-cpu-throttling \
  --gpu 1 \
  --gpu-type nvidia-l4 \
  --max-instances 1 \
  --allow-unauthenticated \
  --port=8080
```






## Docker Build
docker build -t flux-dev-cr .

docker build --secret id=hf_token,src=hf_token.txt . -t your_image_name

docker build --secret id=hf_token,src=hf_token.txt -t REGION-docker.pkg.dev/YOUR_PROJECT_ID/REPOSITORY_NAME/IMAGE_NAME:TAG .

docker build --secret id=hf_token,src=hf_token.txt -t us-central1-docker.pkg.dev/ksp-sandbox/docker-ai-images/flux-dev-cr:v1 .

## Push to Artifact Registry
docker push REGION-docker.pkg.dev/YOUR_PROJECT_ID/REPOSITORY_NAME/IMAGE_NAME:TAG

docker push us-central1-docker.pkg.dev/ksp-sandbox/docker-ai-images/flux-dev-cr:v1

## Deploy to Cloud Run
gcloud beta run deploy flux-dev-cr \
  --image us-central1-docker.pkg.dev/ksp-sandbox/docker-ai-images/flux-dev-cr:v1 \
  --region=us-central1 \
  --cpu 8 \
  --memory 32Gi \
  --no-cpu-throttling \
  --gpu 1 \
  --gpu-type nvidia-l4 \
  --max-instances 1 \
  --allow-unauthenticated \
  --port=8501

