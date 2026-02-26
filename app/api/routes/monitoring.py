from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

from app.schemas.monitoring import PredictionLog
from app.services.monitoring_service import MonitoringService
from app.services.investigation_service import InvestigationService

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


# 1️⃣ Live prediction ingestion (optional / future use)
@router.post("/prediction")
def log_prediction(data: PredictionLog):
    return MonitoringService.ingest_prediction(data)


# 2️⃣ Autonomous analysis (ONLY model URL)
class MonitoringRequest(BaseModel):
    prediction_url: HttpUrl
  
from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

from app.schemas.monitoring import PredictionLog
from app.services.monitoring_service import MonitoringService
from app.services.investigation_service import InvestigationService

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


# 1️⃣ Live prediction ingestion (optional / future use)
@router.post("/prediction")
def log_prediction(data: PredictionLog):
    return MonitoringService.ingest_prediction(data)


# 2️⃣ Autonomous analysis (ONLY model URL)
class MonitoringRequest(BaseModel):
    prediction_url: HttpUrl
  
@router.post("/analyze")
def analyze_model(request: MonitoringRequest):
    print("🔥 ANALYZE ENDPOINT HIT")
    print("MODEL URL:", request.prediction_url)

    service = InvestigationService()
    result = service.investigate(
        model_url=str(request.prediction_url)
    )

    # ✅ FIX: align response with dashboard expectations
    return {
        "metrics": result["current_metrics"],
        "drift": result["drift"],
        "anomalies": result["anomalies"],
        "baseline_exists": result["baseline_exists"],
        "samples_collected": result["samples_collected"],
    }
