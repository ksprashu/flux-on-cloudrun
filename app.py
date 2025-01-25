# A streamlit app that takes a user prompt, some parameters and generates an image

from diffusers import FluxTransformer2DModel, FluxPipeline, BitsAndBytesConfig
from transformers import T5EncoderModel, BitsAndBytesConfig as TBnBConfig
import argparse
import random
import numpy as np
import torch 

if not torch.cuda.is_available():
    raise ValueError("Need a CUDA GPU.")

MODEL_ID = "black-forest-labs/FLUX.1-schnell"
MAX_SEED = np.iinfo(np.int32).max

def load_pipeline():
    transformer_config = BitsAndBytesConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16
    )
    transformer = FluxTransformer2DModel.from_pretrained(
        MODEL_ID, subfolder="transformer", quantization_config=transformer_config, torch_dtype=torch.bfloat16
    )

    text_encoder_2_config = TBnBConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16
    )
    text_encoder_2 = T5EncoderModel.from_pretrained(
        MODEL_ID, subfolder="text_encoder_2", 
        quantization_config=text_encoder_2_config, torch_dtype=torch.bfloat16
    )
    pipeline = FluxPipeline.from_pretrained(
        MODEL_ID, transformer=transformer, text_encoder_2=text_encoder_2, torch_dtype=torch.bfloat16
    ).to("cuda")
    return pipeline 


# create a new empty streamlit app
import streamlit as st

pipeline = load_pipeline()

st.title("Image Generation App")

prompt = st.text_input("Enter your prompt:", "A photo of an astronaut riding a horse on mars")
resolution = st.slider("Resolution", min_value=256, max_value=1024, value=512)
num_inference_steps = st.slider("Number of inference steps", min_value=1, max_value=20, value=4)
# guidance_scale = st.slider("Guidance scale", min_value=1.0, max_value=20.0, value=3.5)
seed = st.number_input("Seed (leave blank for random)", value=None, step=1)


if seed is None:
    seed = random.randint(0, MAX_SEED)    

if st.button("Generate Image"):
    with st.spinner("Generating..."):
        generator = torch.Generator("cuda").manual_seed(seed)
        image = pipeline(
            prompt,
            num_inference_steps=num_inference_steps,
            # guidance_scale=guidance_scale,
            height=resolution,
            width=resolution,
            max_sequence_length=256,
            generator=generator
        ).images[0]
        st.image(image)
        st.write('Done')
