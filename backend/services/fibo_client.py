# backend/services/fibo_client.py
import requests
from config.settings import settings

BRIA_FIBO_URL = "https://api.bria.ai/v1/image/generate"

def generate_image(json_prompt: dict):
    """Generate an image using BRIA FIBO model."""
    headers = {
        "Authorization": f"Bearer {settings.BRIA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "json_prompt": json_prompt,
        "num_inference_steps": 30,
        "guidance_scale": 5,
        "aspect_ratio": "16:9"
    }

    res = requests.post(BRIA_FIBO_URL, json=payload, headers=headers)

    if res.status_code != 200:
        raise Exception(f"BRIA FIBO error: {res.text}")

    data = res.json()
    return {
        "image_url": data["image_url"],
        "json_prompt": data["json_prompt"]
    }
