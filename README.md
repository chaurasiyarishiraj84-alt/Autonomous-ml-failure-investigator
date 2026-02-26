---
title: Autonomous ML Failure Investigator
emoji: 🧠
colorFrom: purple
colorTo: blue
sdk: streamlit
app_file: ui/dashboard.py
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

## 📂 Project Structure

```
autonomous-ml-failure-investigator/
│
├── app/
│   ├── main.py                              # FastAPI entry point
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py                      # Authentication routes
│   │       ├── model.py                     # Model registration routes
│   │       ├── monitoring.py                # Monitoring API endpoints
│   │       └── recommendation.py            # Recommendation routes
│   ├── core/
│   │   ├── automation/
│   │   │   ├── decision_engine.py           # Auto-action decision logic
│   │   │   ├── deploy_manager.py            # Safe model deployment
│   │   │   ├── executor.py                  # Action executor
│   │   │   ├── model_validator.py           # Model validation checks
│   │   │   └── retrain_pipeline.py          # Retraining trigger
│   │   ├── baselines/
│   │   │   ├── baseline_builder.py          # Baseline construction
│   │   │   └── baseline_store.py            # Baseline persistence
│   │   ├── detection/
│   │   │   ├── accuracy_drift_detector.py   # Accuracy drift detection
│   │   │   ├── anomaly_detector.py          # Rule + ML anomaly detection
│   │   │   ├── drift_detector.py            # KS-test, variance, feature drift
│   │   │   └── metric_checker.py            # Threshold-based metric checks
│   │   ├── governance/
│   │   │   └── approval_flow.py             # Human approval + audit logs
│   │   ├── learning/
│   │   │   ├── failure_memory.py            # Stores past failure patterns
│   │   │   └── pattern_learner.py           # Learns from failure history
│   │   ├── metrics/
│   │   │   └── baseline_builder.py          # Metrics computation
│   │   ├── observer/
│   │   │   ├── accuracy_tracker.py          # Tracks accuracy over time
│   │   │   ├── data_collector.py            # Collects prediction data
│   │   │   ├── model_prober.py              # Probes model behavior
│   │   │   └── model_watcher.py             # Continuous model watcher
│   │   ├── probing/
│   │   │   ├── model_prober.py              # Model probe logic
│   │   │   ├── payload_generator.py         # Test payload generation
│   │   │   └── universal_model_caller.py    # Universal model connector
│   │   ├── rca/
│   │   │   ├── feature_attribution.py       # Feature-level RCA
│   │   │   ├── root_cause_analyzer.py       # Main RCA engine
│   │   │   └── shap_explainer.py            # SHAP-based explainability
│   │   ├── recommendation/
│   │   │   ├── recommender.py               # Recommendation orchestrator
│   │   │   └── rule_engine.py               # Maps failures to fixes
│   │   ├── storage/
│   │   │   └── baseline_store.py            # Baseline storage layer
│   │   └── utils/
│   │       └── serialization.py             # JSON/data serialization
│   ├── db/
│   │   ├── models.py                        # Database models
│   │   └── session.py                       # DB session management
│   ├── schemas/
│   │   ├── auth.py                          # Auth request/response models
│   │   ├── model.py                         # Model schema
│   │   ├── monitoring.py                    # Monitoring schema
│   │   └── recommendation.py               # Recommendation schema
│   ├── security/
│   │   ├── auth.py                          # Auth & token handling
│   │   └── encryption.py                    # Data encryption
│   ├── services/
│   │   ├── auth_service.py                  # Authentication service
│   │   ├── automation_service.py            # Auto-action service
│   │   ├── baseline_builder.py              # Baseline service
│   │   ├── detection_service.py             # Detection orchestration
│   │   ├── investigation_service.py         # Core investigation layer
│   │   ├── monitoring_service.py            # Monitoring service
│   │   ├── monitoring_orchestrator.py       # Monitoring orchestration
│   │   └── recommendation_service.py        # Recommendation service
│   └── utils/
│       ├── config.py                        # Settings & environment
│       └── logger.py                        # Structured logging
│
├── ui/
│   └── dashboard.py                         # Streamlit frontend dashboard
│
├── tests/
│   ├── test_monitoring.py                   # Monitoring tests
│   ├── test_detection.py                    # Detection tests
│   └── test_recommendation.py              # Recommendation tests
│
├── data/
│   ├── audit_logs/                          # Governance audit trail
│   │   └── approvals.json                   # Human approval log
│   └── samples/                             # Safe example data
│
├── baselines/                               # Stored model baselines (auto-generated)
│
├── docs/
│   ├── architecture.md                      # System architecture details
│   ├── threat_model.md                      # Security threat model
│   └── user_guide.md                        # User guide
│
├── docker/
│   └── Dockerfile                           # Docker configuration
│
├── dummy_model/                             # Test model for local testing
│
├── .env.example                             # Environment variables template
├── .gitignore                               # Git ignore rules
├── Dockerfile                               # Root Dockerfile
├── requirements.txt                         # Python dependencies
└── README.md
```

---

## ✨ Key Features

### 📊 Model Monitoring
- Average confidence score
- Confidence standard deviation
- Error rate tracking
- Latency monitoring
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
- Assigns severity: critical / high / medium / low

### 🧠 Explainability
- Feature importance analysis via SHAP
- Identifies drifting features
- Plain English failure explanations
- Business-safe, audit-ready reports

### 🛠️ Recommendation Engine
- Maps each failure type to specific corrective action
- Actionable suggestions: retrain, rollback, fix pipeline, recalibrate
- Priority-ranked: CRITICAL → HIGH → MEDIUM → LOW
- Context-aware — different recommendations per failure type

### 👨‍⚖️ Human-in-the-Loop Governance
- Approve / Reject recommendations via dashboard
- No auto-action without explicit user consent
- Full audit log with timestamps
- Compliant with enterprise governance standards

### 🖥️ Dashboard (Streamlit)
- Real-time Plotly charts (confidence, error rate, latency)
- Start / Stop monitoring controls
- CSV data export
- Alerts & anomaly indicators
- Governance approval buttons with audit log
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

### Start the backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify it's running:
```
http://localhost:8000/health
```

### Start the dashboard
```bash
streamlit run ui/dashboard.py
```

Open in browser:
```
http://localhost:8501
```

---

## 🧪 Quick Test

Create a simple test model (`test_model.py`):

```python
from fastapi import FastAPI
import random

app = FastAPI()

@app.post("/predict")
def predict(data: dict):
    return {
        "prediction": "spam" if random.random() > 0.5 else "not_spam",
        "confidence": round(random.uniform(0.6, 0.95), 3)
    }
```

Run it:
```bash
uvicorn test_model:app --port 9000 --reload
```

In the dashboard, enter `http://127.0.0.1:9000/predict` and click **Start Monitoring**.

To simulate failures and test RCA & recommendations:
```python
"confidence": round(random.uniform(0.1, 0.3), 3)  # triggers low confidence alert
```

---

## 📄 API Reference

### `POST /monitoring/analyze`

Runs full investigation on a model endpoint.

**Request:**
```json
{
  "prediction_url": "http://your-model.com/predict"
}
```

**Response:**
```json
{
  "metrics": {
    "avg_confidence": 0.85,
    "confidence_std": 0.04,
    "error_rate": 0.0,
    "total_samples": 5
  },
  "drift": {
    "confidence_distribution": {
      "method": "KS-test",
      "statistic": 0.2,
      "p_value": 0.43,
      "drift_detected": false
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

## 🔌 Supported Model Types

| Type | Example |
|---|---|
| Generic REST API | Any `POST /predict` endpoint |
| HuggingFace Inference API | `https://api-inference.huggingface.co/...` |
| Gradio Apps | `/run/predict` endpoints |
| Local models | `http://localhost:PORT/predict` |

---

## 🐛 Troubleshooting

### Problem: Backend not starting
**Error:** `ERROR: Address already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

---

### Problem: Streamlit dashboard not loading
**Error:** `ConnectionError: Failed to connect to backend`

**Solution:** Make sure backend is running first on port 8000, then start dashboard:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

### Problem: ModuleNotFoundError
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Activate virtual environment first, then:
```bash
pip install -r requirements.txt
```

---

### Problem: RCA variable error
**Error:** `UnboundLocalError: cannot access local variable 'rca'`

**Solution:** Remove this line from `investigation_service.py`:
```python
from app.core import rca  # delete this line
```

---

### Problem: Samples Collected stays at 0
**Solution:** Make sure your model returns a `confidence` field in its response:
```json
{ "prediction": "spam", "confidence": 0.87 }
```

---

### Problem: streamlit-autorefresh not found
**Solution:**
```bash
pip install streamlit-autorefresh
```

---

### Problem: SHAP or Evidently install fails
**Solution:**
```bash
pip install shap --no-cache-dir
pip install evidently --no-cache-dir
```

---

### Problem: pydantic_settings import error
**Error:** `ModuleNotFoundError: No module named 'pydantic_settings'`

**Solution:**
```bash
pip install pydantic-settings
```

---

### Problem: Port already in use for test model
**Solution:** Run test model on a different port:
```bash
uvicorn test_model:app --port 9001 --reload
# Then use http://127.0.0.1:9001/predict in dashboard
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 🌍 Deployment

- ✅ Docker ready
- ✅ Hugging Face Spaces compatible
- ✅ Cloud-ready architecture (AWS, GCP, Azure)
- ✅ CI/CD compatible

```bash
docker build -t ml-failure-investigator .
docker run -p 8000:8000 ml-failure-investigator
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

> This project demonstrates how real production ML systems are monitored, debugged, and governed — not just how models are trained. It reflects industry-standard MLOps thinking used at scale.