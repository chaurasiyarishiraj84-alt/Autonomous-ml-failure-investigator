---
title: Autonomous ML Failure Investigator
emoji: 🧠
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: true
license: mit
---

# 🧠 Autonomous ML Failure Investigator

> A Tier-1+ production-grade MLOps system that continuously monitors deployed ML models, detects failures, explains root causes, and recommends corrective actions — autonomously and intelligently.

> 💡 **Running on HuggingFace Spaces?** No setup needed — the app is already live above. The installation and localhost instructions below are for **local development only.**

**Autonomous ML Failure Investigator** is an advanced Model Observability, Drift Detection, and Root Cause Analysis (RCA) system designed to monitor deployed machine learning models in real time, detect failures, explain why they occur, and provide actionable recommendations with human-in-the-loop governance.

This project simulates industry-grade MLOps monitoring platforms used in production environments by companies like Google, Netflix, and Amazon.

---

## 🩺 The Core Idea

Think of this system as a **doctor for ML models in production.**

| Doctor | This System |
|---|---|
| Patient | Deployed ML model |
| Symptoms | Accuracy drop, drift, anomalies |
| Tests | Metrics, KS-test, SHAP |
| Diagnosis | Root Cause Analysis |
| Explanation | Human-readable report |
| Medicine | Retrain, rollback, fix pipeline |
| Surgery (optional) | Auto-fix with human approval |
| Medical history | Failure memory & learning |

---

## 🚀 What This Project Does

For any deployed ML model, this system:

- **Continuously monitors** prediction behavior via API
- **Learns a baseline** of normal model performance automatically
- **Detects drift and anomalies** using statistical tests and ML
- **Explains why failures happen** through Root Cause Analysis
- **Identifies which features** are responsible for failures
- **Generates actionable recommendations** specific to each failure type
- **Requires human approval** before any critical action is taken
- **Produces a diagnostic report** for model improvement
- **Learns from past failures** to improve detection over time

---

## 🏗️ System Architecture

```
User connects model via API URL
         ↓
Data Capture Layer          → logs inputs, predictions, latency
         ↓
Baseline Learning           → learns normal behavior automatically
         ↓
Drift & Anomaly Detection   → KS-test, variance, feature shift
         ↓
Root Cause Analysis (RCA)   → why did it fail? which feature?
         ↓
Explanation Layer           → plain English findings
         ↓
Recommendation Engine       → specific actionable fixes
         ↓
Human Approval (Governance) → approve/reject with audit log
         ↓
Continuous Learning         → improves from past failures
```

---

## ✅ Compatible API Requirements

Any API URL you connect to this system must follow **3 simple rules:**

### 1. Must be a public URL
```
✅ https://anything.hf.space/predict
✅ https://any-public-api.com/predict
❌ http://127.0.0.1:9000/predict   ← localhost only works for local development
```

### 2. Must accept POST requests with a JSON body
```json
POST /predict
Content-Type: application/json

{"text": "anything"}
```

### 3. Must return JSON with a `confidence` field
```json
{
    "prediction": "any string",
    "confidence": 0.85
}
```

> `confidence` must be a **float between 0.0 and 1.0** — this is the most critical field.

---

### 🧪 Ready-to-Use Test Models

Deploy these on HuggingFace to simulate different failure scenarios:

| Model | URL | Behavior |
|---|---|---|
| 🟢 Healthy Model | `https://rishi-raj123-healthy-model.hf.space/predict` | confidence 0.80–0.95 — normal |
| 🔴 Low Confidence | `https://rishi-raj123-low-confidence-model.hf.space/predict` | confidence 0.10–0.30 — triggers alerts |
| 🟡 Random Model | `https://rishi-raj123-random-model.hf.space/predict` | confidence 0.0–1.0 — unpredictable |
| 📉 Drift Model | `https://rishi-raj123-drift-model.hf.space/predict` | confidence degrades over time |

Each model is a minimal FastAPI app with a single `POST /predict` endpoint — fully compatible with all system features including drift detection, RCA, and recommendations.

---

## 📂 Project Structure

```
autonomous-ml-failure-investigator/
│
├── app/
│   ├── main.py                              # FastAPI entry point
│   ├── api/
│   │   └── routes/
│   │       ├── monitoring.py                # Monitoring API endpoints
│   │       └── recommendation.py            # Recommendation routes
│   ├── core/
│   │   ├── detection/
│   │   │   ├── anomaly_detector.py          # Rule + ML anomaly detection
│   │   │   ├── drift_detector.py            # KS-test, variance, feature drift
│   │   │   └── metric_checker.py            # Threshold-based metric checks
│   │   ├── probing/
│   │   │   └── universal_model_caller.py    # Universal model connector
│   │   ├── rca/
│   │   │   └── feature_attribution.py       # Feature-level RCA
│   │   ├── recommendation/
│   │   │   └── rule_engine.py               # Maps failures to fixes
│   │   └── storage/
│   │       └── baseline_store.py            # Baseline storage layer
│   └── services/
│       ├── baseline_builder.py              # Baseline service
│       ├── investigation_service.py         # Core investigation layer
│       └── monitoring_service.py            # Monitoring service
│
├── ui/
│   └── dashboard.py                         # Streamlit frontend dashboard
│
├── tests/
│   ├── test_monitoring.py
│   ├── test_detection.py
│   └── test_recommendation.py
│
├── baselines/                               # Stored model baselines (auto-generated)
├── Dockerfile                               # Docker configuration
├── start.sh                                 # Multi-process startup script
├── requirements.txt                         # Python dependencies
└── README.md
```

---

## ✨ Key Features

### 📊 Model Monitoring
- Average confidence score tracking
- Confidence standard deviation
- Error rate calculation
- Latency monitoring in milliseconds
- Real-time sample collection counter

### 📈 Baseline Learning
- Automatically learns "normal" model behavior on first run
- Stores baseline metrics per model URL
- Used as reference for all future drift comparisons

### 🚨 Drift & Anomaly Detection
- **KS-Test** — statistical confidence distribution drift
- **Variance analysis** — confidence explosion detection
- **Feature mean shift** — covariate drift per feature
- **Rule-based checks** — low confidence, high error rate, silent failures
- **ML-based** — Isolation Forest anomaly detection

### 🔍 Root Cause Analysis (RCA)
- Identifies exactly why failure occurred
- Reports which features contributed most
- Highlights affected user segments
- Assigns severity: `critical` / `high` / `medium` / `low`

### 🛠️ Recommendation Engine
- Maps each failure type to specific corrective action
- Actionable suggestions: retrain, rollback, fix pipeline, recalibrate
- Priority-ranked: `CRITICAL` → `HIGH` → `MEDIUM` → `LOW`
- Context-aware — different recommendations per failure type

### 👨‍⚖️ Human-in-the-Loop Governance
- Approve / Reject recommendations via dashboard
- No auto-action without explicit user consent
- Full audit log with timestamps
- Compliant with enterprise governance standards

### 🖥️ Live Dashboard (Streamlit)
- Real-time Plotly charts (confidence, error rate, latency)
- Start / Stop monitoring controls
- CSV data export
- Alerts & anomaly indicators
- Governance approval panel with audit log
- Auto-refreshes every 2 seconds

---

## ⚙️ Installation (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/chaurasiyarishiraj84-alt/Autonomous-ml-failure-investigator.git
cd autonomous-ml-failure-investigator
```

### 2. Create virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```

---

## ▶️ Running Locally

**Start the backend:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Verify at: `http://localhost:8000/health`

**Start the dashboard:**
```bash
streamlit run ui/dashboard.py
```
Open at: `http://localhost:8501`

---

## 🧪 Quick Test

Create a simple local test model (`test_model.py`):

```python
from fastapi import FastAPI
import random

app = FastAPI()

@app.post("/predict")
def predict(data: dict = None):
    return {
        "prediction": "spam" if random.random() > 0.5 else "not_spam",
        "confidence": round(random.uniform(0.6, 0.95), 3)
    }
```

Run it:
```bash
uvicorn test_model:app --port 9000 --reload
```

In the dashboard enter `http://127.0.0.1:9000/predict` → click **Start Monitoring**.

---

## 📄 API Reference

### `POST /monitoring/analyze`
Runs full investigation on a model endpoint.

**Request:**
```json
{ "prediction_url": "https://your-model.com/predict" }
```

**Response:**
```json
{
  "metrics": {
    "avg_confidence": 0.85,
    "confidence_std": 0.04,
    "error_rate": 0.02,
    "total_samples": 5
  },
  "drift": {
    "confidence_distribution": {
      "method": "KS-test",
      "drift_detected": false,
      "p_value": 0.43
    }
  },
  "anomalies": [],
  "rca": {
    "root_cause": "none",
    "severity": "none",
    "failure_reason": "Model operating normally"
  },
  "recommendations": [
    { "action": "No action required", "priority": "NONE" }
  ],
  "samples_collected": 5
}
```

### `GET /health`
Returns system health status.

### `POST /monitoring/prediction`
Ingest a single prediction log manually.

---

## 📚 Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Uvicorn |
| Frontend Dashboard | Streamlit |
| Data Validation | Pydantic |
| Drift Detection | SciPy (KS-test), NumPy |
| Anomaly Detection | scikit-learn (Isolation Forest) |
| Explainability | SHAP |
| Visualization | Plotly |
| Storage | JSON-based baseline store |
| Logging | Python logging + Loguru |
| Containerization | Docker |

---

## 🔐 Security Design

- **Read-only access** — system never modifies user models or data
- **No source code access** — monitors behavior via API only
- **No data ownership** — raw data never stored long-term
- **Permission-based actions** — all critical actions require explicit user consent
- **Audit trail** — every approval/rejection logged with timestamp
- **PII-safe** — only aggregated metrics stored, never raw features

---

## 🐛 Troubleshooting

| Problem | Error | Solution |
|---|---|---|
| Backend not starting | `Address already in use` | Kill process on port 8000 |
| Dashboard not loading | `ConnectionError` | Start backend first on port 8000 |
| Module not found | `No module named 'fastapi'` | Activate venv → `pip install -r requirements.txt` |
| Samples stuck at 0 | — | Ensure model returns `confidence` field |
| autorefresh not found | — | `pip install streamlit-autorefresh` |
| pydantic error | `No module named 'pydantic_settings'` | `pip install pydantic-settings` |
| Confidence always 0.0 | — | Use a public URL, not localhost on HuggingFace |

---

## 🌍 Deployment

- ✅ Docker ready
- ✅ HuggingFace Spaces compatible
- ✅ Cloud-ready (AWS, GCP, Azure)
- ✅ CI/CD compatible

```bash
docker build -t ml-failure-investigator .
docker run -p 7860:7860 ml-failure-investigator
```

---

## 🎯 Use Cases

| Domain | Example |
|---|---|
| Finance | Fraud model drift detection |
| Healthcare | Silent diagnostic model failure prevention |
| E-commerce | Recommendation quality degradation |
| Autonomous Driving | Edge model anomaly analysis |
| AI SaaS | Customer model health monitoring |

---

## 🏆 Tier-1+ MLOps Compliance

| Feature | Status |
|---|---|
| Continuous monitoring | ✅ |
| Explainable AI (XAI) | ✅ |
| Automated root-cause analysis | ✅ |
| Human-in-the-loop governance | ✅ |
| Audit logging & compliance | ✅ |
| Domain-agnostic core | ✅ |
| Safe advisory-first design | ✅ |
| Statistical drift detection | ✅ |
| Auto-refresh live dashboard | ✅ |

---

## 👤 Author

**Rishi Raj Chaurasiya**
B.Tech — Artificial Intelligence & Machine Learning

---

## 📜 License

MIT License — Open Source

---

> *This project demonstrates how real production ML systems are monitored, debugged, and governed — not just how models are trained. It reflects industry-standard MLOps thinking used at scale.*
