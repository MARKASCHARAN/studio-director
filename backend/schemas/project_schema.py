from pydantic import BaseModel
from typing import Any

class Project(BaseModel):
    id: str | None = None
    name: str
    data: dict[str, Any]
