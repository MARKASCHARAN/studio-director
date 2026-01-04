# backend/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import traceback
import json

from config.settings import settings

# Import VLM / BRIA tools
from services.vlm_client import (
    prompt_to_json,
    image_bytes_to_json,
    generate_image_and_wait,
    client
)

from services.agent_service import (
    generate_shot_json,
    auto_fix_json
)

# ---------------------------------------------------------
# FASTAPI SETUP
# ---------------------------------------------------------
app = FastAPI(title="StudioDirector API", version="1.0.0")


# ---------------------------------------------------------
# SCHEMAS
# ---------------------------------------------------------
class TranslateRequest(BaseModel):
    prompt: str


class TranslateResponse(BaseModel):
    result: Dict[str, Any]


class GenerateRequest(BaseModel):
    structured_json: Dict[str, Any]   # renamed from json → avoids warnings


class GenerateResponse(BaseModel):
    image_url: str
    json: Dict[str, Any]
    request_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RefineRequest(BaseModel):
    structured_json: Dict[str, Any]
    instruction: str


class RefineResponse(BaseModel):
    image_url: str
    json: Dict[str, Any]


class InspireResponse(BaseModel):
    image_url: str
    json: Dict[str, Any]


class MultiShotRequest(BaseModel):
    shot_types: List[str]


class MultiShotItem(BaseModel):
    type: str
    image_url: str
    json: Dict[str, Any]


class MultiShotResponse(BaseModel):
    shots: List[MultiShotItem]


# ---------------------------------------------------------
# BASIC HEALTH
# ---------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/test-key")
def test_key():
    return {
        "bria_key_loaded": bool(settings.BRIA_API_KEY),
        "gemini_key_loaded": bool(settings.GEMINI_API_KEY),
    }


# ---------------------------------------------------------
# 1️⃣ TRANSLATE — Prompt → JSON
# ---------------------------------------------------------
@app.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    try:
        raw_json = prompt_to_json(req.prompt)  # Gemini conversion
        fixed = auto_fix_json(raw_json)
        return {"result": fixed}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, str(e))


# ---------------------------------------------------------
# 2️⃣ GENERATE — Structured JSON → Image
# ---------------------------------------------------------
@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    try:
        if not req.structured_json:
            raise HTTPException(422, "structured_json is required.")

        fixed_json = auto_fix_json(req.structured_json)

        structured_prompt = json.dumps(fixed_json, ensure_ascii=False)

        print("\n--- BRIA STRUCTURED PROMPT ---")
        print(structured_prompt)
        print("--------------------------------\n")

        result = await generate_image_and_wait({
            "structured_prompt": structured_prompt
        })

        return {
            "image_url": result["image_url"],
            "json": fixed_json,
            "request_id": result.get("request_id"),
            "metadata": result.get("metadata")
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, str(e))


# ---------------------------------------------------------
# 3️⃣ REFINE — Modify JSON → New Image
# ---------------------------------------------------------
@app.post("/refine", response_model=RefineResponse)
async def refine(req: RefineRequest):
    try:
        refined = req.structured_json.copy()
        refined["refinement_instruction"] = req.instruction

        fixed = auto_fix_json(refined)

        result = await generate_image_and_wait({
            "structured_prompt": json.dumps(fixed)
        })

        return {"image_url": result["image_url"], "json": fixed}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, str(e))


# ---------------------------------------------------------
# 4️⃣ INSPIRE — Image → JSON → New Image
# ---------------------------------------------------------
@app.post("/inspire", response_model=InspireResponse)
async def inspire(image: UploadFile = File(...)):
    try:
        img_bytes = await image.read()
        extracted = image_bytes_to_json(img_bytes, mime_type=image.content_type)

        fixed = auto_fix_json(extracted)

        result = await generate_image_and_wait({
            "structured_prompt": json.dumps(fixed)
        })

        return {"image_url": result["image_url"], "json": fixed}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, str(e))


# ---------------------------------------------------------
# 5️⃣ MULTI-SHOT — Generate multiple shots
# ---------------------------------------------------------
@app.post("/multi-shot", response_model=MultiShotResponse)
async def multi_shot(
    image: UploadFile = File(...),
    shot_types_json: Optional[str] = Form(None)
):
    try:
        img_bytes = await image.read()
        base_json = image_bytes_to_json(img_bytes, mime_type=image.content_type)

        if shot_types_json:
            shot_types = json.loads(shot_types_json)
        else:
            shot_types = ["establishing", "medium", "hero", "closeup"]

        shots_output = []

        for shot in shot_types:
            shot_json = generate_shot_json(base_json, shot)
            fixed = auto_fix_json(shot_json)

            result = await generate_image_and_wait({
                "structured_prompt": json.dumps(fixed)
            })

            shots_output.append({
                "type": shot,
                "image_url": result["image_url"],
                "json": fixed
            })

        return {"shots": shots_output}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, str(e))


# ---------------------------------------------------------
# 6️⃣ LIST GEMINI MODELS
# ---------------------------------------------------------
@app.get("/list-models")
def list_models():
    try:
        if hasattr(client, "models") and hasattr(client.models, "list"):
            return {"models": client.models.list()}
        return {"models": []}
    except Exception as e:
        return {"error": str(e)}
