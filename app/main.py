import pathway as pw

# -------------------------------
# Schema (with location)
# -------------------------------
class HospitalSchema(pw.Schema):
    hospital_id: int
    hospital_name: str
    city: str
    latitude: float
    longitude: float
    icu_beds: int
    oxygen_beds: int
    timestamp: str


# -------------------------------
# Input (streaming CSV)
# -------------------------------
hospital_stream = pw.io.csv.read(
    "../data/",
    schema=HospitalSchema,
    mode="streaming",
)


# -------------------------------
# Latest hospital status
# -------------------------------
latest_status = hospital_stream.groupby(
    hospital_stream.hospital_id
).reduce(
    hospital_id=pw.reducers.latest(hospital_stream.hospital_id),
    hospital_name=pw.reducers.latest(hospital_stream.hospital_name),
    city=pw.reducers.latest(hospital_stream.city),
    latitude=pw.reducers.latest(hospital_stream.latitude),
    longitude=pw.reducers.latest(hospital_stream.longitude),
    icu_beds=pw.reducers.latest(hospital_stream.icu_beds),
    oxygen_beds=pw.reducers.latest(hospital_stream.oxygen_beds),
    timestamp=pw.reducers.latest(hospital_stream.timestamp),
)


# -------------------------------
# ICU Alerts (ICU = 0)
# -------------------------------
icu_alerts = latest_status.filter(
    pw.this.icu_beds == 0
)


# -------------------------------
# ICU Recovered (ICU > 0)
# -------------------------------
icu_recovered = latest_status.filter(
    pw.this.icu_beds > 0
)


# -------------------------------
# ICU Exhaustion Prediction (heuristic)
# -------------------------------
icu_prediction = latest_status.select(
    hospital=pw.this.hospital_name,
    city=pw.this.city,
    predicted_exhaustion=pw.if_else(
        pw.this.icu_beds <= 1,
        "30–60 mins",
        "Stable",
    ),
)


# -------------------------------
# Best Hospital Recommendation
# -------------------------------
best_hospital = latest_status.filter(
    pw.this.icu_beds > 0
).select(
    hospital=pw.this.hospital_name,
    city=pw.this.city,
    icu=pw.this.icu_beds,
    oxygen=pw.this.oxygen_beds,
)


# -------------------------------
# Nearby Hospital (location + ICU)
# -------------------------------
nearby_hospitals = latest_status.select(
    hospital=pw.this.hospital_name,
    city=pw.this.city,
    latitude=pw.this.latitude,
    longitude=pw.this.longitude,
    icu=pw.this.icu_beds,
    oxygen=pw.this.oxygen_beds,
)


# -------------------------------
# City-level ICU Summary
# -------------------------------

city_icu_summary = latest_status.groupby(
    latest_status.city
).reduce(
    city=latest_status.city,         # ✅ FIX
    total_icu=pw.reducers.sum(latest_status.icu_beds),
)



# -------------------------------
# Severity Score
# -------------------------------
severity_score = latest_status.select(
    hospital=pw.this.hospital_name,
    city=pw.this.city,
    severity=pw.if_else(
        pw.this.icu_beds == 0,
        "CRITICAL",
        pw.if_else(pw.this.icu_beds <= 2, "WARNING", "SAFE"),
    ),
)


# -------------------------------
# ICU Trend (simple signal)
# -------------------------------
icu_trend = latest_status.select(
    hospital=pw.this.hospital_name,
    city=pw.this.city,
    trend=pw.if_else(
        pw.this.icu_beds == 0,
        "WORSENING",
        "STABLE",
    ),
)


# -------------------------------
# Auto Escalation
# -------------------------------
auto_escalation = latest_status.filter(
    pw.this.icu_beds == 0
).select(
    hospital=pw.this.hospital_name,
    city=pw.this.city,
    message="ESCALATE: Divert patient to nearby city",
)


# -------------------------------
# Outputs
# -------------------------------
pw.io.jsonlines.write(latest_status, "output.jsonl")
pw.io.jsonlines.write(icu_alerts, "icu_alerts.jsonl")
pw.io.jsonlines.write(icu_recovered, "icu_recovered.jsonl")
pw.io.jsonlines.write(icu_prediction, "icu_prediction.jsonl")
pw.io.jsonlines.write(best_hospital, "best_hospital.jsonl")
pw.io.jsonlines.write(nearby_hospitals, "nearby_hospitals.jsonl")
pw.io.jsonlines.write(city_icu_summary, "dashboard_city.jsonl")
pw.io.jsonlines.write(severity_score, "severity_score.jsonl")
pw.io.jsonlines.write(icu_trend, "icu_trend.jsonl")
pw.io.jsonlines.write(auto_escalation, "auto_escalation.jsonl")


# -------------------------------
# Run engine
# -------------------------------
pw.run()
