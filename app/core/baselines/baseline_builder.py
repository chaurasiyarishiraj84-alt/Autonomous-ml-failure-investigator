from typing import List, Dict, Any
from statistics import mean, pstdev
from app.schemas.monitoring import PredictionLog


class BaselineBuilder:
    """
    Builds baseline from historical prediction logs
    """

    @staticmethod
    def build(logs: List[PredictionLog]) -> Dict[str, Any]:
        confidences = [
            log.confidence for log in logs if log.confidence is not None
        ]

        baseline = {
            "total_samples": len(logs),
            "avg_confidence": mean(confidences) if confidences else None,
            "confidence_std": pstdev(confidences) if len(confidences) > 1 else None,
        }

        return baseline
