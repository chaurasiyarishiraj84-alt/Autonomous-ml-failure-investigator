from typing import Dict, Any, List
import time
import requests


class ModelProber:
    """
    Probes an external model API in read-only mode.
    """

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def probe(
        self,
        prediction_url: str,
        test_payloads: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Sends test payloads to the model and collects metrics.
        """

        total_latency = 0.0
        confidences = []
        successful_calls = 0
        errors = 0

        for payload in test_payloads:
            try:
                start = time.time()
                response = requests.post(
                    prediction_url,
                    json=payload,
                    timeout=self.timeout,
                )
                latency = time.time() - start
                total_latency += latency

                if response.status_code != 200:
                    errors += 1
                    continue

                result = response.json()
                successful_calls += 1

                # Optional confidence extraction
                if isinstance(result, dict) and "confidence" in result:
                    confidences.append(result["confidence"])

            except Exception:
                errors += 1

        avg_latency = (
            total_latency / successful_calls if successful_calls > 0 else None
        )

        avg_confidence = (
            sum(confidences) / len(confidences) if confidences else None
        )

        return {
            "total_requests": len(test_payloads),
            "successful_requests": successful_calls,
            "error_requests": errors,
            "avg_latency": avg_latency,
            "avg_confidence": avg_confidence,
        }
