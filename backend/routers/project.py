from fastapi import APIRouter

router = APIRouter()

@router.post('/project/save')
def save_project(payload: dict):
    return {"status":"saved"}

@router.get('/project/load')
def load_project():
    return {"project": null}
