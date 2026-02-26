from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class PredictionLog(BaseModel):
    model_id: str
    input_features: Dict[str, Any]
    prediction: Any
    confidence: float | None = None
    ground_truth: Any | None = None
    timestamp: datetime
