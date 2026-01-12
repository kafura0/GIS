from fastapi import FastAPI
from app.database import Base, engine
from app.routers import aoi
from fastapi.staticfiles import StaticFiles

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GIS API",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include AOI routes
app.include_router(aoi.router, prefix="/api/aoi", tags=["AOI"])


@app.get("/")
def root():
    return {"message": "GIS API is running 🚀"}
