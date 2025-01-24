# 1. Build and tag the image

## Enable secrets
`export DOCKER_BUILDKIT=1`

## Typical build
`docker build -t flux-dev-cr .`

## Build with secrets
`docker build --secret id=hf_token,src=hf_token.txt -t REGION-docker.pkg.dev/YOUR_PROJECT_ID/REPOSITORY_NAME/IMAGE_NAME:TAG .`

`docker build --secret id=hf_token,src=hf_token.txt -t us-central1-docker.pkg.dev/my-gcp-project/my-docker-repo/my-streamlit-app:v1 .`

# 2. Create the Artifact Registry repository (if it doesn't exist)
```
gcloud artifacts repositories create my-docker-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="My Docker repository"
```

# 3. Configure Docker for authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# 4. Push the image
docker push REGION-docker.pkg.dev/YOUR_PROJECT_ID/REPOSITORY_NAME/IMAGE_NAME:TAG

docker push us-central1-docker.pkg.dev/my-gcp-project/my-docker-repo/my-streamlit-app:v1

# 5. Deploy to Cloud Run
gcloud run deploy my-streamlit-service \
    --image=us-central1-docker.pkg.dev/my-gcp-project/my-docker-repo/my-streamlit-app:v1 \
    --region=us-central1 \
    --set-env-vars="HUGGINGFACE_API_KEY=your_api_key" \
    --allow-unauthenticated \
    --port=8501 \
    --memory=1Gi \
    --cpu=1





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

