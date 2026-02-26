import requests
from typing import List, Dict, Any


class ModelProber:
    """
    Safely calls external ML model APIs and collects predictions
    without crashing the backend.
    """

    @staticmethod
    def probe(
        model_url: str,
        test_inputs: List[Dict[str, Any]],
        timeout: int = 5,
    ) -> List[Dict[str, Any]]:

        responses: List[Dict[str, Any]] = []

        for payload in test_inputs:
            try:
                response = requests.post(
                    model_url,
                    json=payload,
                    timeout=timeout
                )

                # Do NOT crash on non-200
                if response.status_code != 200:
                    responses.append({
                        "error": True,
                        "status_code": response.status_code,
                        "payload": payload,
                        "message": response.text
                    })
                    continue

                # Try to parse JSON safely
                try:
                    data = response.json()
                except Exception:
                    data = {
                        "error": True,
                        "message": "Non-JSON response returned"
                    }

                responses.append(data)

            except requests.exceptions.RequestException as e:
                # Connection / timeout / DNS errors
                responses.append({
                    "error": True,
                    "payload": payload,
                    "message": str(e)
                })

        return responses
