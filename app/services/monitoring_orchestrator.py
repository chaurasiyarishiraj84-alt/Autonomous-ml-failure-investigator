from typing import Dict, Any, List

from app.core.observer.model_prober import ModelProber
from app.core.observer.accuracy_tracker import AccuracyTracker

from app.core.detection.drift_detector import DriftDetector
from app.core.detection.anomaly_detector import AnomalyDetector
from app.core.detection.accuracy_drift_detector import AccuracyDriftDetector

from app.core.rca.root_cause_analyzer import RootCauseAnalyzer
from app.core.recommendation.recommender import RecommendationEngine


class MonitoringOrchestrator:
    """
    End-to-end monitoring and decision pipeline
    """

    def __init__(self):
        self.prober = ModelProber()
        self.drift_detector = DriftDetector()
        self.accuracy_drift_detector = AccuracyDriftDetector()

    def run(
        self,
        prediction_url: str,
        test_payloads: List[Dict[str, Any]],
        baseline_metrics: Dict[str, Any],
        ground_truth: List[Any] | None = None,
    ) -> Dict[str, Any]:

        # 1️⃣ Probe model
        probe_metrics = self.prober.probe(prediction_url, test_payloads)

        # 2️⃣ Accuracy tracking
        accuracy_metrics = (
            AccuracyTracker.evaluate(
                predictions=[p.get("prediction") for p in test_payloads],
                ground_truth=ground_truth,
            )
            if ground_truth
            else {"accuracy": None}
        )

        current_metrics = {**probe_metrics, **accuracy_metrics}

        # 3️⃣ Drift detection
        drift_signals = self.drift_detector.detect(
            baseline=baseline_metrics,
            current=current_metrics,
        )

        accuracy_drift = self.accuracy_drift_detector.detect(
            baseline_metrics,
            current_metrics,
        )

        # 4️⃣ Anomaly detection
        anomalies = AnomalyDetector.detect(current_metrics)

        # 5️⃣ Root cause analysis
        root_causes = RootCauseAnalyzer.analyze(
            baseline=baseline_metrics,
            current=current_metrics,
            drift_signals=drift_signals,
            anomalies=anomalies,
        )

        # 6️⃣ Recommendations
        recommendations = RecommendationEngine.recommend(
            {"root_causes": root_causes}
        )

        return {
            "metrics": current_metrics,
            "drift": drift_signals,
            "accuracy_drift": accuracy_drift,
            "anomalies": anomalies,
            "root_causes": root_causes,
            "recommendations": recommendations,
        }
