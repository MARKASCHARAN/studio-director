# backend/services/vlm_client.py
import json
import requests
import asyncio
from typing import Any, Dict
import httpx

from config.settings import settings


BRIA_BASE_URL = "https://engine.prod.bria-api.com/v2"
BRIA_GENERATE_URL = f"{BRIA_BASE_URL}/image/generate"
BRIA_STATUS_URL = f"{BRIA_BASE_URL}/status"
BRIA_STRUCTURED_URL = f"{BRIA_BASE_URL}/structured_prompt/generate"


# ============================================================
# 🔹 1. GEMINI — Prompt → JSON
# ============================================================

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

def prompt_to_json(prompt: str):
    """Convert natural language → JSON using Gemini 2.5 Flash (REST API)."""

    system_prompt = """
    Convert the input into a structured JSON visual scene description.

    The JSON must include:
    - scene.description
    - camera.angle
    - camera.fov
    - lighting.type
    - lighting.intensity
    - color_palette.primary
    - color_palette.secondary

    Return ONLY valid JSON. No markdown or explanations.
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt + "\n\nUser prompt: " + prompt}
                ]
            }
        ]
    }

    headers = {
        "x-goog-api-key": settings.GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(GEMINI_URL, headers=headers, json=payload)

    if res.status_code != 200:
        print("Gemini ERROR:", res.status_code, res.text)
        raise Exception("Gemini request failed")

    text = res.json()["candidates"][0]["content"]["parts"][0]["text"]

    cleaned = text.strip().replace("```json", "").replace("```", "")

    return json.loads(cleaned)



# ============================================================
# 🔹 2. BRIA — Image → JSON
# ============================================================

BRIA_IMAGE_TO_JSON_URL = "https://ai.bria.ai/v2/image/to-json"

def image_to_json(image_file):
    """Upload an image → return JSON scene using BRIA."""

    headers = {
        "api_token": settings.BRIA_API_KEY
    }

    files = {
        "image": (image_file.filename, image_file.file, image_file.content_type)
    }

    res = requests.post(BRIA_IMAGE_TO_JSON_URL, files=files, headers=headers)

    if res.status_code != 200:
        print("🔥 BRIA IMAGE-TO-JSON ERROR:", res.status_code, res.text)
        raise Exception("BRIA image-to-json failed")

    data = res.json()

    if "result" in data and "json_prompt" in data["result"]:
        return data["result"]["json_prompt"]

    print("Unexpected format:", data)
    return None



# ============================================================
# 🔹 3. BRIA — JSON → IMAGE  (Async generate)
# ============================================================

def _bria_headers():
    return {
        "Content-Type": "application/json",
        "api_token": settings.BRIA_API_KEY
    }


async def generate_image_and_wait(json_body, timeout_seconds=60, max_polls=12):
    """
    Uses async V2 image generation.
    Automatically polls the /status/{request_id} endpoint until image is ready.
    """

    async with httpx.AsyncClient(timeout=30) as client:
        
        # Step 1: Send the request (async by default)
        resp = await client.post(
            BRIA_GENERATE_URL,
            json=json_body,
            headers=_bria_headers()
        )

        if resp.status_code not in [200, 202]:
            raise Exception(f"Generation failed: {resp.text}")

        data = resp.json()

        # If sync=true and result returned immediately
        if resp.status_code == 200 and "result" in data:
            return {
                "image_url": data["result"]["image_url"],
                "request_id": data.get("request_id"),
                "metadata": data["result"]
            }

        # Step 2: async flow → extract status_url
        status_url = data.get("status_url")
        request_id = data.get("request_id")

        if not status_url:
            raise Exception("Missing status_url in async response")

        # Step 3: Poll the status service
        for _ in range(max_polls):
            await asyncio.sleep(timeout_seconds / max_polls)

            poll = await client.get(status_url, headers=_bria_headers())
            poll_data = poll.json()

            status = poll_data.get("status")

            if status == "COMPLETED":
                result = poll_data.get("result")
                return {
                    "image_url": result["image_url"],
                    "request_id": request_id,
                    "metadata": result
                }

            elif status == "ERROR":
                raise Exception(poll_data.get("error", {}))

        raise TimeoutError("Image generation took too long")