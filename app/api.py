from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import math

# ---------------- APP INIT ----------------
app = FastAPI()

# ---------------- STATIC & TEMPLATES ----------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ---------------- SAMPLE DATA ----------------
hospitals = [
    {"id": 1, "name": "City Hospital", "lat": 12.97, "lon": 77.59, "severity": 2},
    {"id": 2, "name": "Green Care", "lat": 12.98, "lon": 77.60, "severity": 5},
    {"id": 3, "name": "Apollo Clinic", "lat": 12.95, "lon": 77.58, "severity": 3},
]

# ---------------- DISTANCE LOGIC ----------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

# ---------------- FRONTEND ROUTES ----------------
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/hospitals-ui", response_class=HTMLResponse)
def hospitals_ui(request: Request):
    return templates.TemplateResponse("hospitals.html", {"request": request})

@app.get("/nearby-ui", response_class=HTMLResponse)
def nearby_ui(request: Request):
    return templates.TemplateResponse("nearby.html", {"request": request})

@app.get("/alerts-ui", response_class=HTMLResponse)
def alerts_ui(request: Request):
    return templates.TemplateResponse("alerts.html", {"request": request})

@app.get("/assistant-ui", response_class=HTMLResponse)
def assistant_ui(request: Request):
    return templates.TemplateResponse("assistant.html", {"request": request})

# ---------------- API ROUTES ----------------
@app.get("/nearby")
def nearby(lat: float = Query(...), lon: float = Query(...)):
    results = []
    for h in hospitals:
        distance = haversine(lat, lon, h["lat"], h["lon"])
        item = h.copy()
        item["distance_km"] = distance
        results.append(item)
    results.sort(key=lambda x: x["distance_km"])
    return results

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(payload: ChatRequest):
    msg = payload.message.lower()

    if "icu" in msg or "beds" in msg:
        reply = "Green Care has high ICU load, Apollo Clinic has moderate availability."
    elif "near" in msg:
        reply = "City Hospital is the nearest hospital based on your location."
    elif "safe" in msg or "best" in msg:
        reply = "Green Care Hospital is currently the safest based on severity index."
    else:
        reply = "I can help with ICU availability, nearby hospitals, and safety decisions."

    return {"reply": reply}
