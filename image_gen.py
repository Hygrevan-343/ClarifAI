from krutrim_cloud import KrutrimCloud
from dotenv import load_dotenv
from krutrim_cloud.lib.utils import convert_base64_to_PIL_img, convert_base64_to_OpenCV_img
import os

load_dotenv()
client = KrutrimCloud()

def generate_image (img_prompt, index):
    print(img_prompt)
    try:
        stable_diffusion_response = client.images.generations.diffusion(
            model_name="diffusion1XL",
            image_height=1024,
            image_width=1024,
            prompt=img_prompt
        )
        
        print(f"Number of Images created: {stable_diffusion_response.created}")
        print(f"Error: {stable_diffusion_response.error}")

        output_dir = "./static/output"
        os.makedirs(output_dir, exist_ok=True)

        if stable_diffusion_response.data:
            image = stable_diffusion_response.data[0]
            PIL_img = convert_base64_to_PIL_img(image["b64_json"])
            filename = f"image-{index}.png"
            filepath = os.path.join(output_dir, filename)
            PIL_img.save(filepath)
            print(f"Image saved as {filename}")

    except Exception as exc:
        print(f"Exception: {exc}")
