from typing import Dict, Any


class MetricChecker:
    """
    Compares live metrics against stored baseline
    """

    @staticmethod
    def check(baseline: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
        results = {}

        # 1️⃣ Confidence degradation check
        if (
            baseline.get("avg_confidence") is not None
            and current.get("avg_confidence") is not None
        ):
            drop = baseline["avg_confidence"] - current["avg_confidence"]

            if drop > 0.1:
                results["confidence"] = {
                    "status": "degraded",
                    "baseline": baseline["avg_confidence"],
                    "current": current["avg_confidence"],
                    "drop": drop,
                }
            else:
                results["confidence"] = {
                    "status": "normal",
                    "drop": drop,
                }

        # 2️⃣ Latency regression check
        if (
            baseline.get("avg_latency_ms") is not None
            and current.get("avg_latency_ms") is not None
        ):
            increase = current["avg_latency_ms"] - baseline["avg_latency_ms"]

            if increase > 50:
                results["latency"] = {
                    "status": "degraded",
                    "baseline": baseline["avg_latency_ms"],
                    "current": current["avg_latency_ms"],
                    "increase_ms": increase,
                }
            else:
                results["latency"] = {
                    "status": "normal",
                    "increase_ms": increase,
                }

        return results
