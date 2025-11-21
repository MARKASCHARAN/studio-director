from fastapi import APIRouter

router = APIRouter()

@router.post('/inspire')
def inspire_generation(payload: dict):
    # TODO: analyze image and produce variations
    return {"status":"ok"}
