from fastapi import APIRouter
from schemas.refine_schema import RefineRequest
from services.vlm_client import refine_json
from services.fibo_client import generate_fibo_image

router = APIRouter()

@router.post("/refine")
def refine(req: RefineRequest):
    refined_json = refine_json(req.json, req.instruction)
    url, updated_json = generate_fibo_image(refined_json)
    return {"image_url": url, "json": updated_json}
