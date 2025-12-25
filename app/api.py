from fastapi import FastAPI
import json

app = FastAPI(title="Hospital Realtime AI")

def read_jsonl(file):
    try:
        with open(file) as f:
            return [json.loads(line) for line in f.readlines()]
    except:
        return []

@app.get("/")
def root():
    return {"message": "Hospital Realtime AI is running"}

@app.get("/status")
def status():
    return read_jsonl("output.jsonl")[-10:]

@app.get("/icu-alerts")
def icu_alerts():
    return read_jsonl("icu_alerts.jsonl")

@app.get("/best-hospital")
def best_hospital():
    return read_jsonl("best_hospital.jsonl")

@app.get("/nearby-hospitals")
def nearby_hospitals():
    return read_jsonl("nearby_hospitals.jsonl")

@app.get("/severity")
def severity():
    return read_jsonl("severity_score.jsonl")

@app.get("/trend")
def trend():
    return read_jsonl("icu_trend.jsonl")

@app.get("/escalation")
def escalation():
    return read_jsonl("auto_escalation.jsonl")
