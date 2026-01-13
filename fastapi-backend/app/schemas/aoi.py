from pydantic import BaseModel, Field

class AOICreate(BaseModel):
    geom: dict = Field(..., description="GeoJSON geometry")
    name: str | None = None

class AOIResponse(BaseModel):
    id: int
    name: str | None
    geom: dict

    class Config:
        from_attributes = True   # formerly orm_mode
