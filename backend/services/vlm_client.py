# backend/services/vlm_client.py
import requests
from config.settings import settings

# BRIA API endpoints
BRIA_PROMPT_TO_JSON_URL = "https://api.bria.ai/v1/image/prompt-to-json"
print("🔗 BRIA URL LOADED:", BRIA_PROMPT_TO_JSON_URL)

  
BRIA_IMAGE_TO_JSON_URL  = "https://api.bria.ai/v1/image-to-json"

def prompt_to_json(prompt: str):
    """Convert short text prompt -> detailed JSON using BRIA VLM."""
    headers = {
        "Authorization": f"Bearer {settings.BRIA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {"prompt": prompt}

    res = requests.post(BRIA_PROMPT_TO_JSON_URL, json=payload, headers=headers)

    if res.status_code != 200:
        print("🔥 BRIA PROMPT-TO-JSON ERROR:", res.status_code, res.text)
        raise Exception("BRIA prompt-to-json failed")

    return res.json().get("json_prompt")


def image_to_json(image_file):
    """Convert uploaded image -> JSON description using BRIA Inspire."""
    headers = {"Authorization": f"Bearer {settings.BRIA_API_KEY}"}

    files = {
        "image": (image_file.filename, image_file.file, image_file.content_type)
    }

    res = requests.post(BRIA_IMAGE_TO_JSON_URL, files=files, headers=headers)

    if res.status_code != 200:
        print("🔥 BRIA IMAGE-TO-JSON ERROR:", res.status_code, res.text)
        raise Exception("BRIA image-to-json failed")

    return res.json().get("json_prompt")
