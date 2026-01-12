from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AOI
from app.schemas.aoi import AOICreate, AOIResponse
from shapely.geometry import shape, mapping

router = APIRouter()

# GET all AOIs
@router.get("/", response_model=list[AOIResponse])
def get_aois(db: Session = Depends(get_db)):
    return db.query(AOI).all()

# POST AOI (accept GeoJSON)
@router.post("/", response_model=AOIResponse)
def create_aoi(aoi: AOICreate, db: Session = Depends(get_db)):
    try:
        geom = mapping(shape(aoi.geojson))  # convert GeoJSON to shapely object
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid GeoJSON: {e}")

    db_aoi = AOI(geom=geom)
    db.add(db_aoi)
    db.commit()
    db.refresh(db_aoi)
    return db_aoi
