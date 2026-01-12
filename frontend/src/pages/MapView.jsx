import { useEffect, useState } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import L from "leaflet";
import "leaflet-draw";

import api from "../api/api";

// Component to attach draw controls
function DrawTools({ onAoiCreated }) {
  const map = useMap();

  useEffect(() => {
    if (!map) return;

    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    const drawControl = new L.Control.Draw({
      draw: {
        rectangle: true,
        polygon: true,
        polyline: false,
        circle: false,
        marker: false,
        circlemarker: false,
      },
      edit: {
        featureGroup: drawnItems,
      },
    });

    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, async (e) => {
      const layer = e.layer;
      drawnItems.addLayer(layer);

      const geojson = layer.toGeoJSON();

      onAoiCreated(geojson);
    });

  }, [map]);

  return null;
}

// Component to display returned AOI GeoJSON
function AoiResultLayer({ data }) {
  const map = useMap();

  useEffect(() => {
    if (!data) return;

    const layer = L.geoJSON(data, {
      style: {
        color: "green",
        weight: 3,
      },
    }).addTo(map);

    map.fitBounds(layer.getBounds());

    return () => {
      map.removeLayer(layer);
    };
  }, [data]);

  return null;
}

// Main Map Page
export default function MapView() {
  const [aoiResult, setAoiResult] = useState(null);

  // Send AOI to backend
  const processAoi = async (geojson) => {
    try {
      const res = await api.post("process-aoi/", {
        geometry: geojson.geometry,
      });

      const returnedGeoJSON = JSON.parse(res.data.geojson);

      setAoiResult(returnedGeoJSON);
    } catch (err) {
      console.error(err);
      alert("Error processing AOI");
    }
  };

  return (
    <div className="w-full h-screen">
      <MapContainer
        center={[0.0236, 37.9062]}
        zoom={6}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="© OpenStreetMap contributors"
        />

        <DrawTools onAoiCreated={processAoi} />

        {aoiResult && <AoiResultLayer data={aoiResult} />}
      </MapContainer>
    </div>
  );
}
