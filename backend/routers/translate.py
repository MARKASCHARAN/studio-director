from fastapi import APIRouter

router = APIRouter()

@router.post('/translate')
def translate_brief(payload: dict):
    # TODO: call VLM to produce JSON
    return {"json": {}}
