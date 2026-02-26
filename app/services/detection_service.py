from typing import Dict, Any, List
from app.core.detection.anomaly_detector import AnomalyDetector


class DetectionService:
    def __init__(self):
        self.detector = AnomalyDetector()

    def detect(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Entry point used by InvestigationService
        """
        return self.detector.detect(metrics)
