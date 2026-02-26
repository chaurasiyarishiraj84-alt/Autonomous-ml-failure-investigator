from typing import Dict, Any
import numpy as np
from scipy.stats import ks_2samp


class DriftDetector:
    """
    Detects model drift using:

    1. Output-level drift (confidence variance explosion)
    2. Feature-level drift (mean shift)
    3. Statistical distribution drift (KS-test on confidence scores)
    """

    def __init__(
        self,
        confidence_threshold: float = 1.5,
        feature_drift_threshold: float = 0.2,
        significance_level: float = 0.05,
    ):
        self.confidence_threshold = confidence_threshold
        self.feature_drift_threshold = feature_drift_threshold
        self.significance_level = significance_level

    def detect(
        self,
        baseline: Dict[str, Any],
        current: Dict[str, Any],
    ) -> Dict[str, Any]:

        drift_signals: Dict[str, Any] = {}

        
        # 1️⃣ Output-level drift (confidence variance)
        
        base_std = baseline.get("confidence_std")
        curr_std = current.get("confidence_std")

        if (
            isinstance(base_std, (int, float))
            and isinstance(curr_std, (int, float))
            and base_std > 0
        ):
            if curr_std > base_std * self.confidence_threshold:
                drift_signals["confidence_variance"] = {
                    "status": "drift_detected",
                    "baseline_std": round(base_std, 6),
                    "current_std": round(curr_std, 6),
                    "threshold_multiplier": self.confidence_threshold,
                }

        
        # 2️⃣ Feature-level drift (mean shift)
        
        baseline_features = baseline.get("features", {})
        current_features = current.get("features", {})

        feature_drifts = []

        if isinstance(baseline_features, dict) and isinstance(current_features, dict):
            for feature, base_values in baseline_features.items():

                if (
                    feature not in current_features
                    or not base_values
                    or not current_features[feature]
                ):
                    continue

                base_arr = np.array(base_values, dtype=float)
                curr_arr = np.array(current_features[feature], dtype=float)

                base_mean = np.mean(base_arr)
                curr_mean = np.mean(curr_arr)

                if base_mean == 0:
                    drift_score = abs(curr_mean)
                else:
                    drift_score = abs(curr_mean - base_mean) / abs(base_mean)

                if drift_score > self.feature_drift_threshold:
                    feature_drifts.append(
                        {
                            "feature": feature,
                            "baseline_mean": round(float(base_mean), 6),
                            "current_mean": round(float(curr_mean), 6),
                            "drift_score": round(float(drift_score), 6),
                        }
                    )

        if feature_drifts:
            drift_signals["feature_mean_shift"] = feature_drifts

        
        # 3️⃣ Statistical drift (KS-test on confidence scores)
        
        baseline_conf = baseline.get("confidence_scores")
        current_conf = current.get("confidence_scores")

        if (
            isinstance(baseline_conf, list)
            and isinstance(current_conf, list)
            and len(baseline_conf) > 1
            and len(current_conf) > 1
        ):
            stat, p_value = ks_2samp(
                np.array(baseline_conf, dtype=float),
                np.array(current_conf, dtype=float),
            )

            drift_signals["confidence_distribution"] = {
                "method": "KS-test",
                "statistic": round(float(stat), 6),
                "p_value": round(float(p_value), 6),
                "drift_detected": p_value < self.significance_level,
                "significance_level": self.significance_level,
            }

        
        # Final safety net
        
        if not drift_signals:
            drift_signals["status"] = "no_drift_detected"

        return drift_signals
