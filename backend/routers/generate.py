from fastapi import APIRouter
from schemas.generate_schema import GenerateRequest
from services.fibo_client import generate_fibo_image
from services.agent_service import auto_fix_json

router = APIRouter()

@router.post("/generate")
def generate_image(req: GenerateRequest):

    json_fixed = auto_fix_json(req.json)

    url, updated_json = generate_fibo_image(json_fixed)

    return {
        "image_url": url,
        "json": updated_json
    }
