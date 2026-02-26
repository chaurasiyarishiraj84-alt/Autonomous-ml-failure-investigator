from typing import Dict, Any


class AccuracyDriftDetector:
    """
    Detects accuracy degradation against baseline.
    Tier-1 safe, rule-based.
    """

    def __init__(self, drop_threshold: float = 0.1):
        """
        drop_threshold: relative accuracy drop (e.g. 0.1 = 10%)
        """
        self.drop_threshold = drop_threshold

    def detect(
        self,
        baseline_metrics: Dict[str, Any],
        current_metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        baseline_acc = baseline_metrics.get("accuracy")
        current_acc = current_metrics.get("accuracy")

        if baseline_acc is None or current_acc is None:
            return {"status": "unknown"}

        drop = baseline_acc - current_acc
        relative_drop = drop / baseline_acc if baseline_acc > 0 else 0

        if relative_drop >= self.drop_threshold:
            return {
                "status": "degraded",
                "baseline_accuracy": baseline_acc,
                "current_accuracy": current_acc,
                "relative_drop": round(relative_drop, 4),
            }

        return {
            "status": "stable",
            "baseline_accuracy": baseline_acc,
            "current_accuracy": current_acc,
            "relative_drop": round(relative_drop, 4),
        }
