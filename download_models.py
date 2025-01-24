from diffusers import FluxTransformer2DModel, FluxPipeline, BitsAndBytesConfig
from transformers import T5EncoderModel, BitsAndBytesConfig as TBnBConfig
import torch

MODEL_ID = "black-forest-labs/FLUX.1-dev"

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
