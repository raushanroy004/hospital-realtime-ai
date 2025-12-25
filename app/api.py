from fastapi import FastAPI, Query
import json
import os

app = FastAPI(title="Hospital Realtime AI")

BASE_DIR = os.path.dirname(__file__)

def read_jsonl(filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [json.loads(line) for line in f]

# -------------------------------
# Root
# -------------------------------
@app.get("/")
def root():
    return {"message": "Hospital Realtime AI is running"}

# -------------------------------
# All hospital status
# -------------------------------
@app.get("/hospitals")
def hospitals():
    return read_jsonl("output.jsonl")

# -------------------------------
# Best hospital (ICU > 0)
# -------------------------------
@app.get("/best-hospital")
def best_hospital():
    return read_jsonl("best_hospital.jsonl")

# -------------------------------
# Nearby hospital
# -------------------------------
@app.get("/nearby")
def nearby(lat: float = Query(...), lon: float = Query(...)):
    hospitals = read_jsonl("nearby_hospitals.jsonl")

    if not hospitals:
        return {"message": "No hospital data available"}

    hospitals = [h for h in hospitals if h.get("icu", 0) > 0]

    hospitals.sort(
        key=lambda h: (h["latitude"] - lat) ** 2 + (h["longitude"] - lon) ** 2
    )

    if not hospitals:
        return {"message": "No nearby hospitals with ICU"}

    return hospitals[0]

# -------------------------------
# ICU severity
# -------------------------------
@app.get("/severity")
def severity():
    return read_jsonl("severity_score.jsonl")

# -------------------------------
# ICU trend
# -------------------------------
@app.get("/icu-trend")
def icu_trend():
    return read_jsonl("icu_trend.jsonl")

# -------------------------------
# Auto escalation
# -------------------------------
@app.get("/auto-escalation")
def auto_escalation():
    return read_jsonl("auto_escalation.jsonl")
