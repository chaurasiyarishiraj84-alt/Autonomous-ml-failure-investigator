import numpy as np
from typing import Dict, Any, List

from app.core.detection.anomaly_detector import AnomalyDetector
from app.core.detection.drift_detector import DriftDetector
from app.core.storage.baseline_store import BaselineStore
from app.core.probing.universal_model_caller import UniversalModelCaller
from app.services.baseline_builder import BaselineBuilder
from app.core.rca.feature_attribution import FeatureAttributor
from app.core.recommendation.rule_engine import RecommendationRuleEngine


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj


class InvestigationService:
    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.drift_detector = DriftDetector()

    def investigate(
        self,
        model_url: str,
        probe_runs: int = 5,
    ) -> Dict[str, Any]:

        predictions: List[Dict[str, Any]] = []
        confidence_scores: List[float] = []

        # 🔁 Probe model multiple times — no forced payload
        # UniversalModelCaller auto-detects the correct payload
        for _ in range(probe_runs):
            try:
                response = UniversalModelCaller.call(
                    model_url=model_url,
                )
                print(f"✅ Response: {response}")
                predictions.append(response)
                confidence_scores.append(response.get("confidence", 0.0))
            except Exception as e:
                print(f"❌ Model call failed: {e}")
                continue

        # 📊 Current metrics
        current_metrics = BaselineBuilder.build(predictions)
        current_metrics["confidence_scores"] = confidence_scores

        # 📦 Load baseline
        baseline = BaselineStore.load(model_url)

        # 🧠 First run → save baseline
        if baseline is None:
            BaselineStore.save(model_url, current_metrics)
            drift = {}
        else:
            drift = self.drift_detector.detect(
                baseline=baseline,
                current=current_metrics,
            )

        # 🚨 Anomaly detection
        anomalies = self.anomaly_detector.detect(current_metrics)

        # 🧠 Root Cause Analysis
        rca = FeatureAttributor.analyze(
            predictions=predictions,
            drift=drift,
            anomalies=anomalies,
        )

        # 💊 Recommendations
        recommendations = RecommendationRuleEngine.generate(
            rca=rca,
            drift=drift,
            anomalies=anomalies,
            metrics=current_metrics,
        )

        # 📦 Build result
        result = {
            "metrics": current_metrics,
            "current_metrics": current_metrics,
            "baseline_exists": baseline is not None,
            "drift": drift,
            "anomalies": anomalies,
            "rca": rca,
            "recommendations": recommendations,
            "samples_collected": len(predictions),
        }

        return make_json_safe(result)
