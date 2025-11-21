from fastapi import APIRouter

router = APIRouter()

@router.post('/refine')
def refine_scene(payload: dict):
    # TODO: apply refine patch
    return {"status":"ok"}
