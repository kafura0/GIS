from pydantic import BaseModel
from typing import List
from shapely.geometry import mapping, shape

class AOICreate(BaseModel):
    # Accept a GeoJSON polygon
    geojson: dict

class AOIResponse(BaseModel):
    id: int
    geojson: dict

    class Config:
        orm_mode = True
