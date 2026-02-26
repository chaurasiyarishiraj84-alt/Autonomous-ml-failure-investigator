from typing import Dict, Any, List
from app.schemas.monitoring import PredictionLog
from app.utils.logger import logger
from app.core.detection.drift_detector import DriftDetector
from app.core.probing.universal_model_caller import UniversalModelCaller
from app.core.metrics.baseline_builder import BaselineBuilder


class MonitoringService:

    @staticmethod
    def ingest_prediction(data: PredictionLog):
        logger.info(
            f"Received prediction | model={data.model_id} | prediction={data.prediction}"
        )

        return {
            "status": "received",
            "model_id": data.model_id,
            "timestamp": data.timestamp,
        }

    @staticmethod
    def analyze_model(
        prediction_url: str,
        baseline_metrics: Dict[str, Any] | None = None,
        probe_runs: int = 5,
    ) -> Dict[str, Any]:
        """
        End-to-end analysis:
        1. Auto-detect payload
        2. Call model multiple times
        3. Build current metrics
        4. Detect drift
        """

        logger.info(f"Starting analysis for model: {prediction_url}")

        # 1️⃣ Call model multiple times
        predictions: List[Dict[str, Any]] = []

        for _ in range(probe_runs):
            response = UniversalModelCaller.call(prediction_url)
            predictions.append(response)

        # 2️⃣ Build current metrics
        current_metrics = BaselineBuilder.build(predictions)

        # 3️⃣ Drift detection
        drift_report = {}
        if baseline_metrics:
            detector = DriftDetector()
            drift_report = detector.detect(baseline_metrics, current_metrics)

            if drift_report:
                logger.warning(f"Drift detected: {drift_report}")

        return {
            "current_metrics": current_metrics,
            "drift": drift_report,
            "samples_collected": len(predictions),
        }
