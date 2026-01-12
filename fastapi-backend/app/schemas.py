from pydantic import BaseModel
from typing import Any, Dict

class AOICreate(BaseModel):
    type: str
    geometry: Dict[str, Any]
    properties: Dict[str, Any] | None = None

class AOIResponse(BaseModel):
    id: int
    name: str
    geojson: dict

    class Config:
        orm_mode = True
