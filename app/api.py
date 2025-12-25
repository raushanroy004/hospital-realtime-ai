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

@app.get("/")
def root():
    return {"message": "Hospital Realtime AI is running"}

@app.get("/hospitals")
def hospitals():
    return read_jsonl("output.jsonl")

@app.get("/best-hospital")
def best_hospital():
    data = read_jsonl("best_hospital.jsonl")
    return data[:5]

@app.get("/nearby")
def nearby(lat: float = Query(...), lon: float = Query(...)):
    data = read_jsonl("nearby_hospitals.jsonl")

    if not data:
        return {"message": "No hospital data available"}

    data.sort(
        key=lambda r: (r["latitude"] - lat) ** 2 + (r["longitude"] - lon) ** 2
    )
    return data[:5]

@app.get("/severity")
def severity():
    return read_jsonl("severity_score.jsonl")

@app.get("/trend")
def trend():
    return read_jsonl("icu_trend.jsonl")

@app.get("/alerts")
def alerts():
    return read_jsonl("auto_escalation.jsonl")
