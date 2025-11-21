from fastapi import APIRouter

router = APIRouter()

@router.post('/generate')
def generate_scene(payload: dict):
    # TODO: call FIBO to generate images
    return {"status":"queued"}
