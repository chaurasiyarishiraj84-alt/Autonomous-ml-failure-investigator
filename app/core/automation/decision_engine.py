from typing import Dict, Any, List


class DecisionEngine:
    """
    Makes safe, explainable decisions based on:
    - Drift signals
    - Anomalies
    - Root cause analysis
    """

    @staticmethod
    def decide(
        drift_signals: Dict[str, Any],
        anomalies: List[str],
        root_causes: List[str],
    ) -> Dict[str, Any]:
        """
        Returns a single system decision.
        """

        # Default safe behavior
        decision = {
            "action": "monitor",
            "reason": "No critical issues detected",
            "confidence": "low",
        }

        # 🚨 Critical pipeline failure
        if "no_predictions" in anomalies:
            return {
                "action": "rollback",
                "reason": "Prediction pipeline failure detected",
                "confidence": "high",
            }

        # 🚨 Unreliable predictions
        if "low_confidence" in anomalies:
            return {
                "action": "pause_model",
                "reason": "Model predictions unreliable",
                "confidence": "high",
            }

        # ⚠️ Data or model drift
        if drift_signals:
            return {
                "action": "retrain_model",
                "reason": "Model or data drift detected",
                "confidence": "medium",
            }

        # ℹ️ Issues detected but not critical
        if root_causes:
            return {
                "action": "investigate",
                "reason": "Non-critical issues detected",
                "confidence": "low",
            }

        return decision
