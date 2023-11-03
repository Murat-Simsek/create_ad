import os
import torch
from PIL import Image
from diffusers import AutoPipelineForImage2Image


class Hfimg2img():
    def __init__(self) -> None:
        # Check if a GPU is available
        if torch.cuda.is_available():
        # If a GPU is available, move the pipeline to the GPU
            self.pipeline = AutoPipelineForImage2Image.from_pretrained(
            "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, variant="fp16").to("cuda")
        else:
        # If a GPU is not available, keep the pipeline on the CPU
            self.pipeline = AutoPipelineForImage2Image.from_pretrained(
            "runwayml/stable-diffusion-v1-5", variant="fp32").to("cpu")

    def img2img_generate(self, file_path, prompt, hex_color):

        init_image = Image.open(file_path).convert("RGB")

        prompt = prompt + ", theme color " + hex_color  # " A glass cup of coffee, detailed, 8k"

        image = self.pipeline(prompt, image=init_image, guidance_scale=8.0).images[0]
        name_file, ext = os.path.splitext(file_path)
        base_filename = os.path.basename(name_file)
        image.save(os.path.join('received_img', base_filename + "_generated" + ext))
        return "received_img/" + base_filename + "_generated.png"
