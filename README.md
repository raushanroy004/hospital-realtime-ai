🏥 Hospital Realtime AI — Emergency Decision Intelligence Platform

🚀 Live Project:
👉 https://hospital-realtime-ai.onrender.com

(Public demo — works on desktop & mobile)

📌 Problem Statement

In medical emergencies, time-critical decisions like which hospital to choose can save lives.
However, patients and ambulances often lack real-time visibility into:

ICU bed availability

Hospital load and severity

Nearby safer alternatives

Emergency escalation alerts

This project solves that gap using real-time data processing and AI-assisted decision support.

💡 Solution Overview

Hospital Realtime AI is an end-to-end platform that provides:

📊 Live hospital status monitoring

🚑 Nearby hospital recommendations using location

🚨 Emergency alerts when ICU capacity is critical

🤖 AI assistant for instant decision guidance

🌐 Clean, professional multi-page dashboard UI

☁️ Cloud-deployed and publicly accessible

The system is built using Pathway for real-time data processing and FastAPI for serving insights.

🧠 Key Features
✅ Real-Time Hospital Intelligence

ICU availability tracking

Severity index (low / medium / high load)

Live updates using streaming logic

📍 Nearby Hospital Finder

Distance-based recommendations using latitude & longitude

Sorted results for fastest decision-making

Interactive map integration

🚨 Emergency Alerts

Red blinking alerts for ICU exhaustion

Automated diversion recommendations

High-load early warnings

🤖 AI Medical Assistant

Natural language queries like:

“Which hospital has ICU beds?”

“What is the safest nearby hospital?”

Fast, rule-based responses (hackathon-safe & reliable)

🎨 Professional UI / UX

Dashboard-style layout

Multi-page navigation

Apple / Google-inspired clean design

Responsive & deployment-ready

🏗️ System Architecture
[ Streaming Data ]
        ↓
[ Pathway Engine ]
  (Real-time processing)
        ↓
[ FastAPI Backend ]
        ↓
[ Dashboard + APIs ]
        ↓
[ End Users / Emergency Teams ]

🛠️ Tech Stack

Pathway — Real-time data processing framework

FastAPI — Backend API & server

Uvicorn — ASGI server

HTML / CSS / Jinja2 — Frontend UI

Leaflet.js — Map visualization

Render — Cloud deployment

📂 Project Structure
hospital_realtime_ai/
│
├── app/
│   ├── api.py              # FastAPI backend
│   ├── templates/          # HTML pages
│   └── static/             # CSS & assets
│
├── data/                   # Simulated hospital streams
├── requirements.txt
├── render.yaml
└── README.md

🚀 Live Demo Routes
Feature	URL
Dashboard	/
Nearby Hospitals	/nearby-ui
Alerts	/alerts-ui
AI Assistant	/assistant-ui
API (Nearby)	/nearby?lat=12.97&lon=77.59
⚙️ How to Run Locally
# Clone repo
git clone https://github.com/raushanroy004/hospital-realtime-ai.git
cd hospital-realtime-ai

# Create virtual env
python3 -m venv pathway_env
source pathway_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.api:app --reload


Open:
👉 http://127.0.0.1:8000

🌍 Deployment

This project is deployed on Render using:

uvicorn app.api:app --host 0.0.0.0 --port 10000


Deployment configuration is included via render.yaml.

🎯 Use-Cases

Emergency response teams

Ambulance routing decisions

Hospital capacity planning

Public health dashboards

Smart city healthcare systems

📈 Future Enhancements

🔍 Real LLM-based RAG with vector search

📡 Kafka / live data connectors

🏥 Integration with real hospital feeds

🌙 Dark mode UI

📱 Mobile-first PWA

🏆 Why This Project Stands Out

✔ Real-time data processing
✔ End-to-end system (backend + frontend + deploy)
✔ Clear real-world impact
✔ Clean architecture
✔ Hackathon & resume-ready

👤 Author

Raushan Roy

GitHub: https://github.com/raushanroy004

Domain: AI / ML / Real-time Systems

📜 License

This project is built for educational, demonstration, and non-commercial use.
