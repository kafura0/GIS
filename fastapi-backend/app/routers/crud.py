from sqlalchemy.orm import Session
from . import models
from geoalchemy2.shape import from_shape
from shapely.geometry import shape


def create_aoi(db: Session, name: str, geom_geojson: dict):
    geom_obj = from_shape(shape(geom_geojson), srid=4326)
    db_obj = models.AOI(name=name, geom=geom_obj)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_aois(db: Session):
    return db.query(models.AOI).all()