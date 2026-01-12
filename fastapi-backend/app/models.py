from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AOI(Base):
    __tablename__ = "aoi"

    id = Column(Integer, primary_key=True, index=True)
    geom = Column(JSON)  # store GeoJSON for simplicity
