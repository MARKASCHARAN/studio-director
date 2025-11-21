from pydantic import BaseModel

class RefinePatch(BaseModel):
    path: str
    value: object
