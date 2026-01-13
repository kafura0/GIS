# FastAPI GIS Backend


1. Copy .env.example -> .env and fill in DB credentials.
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run FastAPI server:

``bash
uvicorn app.main:app --reload
```

4. Test endpoints in Postman:

GET all AOIs: GET http://127.0.0.1:8000/api/aoi

Create AOI (POST): URL: http://127.0.0.1:8000/api/aoi Body (JSON): { "name": "MyAOI", "geom": { "type": "Polygon", "coordinates": [ [ [0,0], [0,1], [1,1], [1,0], [0,0] ] ] } }