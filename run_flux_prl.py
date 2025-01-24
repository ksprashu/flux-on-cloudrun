from diffusers import FluxTransformer2DModel, FluxPipeline, BitsAndBytesConfig
from transformers import T5EncoderModel, BitsAndBytesConfig as TBnBConfig
import argparse
import random
import numpy as np
import torch 
from torch.nn import DataParallel

if not torch.cuda.is_available():
    raise ValueError("Need a CUDA GPU.")

MODEL_ID = "black-forest-labs/FLUX.1-dev"
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

    # Use DataParallel to distribute work across all available GPUs
    if torch.cuda.device_count() > 1:
        print(f"Using {torch.cuda.device_count()} GPUs for parallel inference")
        pipeline = DataParallel(pipeline)
            
    return pipeline 


def split_workload_and_generate(pipeline, prompt, num_gpus, **kwargs):
    # Split the prompts across available GPUs
    device_prompts = [
        (f"cuda:{i}", prompt) for i in range(num_gpus)
    ]

    # Process each prompt on its assigned GPU
    images = []
    for device, prompt in device_prompts:
        pipeline.to(device)  # Move pipeline to the assigned device
        image = pipeline(prompt, **kwargs).images[0]
        images.append(image)

    return images


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, default="a tiny astronaut hatching from an egg on the moon")
    parser.add_argument("--num_inference_steps", type=int, default=30)
    parser.add_argument("--guidance_scale", type=float, default=3.5)
    parser.add_argument("--resolution", type=str, default="1024x1024", help="{heightxwidth}")
    parser.add_argument("--seed", type=int, default=2025)
    parser.add_argument("--out_path", type=str, default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    pipeline = load_pipeline()

    # Number of available GPUs
    num_gpus = torch.cuda.device_count()
    print(f"Using {num_gpus} GPUs for parallel inference")

    height, width = args.resolution.split("x")
    kwargs = {
        "num_inference_steps": args.num_inference_steps,  # the more of this, the more the inference latency
        "height": height,
        "width": width,
        "guidance_scale": args.guidance_scale, # controls how much the image respects the prompt.
        "max_sequence_length": 512,
        "generator": torch.manual_seed(args.seed), # for reproducibility
    }    
    # image = pipeline(
    #     args.prompt,
    #     num_inference_steps=args.num_inference_steps, # the more of this, the more the inference latency
    #     height=float(height),
    #     width=float(width),
    #     guidance_scale=args.guidance_scale, # controls how much the image respects the prompt.
    #     max_sequence_length=512,
    #     generator=torch.manual_seed(args.seed), # for reproducibility.
    # ).images[0]

    images = split_workload_and_generate(pipeline, args.prompt, num_gpus, **kwargs)
    
    if args.out_path is None:
        args.out_path = str(random.randint(0, MAX_SEED)) + ".png"

    image.save(args.out_path)
    print(f"Image serialized to {args.out_path}.")

    