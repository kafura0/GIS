from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from app.database import Base

class AOI(Base):
    __tablename__ = "aoi"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    geom = Column(Geometry("POLYGON", srid=4326))
