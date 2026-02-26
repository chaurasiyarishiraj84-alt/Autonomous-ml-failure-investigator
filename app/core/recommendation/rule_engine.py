from typing import List, Dict, Any


class RecommendationRuleEngine:
    """
    Maps root causes to specific actionable recommendations.
    """

    @staticmethod
    def generate(
        root_causes: List[str] = [],
        rca: Dict[str, Any] = {},
        drift: Dict[str, Any] = {},
        anomalies: List[str] = [],
        metrics: Dict[str, Any] = {},
    ) -> List[Dict[str, str]]:

        actions = []

        # --- From old root_causes strings (keep backward compat) ---
        for cause in root_causes:
            if "data distribution drift" in cause.lower():
                actions.append({
                    "action": "Retrain model with recent data",
                    "detail": "Input data drift detected — retrain with last 30 days of production data.",
                    "priority": "HIGH",
                    "type": "retrain",
                })
            if "confidence significantly dropped" in cause.lower():
                actions.append({
                    "action": "Evaluate model performance",
                    "detail": "Prediction quality degraded — review model accuracy on recent samples.",
                    "priority": "HIGH",
                    "type": "evaluate",
                })
            if "no incoming prediction data" in cause.lower():
                actions.append({
                    "action": "Check prediction pipeline",
                    "detail": "Pipeline may be broken — verify model endpoint and data flow.",
                    "priority": "CRITICAL",
                    "type": "rollback",
                })
            if "predictions unreliable" in cause.lower():
                actions.append({
                    "action": "Pause model usage",
                    "detail": "Low confidence predictions — rollback to last stable model version.",
                    "priority": "CRITICAL",
                    "type": "rollback",
                })

        # --- From RCA root cause ---
        root_cause = rca.get("root_cause", "unknown")

        if root_cause == "concept_drift":
            actions.append({
                "action": "Retrain model",
                "detail": "Confidence distribution shifted — retrain with last 30 days of data.",
                "priority": "HIGH",
                "type": "retrain",
            })
        elif root_cause == "feature_drift":
            affected = ", ".join(rca.get("affected_features", [])) or "unknown"
            actions.append({
                "action": "Fix feature pipeline",
                "detail": f"Features [{affected}] drifted — check preprocessing steps.",
                "priority": "HIGH",
                "type": "data_fix",
            })
        elif root_cause == "low_confidence":
            actions.append({
                "action": "Retrain with diverse data",
                "detail": f"Confidence below threshold — add edge case examples to training set.",
                "priority": "HIGH",
                "type": "retrain",
            })
        elif root_cause == "high_error_rate":
            actions.append({
                "action": "Investigate misclassified samples",
                "detail": "Error rate too high — review recent prediction logs for failure patterns.",
                "priority": "HIGH",
                "type": "data_fix",
            })
        elif root_cause == "model_unavailable":
            actions.append({
                "action": "Rollback to previous version",
                "detail": "Model not responding — immediately rollback to last stable version.",
                "priority": "CRITICAL",
                "type": "rollback",
            })
        elif root_cause == "variance_explosion":
            actions.append({
                "action": "Recalibrate thresholds",
                "detail": "Confidence variance exploded — tune decision thresholds.",
                "priority": "MEDIUM",
                "type": "threshold_tune",
            })

        # --- From drift signals ---
        conf_dist = drift.get("confidence_distribution", {})
        if conf_dist.get("drift_detected") and root_cause == "unknown":
            actions.append({
                "action": "Schedule retraining",
                "detail": f"KS-test p-value={conf_dist.get('p_value')} — distribution shift detected.",
                "priority": "HIGH",
                "type": "retrain",
            })

        # --- From anomalies ---
        if "no_predictions" in anomalies and root_cause == "unknown":
            actions.append({
                "action": "Check model endpoint",
                "detail": "No predictions returned — verify model API is running correctly.",
                "priority": "CRITICAL",
                "type": "rollback",
            })

        # --- No issues ---
        if not actions:
            actions.append({
                "action": "No action required",
                "detail": "Model is performing within healthy parameters.",
                "priority": "NONE",
                "type": "none",
            })

        # Sort by priority
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "NONE": 4}
        actions.sort(key=lambda x: priority_order.get(x.get("priority", "NONE"), 99))

        return actions