# backend/services/vlm_client.py

import json
import base64
import asyncio
from typing import Any, Dict

import requests
import httpx
from fastapi import UploadFile
from google import genai

from config.settings import settings


# ============================================================
# 🔹 BRIA API
# ============================================================

BRIA_BASE_URL = "https://engine.prod.bria-api.com/v2"
BRIA_GENERATE_URL = f"{BRIA_BASE_URL}/image/generate"


def _bria_headers():
    return {
        "Content-Type": "application/json",
        "api_token": settings.BRIA_API_KEY
    }


# ============================================================
# 🔹 1. GEMINI — Prompt → JSON
# ============================================================

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


def prompt_to_json(prompt: str):
    """Convert natural language → JSON using Gemini."""

    system_prompt = """
    You MUST output a valid Bria V2 structured_prompt JSON.

    EXACT REQUIRED SCHEMA:

    {
      "short_description": "string",
      "objects": [
        {
          "description": "string",
          "location": "string",
          "relationship": "string",
          "relative_size": "string",
          "shape_and_color": "string",
          "texture": "string",
          "appearance_details": "string",
          "orientation": "string"
        }
      ],
      "background_setting": "string",
      "lighting": {
        "conditions": "string",
        "direction": "string",
        "shadows": "string"
      },
      "aesthetics": {
        "composition": "string",
        "color_scheme": "string",
        "mood_atmosphere": "string",
        "preference_score": "very high",
        "aesthetic_score": "very high"
      },
      "photographic_characteristics": {
        "depth_of_field": "string",
        "focus": "string",
        "camera_angle": "string",
        "lens_focal_length": "string"
      },
      "style_medium": "photograph",
      "context": "string",
      "artistic_style": "realistic, detailed"
    }

    RULES:
    - Return ONLY JSON.
    - No markdown.
    - No backticks.
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt + "\n\nUser prompt:\n" + prompt}
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

    # Clean for JSON
    cleaned = text.strip().replace("```json", "").replace("```", "")

    return json.loads(cleaned)


# ============================================================
# 🔹 2. GEMINI — Image → JSON
# ============================================================

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def image_to_json(image: UploadFile):
    img_bytes = image.file.read()
    b64 = base64.b64encode(img_bytes).decode("utf-8")

    response = client.models.generate_content(
        model="models/gemini-2.0-flash-exp-image-generation",
        contents=[
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": image.content_type,
                            "data": b64
                        }
                    },
                    {
                        "text": (
                            "Analyze this image and output a COMPLETE Bria structured_prompt JSON. "
                            "Return ONLY valid JSON. No markdown."
                        )
                    }
                ]
            }
        ]
    )

    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)




# ============================================================
# 🔹 3. BRIA — JSON → IMAGE (Async)
# ============================================================

async def generate_image_and_wait(json_body, timeout_seconds=60, max_polls=12):
    """
    Uses Bria V2 async image generation.
    Polls until image is ready.
    """

    async with httpx.AsyncClient(timeout=30) as client:

        # Step 1 — send request
        resp = await client.post(
            BRIA_GENERATE_URL,
            json=json_body,
            headers=_bria_headers()
        )

        if resp.status_code not in [200, 202]:
            raise Exception(f"Generation failed: {resp.text}")

        data = resp.json()

        # Sync result returned instantly
        if resp.status_code == 200 and "result" in data:
            return {
                "image_url": data["result"]["image_url"],
                "request_id": data.get("request_id"),
                "metadata": data["result"]
            }

        # Async flow
        status_url = data.get("status_url")
        request_id = data.get("request_id")

        if not status_url:
            raise Exception("No status_url in async Bria response")

        # Poll
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

            if status == "ERROR":
                raise Exception(poll_data.get("error"))

        raise TimeoutError("Image generation took too long")
