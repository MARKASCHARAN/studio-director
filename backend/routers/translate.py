from fastapi import APIRouter
from services.vlm_client import prompt_to_json
from schemas.translate_schema import TranslateRequest

router = APIRouter()

@router.post("/translate")
def translate_prompt(req: TranslateRequest):
    json_prompt = prompt_to_json(req.prompt)
    return {"json": json_prompt}
