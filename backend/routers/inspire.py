from fastapi import APIRouter, UploadFile
from services.vlm_client import image_to_json
from services.fibo_client import generate_fibo_image

router = APIRouter()

@router.post("/inspire")
def inspire(image: UploadFile):
    json_prompt = image_to_json(image)
    url, updated_json = generate_fibo_image(json_prompt)
    return {"image_url": url, "json": updated_json}
