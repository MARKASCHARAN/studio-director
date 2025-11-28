# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import traceback
import json   # ✅ FIXED – needed for json.dumps
from services.vlm_client import client


from config.settings import settings
from services.vlm_client import (
    prompt_to_json,
    image_to_json,
    generate_image_and_wait     # async BRIA generator
)


app = FastAPI(title="Studio-Director API", version="0.1.0")


# ============================================================
# 🔹 SCHEMAS
# ============================================================

class TranslateRequest(BaseModel):
    prompt: str

class TranslateResponse(BaseModel):
    json: Dict[str, Any]


class GenerateRequest(BaseModel):
    json: Dict[str, Any]


class GenerateResponse(BaseModel):
    image_url: str
    json: Dict[str, Any]
    request_id: str | None = None
    metadata: Dict[str, Any] | None = None


class RefineRequest(BaseModel):
    json: Dict[str, Any]
    instruction: str

class RefineResponse(BaseModel):
    image_url: str
    json: Dict[str, Any]


class InspireResponse(BaseModel):
    image_url: str
    json: Dict[str, Any]


# ============================================================
# 🔹 ENV TEST
# ============================================================

@app.get("/test-key")
def test_key():
    return {
        "env": settings.ENV,
        "bria_key_loaded": bool(settings.BRIA_API_KEY),
        "gemini_key_loaded": bool(settings.GEMINI_API_KEY),
    }


# ============================================================
# 🔹 ENDPOINTS
# ============================================================

# 1) Prompt → JSON
@app.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    json_prompt = prompt_to_json(req.prompt)
    return {"json": json_prompt}


# 2) JSON → IMAGE (BRIA V2)
@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    try:
        # Convert pydantic input to Python dict
        payload = req.model_dump(exclude_none=True)

        # Convert "json": {...} to structured_prompt string
        if "json" in payload:
            payload["structured_prompt"] = json.dumps(payload["json"])
            del payload["json"]

        # Bria requires exactly one of these:
        if not any(k in payload for k in ["prompt", "images", "structured_prompt"]):
            raise HTTPException(
                status_code=422,
                detail="Either prompt, images, or structured_prompt must be provided."
            )

        # Run async generator
        result = await generate_image_and_wait(payload)

        return {
            "image_url": result["image_url"],
            "json": payload,             # return final structured prompt
            "request_id": result["request_id"],
            "metadata": result["metadata"]
        }

    except TimeoutError as te:
        raise HTTPException(status_code=504, detail=str(te))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# 3) REFINE JSON → IMAGE
@app.post("/refine", response_model=RefineResponse)
async def refine(req: RefineRequest):

    refined_json = req.json.copy()
    refined_json["refinement_instruction"] = req.instruction

    try:
        result = await generate_image_and_wait({
            "structured_prompt": json.dumps(refined_json)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "image_url": result["image_url"],
        "json": refined_json
    }


# 4) INSPIRE FLOW
@app.post("/inspire", summary="Image → JSON → Image", response_model=InspireResponse)
async def inspire(image: UploadFile = File(...)):

    try:
        # Step 1: Convert Image → JSON dict
        json_prompt = image_to_json(image)

        # Step 2: Convert dict → STRING (Bria requires string!)
        structured_prompt_str = json.dumps(json_prompt, ensure_ascii=False)

        bria_request = {
            "structured_prompt": structured_prompt_str
        }

        # Step 3: Generate image with Bria
        result = await generate_image_and_wait(bria_request)

        return {
            "image_url": result["image_url"],
            "json": json_prompt
        }

    except Exception as e:
        print("INSPIRE ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-models")
def list_models():
    try:
        result = client.models.list()  # call Gemini API
        return [m.name for m in result]
    except Exception as e:
        return {"error": str(e)}
