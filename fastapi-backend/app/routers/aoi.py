from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shapely.geometry import shape
from geoalchemy2.shape import from_shape, to_shape

from app.database import get_db
from app.models.aoi import AOI
from app.schemas.aoi import AOICreate, AOIResponse

router = APIRouter(prefix="/api/aoi", tags=["AOI"])


@router.get("/", response_model=list[AOIResponse])
def get_aois(db: Session = Depends(get_db)):
    db_aois = db.query(AOI).all()
    results = []
    for aoi in db_aois:
        geom = to_shape(aoi.geom)
        results.append(
            AOIResponse(
                id=aoi.id,
                name=aoi.name,
                geom=geom.__geo_interface__,
            )
        )
    return results


@router.post("/", response_model=AOIResponse)
def create_aoi(aoi: AOICreate, db: Session = Depends(get_db)):
    try:
        # GeoJSON dict → shapely object
        shp_geom = shape(aoi.geom)

        # Shapely → WKBElement for PostGIS
        db_geom = from_shape(shp_geom, srid=4326)

        db_aoi = AOI(name=aoi.name, geom=db_geom)
        db.add(db_aoi)
        db.commit()
        db.refresh(db_aoi)

        # Convert back to GeoJSON before returning
        return AOIResponse(
            id=db_aoi.id,
            name=db_aoi.name,
            geom=shp_geom.__geo_interface__
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Invalid geometry: {str(e)}")

