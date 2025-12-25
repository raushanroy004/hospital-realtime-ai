from fastapi import FastAPI, Query

app = FastAPI()

# Dummy hospital data
hospitals = [
    {"id": 1, "name": "City Hospital", "lat": 12.97, "lon": 77.59, "severity": 2},
    {"id": 2, "name": "Green Care", "lat": 12.98, "lon": 77.60, "severity": 5},
    {"id": 3, "name": "Apollo Clinic", "lat": 12.95, "lon": 77.58, "severity": 3},
]

@app.get("/")
def root():
    return {"message": "Hospital Realtime AI is running"}

@app.get("/hospitals")
def get_hospitals():
    return hospitals

@app.get("/best-hospital")
def best_hospital():
    return max(hospitals, key=lambda x: x["severity"])

@app.get("/nearby")
def nearby(lat: float = Query(...), lon: float = Query(...)):
    return hospitals
