from typing import Dict, Any, List
import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    """
    Tier-1+ Hybrid Anomaly Detector

    Combines:
    1. Rule-based safety checks (explainable)
    2. ML-based anomaly detection (adaptive)
    """

    def __init__(
        self,
        contamination: float = 0.05,
        random_state: int = 42,
    ):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
        )
        self._is_fitted = False

    # ------------------------
    # ML PART
    # ------------------------
    def fit(self, historical_metrics: List[Dict[str, Any]]):
        """
        Learn normal behavior from historical metrics.
        """
        X = self._to_matrix(historical_metrics)
        self.model.fit(X)
        self._is_fitted = True

    def detect_ml(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Detect anomalies using ML.
        """
        if not self._is_fitted:
            return []

        X = self._to_matrix([metrics])
        prediction = self.model.predict(X)

        if prediction[0] == -1:
            return ["anomalous_behavior"]

        return []

    # ------------------------
    # RULE-BASED PART
    # ------------------------
    @staticmethod
    def detect_rules(metrics: Dict[str, Any]) -> List[str]:
        """
        Rule-based anomaly detection (Tier-1 safe).
        """
        anomalies = []

        if metrics.get("total_samples", 0) == 0:
            anomalies.append("no_predictions")

        avg_conf = metrics.get("avg_confidence")
        if avg_conf is not None and avg_conf < 0.5:
            anomalies.append("low_confidence")

        error_rate = metrics.get("error_rate")
        if error_rate is not None and error_rate > 0.3:
            anomalies.append("high_error_rate")

        return anomalies

    # ------------------------
    # FINAL ENTRY POINT
    # ------------------------
    def detect(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Unified anomaly detection (rules + ML).
        """
        anomalies = []

        anomalies.extend(self.detect_rules(metrics))
        anomalies.extend(self.detect_ml(metrics))

        return list(set(anomalies))  # remove duplicates

    # ------------------------
    # UTIL
    # ------------------------
    @staticmethod
    def _to_matrix(metrics_list: List[Dict[str, Any]]) -> np.ndarray:
        return np.array([
            [
                m.get("avg_confidence", 0.0),
                m.get("confidence_std", 0.0),
                m.get("total_samples", 0.0),
            ]
            for m in metrics_list
        ])
