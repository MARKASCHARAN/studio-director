# backend/main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Any, Dict
from config.settings import settings

app = FastAPI(title="Studio-Director API", version="0.1.0")

# --- Simple Pydantic schemas for docs and validation ---
class TranslateRequest(BaseModel):
    prompt: str

class TranslateResponse(BaseModel):
    json: Dict[str, Any]

class GenerateRequest(BaseModel):
    json: Dict[str, Any]

class GenerateResponse(BaseModel):
    image_url: str
    json: Dict[str, Any]

class RefineRequest(BaseModel):
    json: Dict[str, Any]
    instruction: str

class RefineResponse(BaseModel):
    image_url: str
    json: Dict[str, Any]

class InspireResponse(BaseModel):
    image_url: str
    json: Dict[str, Any]

# --- Test key route ---
@app.get("/test-key", summary="Test Key", response_model=dict)
def test_key():
    return {"env": settings.ENV, "key_loaded": bool(settings.BRIA_API_KEY)}

from services.vlm_client import prompt_to_json, image_to_json
from services.fibo_client import generate_image



@app.post("/translate", summary="Prompt -> JSON", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    json_prompt = prompt_to_json(req.prompt)
    return {"json": json_prompt}

@app.post("/generate", summary="JSON -> Image", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    result = generate_image(req.json)
    return {"image_url": result["image_url"], "json": result["json_prompt"]}



@app.post("/refine", summary="Refine JSON -> Image", response_model=RefineResponse)
def refine(req: RefineRequest):
    # Step 1: merge instruction into JSON (simple refinement)
    req.json["refinement_instruction"] = req.instruction

    result = generate_image(req.json)
    return {"image_url": result["image_url"], "json": result["json_prompt"]}




@app.post("/inspire", summary="Image -> JSON -> Image", response_model=InspireResponse)
async def inspire(image: UploadFile = File(...)):
    json_prompt = image_to_json(image)
    result = generate_image(json_prompt)

    return {"image_url": result["image_url"], "json": result["json_prompt"]}
