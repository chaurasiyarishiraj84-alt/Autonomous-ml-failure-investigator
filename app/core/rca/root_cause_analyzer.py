from typing import Dict, Any, List


class RootCauseAnalyzer:
    """
    Determines WHY a model is failing.
    Rule-based, explainable .
    """

    @staticmethod
    def analyze(
        baseline: Dict[str, Any],
        current: Dict[str, Any],
        drift_signals: Dict[str, Any],
        anomalies: List[str],
    ) -> List[str]:

        causes: List[str] = []

        # 1️⃣ Data distribution drift
        if "confidence_variance" in drift_signals:
            causes.append("Input data distribution drift detected")

        # 2️⃣ Model confidence degradation
        if (
            baseline.get("avg_confidence") is not None
            and current.get("avg_confidence") is not None
        ):
            if current["avg_confidence"] < baseline["avg_confidence"] * 0.8:
                causes.append("Model confidence significantly dropped")

        # 3️⃣ No prediction traffic
        if "no_predictions" in anomalies:
            causes.append("No incoming prediction data")

        # 4️⃣ Severe prediction quality issue
        if "low_confidence" in anomalies:
            causes.append("Model predictions unreliable")

        # 5️⃣ Fallback
        if not causes:
            causes.append("No clear root cause identified")

        return causes
