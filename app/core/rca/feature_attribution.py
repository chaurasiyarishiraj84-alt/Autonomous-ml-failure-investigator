from typing import Dict, Any, List


class FeatureAttributor:
    """
    Rule-based RCA — explains which feature is causing failure.
    Works without SHAP when model internals are not available.
    """

    @staticmethod
    def analyze(
        predictions: List[Dict[str, Any]],
        drift: Dict[str, Any],
        anomalies: List[str],
    ) -> Dict[str, Any]:

        rca = {
            "root_cause": "unknown",
            "confidence": "low",
            "affected_features": [],
            "affected_segment": "unknown",
            "failure_reason": "No failure detected",
            "severity": "none",
        }

        # No issues detected
        if not anomalies and not drift:
            rca["failure_reason"] = "Model operating normally"
            return rca

        reasons = []
        severity = "low"

        # --- Anomaly-based RCA ---
        if "low_confidence" in anomalies:
            reasons.append("Model confidence is below safe threshold")
            rca["root_cause"] = "low_confidence"
            rca["affected_segment"] = "all_predictions"
            severity = "high"

        if "high_error_rate" in anomalies:
            reasons.append("Error rate exceeds acceptable limit")
            rca["root_cause"] = "high_error_rate"
            severity = "high"

        if "no_predictions" in anomalies:
            reasons.append("Model returned no predictions")
            rca["root_cause"] = "model_unavailable"
            severity = "critical"

        # --- Drift-based RCA ---
        conf_dist = drift.get("confidence_distribution", {})
        if conf_dist.get("drift_detected"):
            p_val = conf_dist.get("p_value", "N/A")
            reasons.append(
                f"Confidence distribution drift detected "
                f"(KS p-value={p_val})"
            )
            rca["root_cause"] = "concept_drift"
            rca["affected_segment"] = "confidence_distribution"
            severity = "high"

        conf_var = drift.get("confidence_variance", {})
        if conf_var.get("status") == "drift_detected":
            reasons.append(
                f"Confidence variance exploded: "
                f"baseline={conf_var.get('baseline_std')} → "
                f"current={conf_var.get('current_std')}"
            )
            rca["root_cause"] = "variance_explosion"
            severity = "medium"

        feature_shifts = drift.get("feature_mean_shift", [])
        if feature_shifts:
            top = sorted(
                feature_shifts,
                key=lambda x: x.get("drift_score", 0),
                reverse=True
            )[0]
            reasons.append(
                f"Feature '{top['feature']}' shifted significantly "
                f"(drift_score={top['drift_score']})"
            )
            rca["affected_features"] = [
                f["feature"] for f in feature_shifts
            ]
            rca["root_cause"] = "feature_drift"
            severity = "medium"

        rca["failure_reason"] = " | ".join(reasons) if reasons else "Unknown cause"
        rca["confidence"] = "high" if len(reasons) >= 2 else "medium"
        rca["severity"] = severity

        return rca
    