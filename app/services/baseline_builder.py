from typing import Dict, Any, List
import numpy as np


class BaselineBuilder:
    @staticmethod
    def build(predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        confidences = [
            p.get("confidence", 0.0)
            for p in predictions
            if isinstance(p, dict)
        ]

        if not confidences:
            return {
                "avg_confidence": 0.0,
                "confidence_std": 0.0,
                "total_samples": 0,
                "error_rate": 1.0,
                "confidence_scores": [],
                "features": {},
            }

        return {
            "avg_confidence": float(np.mean(confidences)),
            "confidence_std": float(np.std(confidences)),
            "total_samples": len(confidences),
            "error_rate": 0.0,
            "confidence_scores": confidences,
            "features": {},
        }
