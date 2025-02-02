from diffusers import FluxTransformer2DModel, FluxPipeline, BitsAndBytesConfig
from transformers import T5EncoderModel, BitsAndBytesConfig as TBnBConfig
import torch
from google.cloud import storage
import os

MODEL_ID = "black-forest-labs/FLUX.1-dev"


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def download_models():
    # Download transformer
    transformer_config = BitsAndBytesConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16
    )
    FluxTransformer2DModel.from_pretrained(
        MODEL_ID, subfolder="transformer", 
        quantization_config=transformer_config, 
        torch_dtype=torch.bfloat16
    )

    # Download text encoder 2
    text_encoder_2_config = TBnBConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16
    )
    T5EncoderModel.from_pretrained(
        MODEL_ID, subfolder="text_encoder_2", 
        quantization_config=text_encoder_2_config, 
        torch_dtype=torch.bfloat16
    )

    # Download pipeline
    FluxPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16
    )
    print("Model and pipeline downloaded successfully.")

if __name__ == "__main__":
    if not torch.cuda.is_available():
        raise ValueError("CUDA GPU is required for model download.")
    download_models()

    # upload all the files downloaded to /models to GCS
    bucket_name = 'flux-dev-cr-models'
    local_file_path = '/mount'
    destination_blob_name = '.'
