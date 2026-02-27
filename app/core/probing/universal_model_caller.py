import requests
from typing import Dict, Any, Optional
from urllib.parse import urlparse

# Known payload formats for auto-detection
COMMON_PAYLOADS = [
    {"text": "test input"},
    {"input": "test input"},
    {"inputs": "test input"},
    {"data": ["test input"]},
]


class UniversalModelCaller:
    """
    Universal ML model caller.

    Guarantees output:
    {
        "prediction": str | None,
        "confidence": float
    }
    """

    _payload_cache: Dict[str, Dict[str, Any]] = {}

    # -------------------------------------------------
    @classmethod
    def call(
        cls,
        model_url: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        parsed = urlparse(model_url)

        try:
            # Hugging Face Inference API
            if "huggingface.co" in parsed.netloc:
                return cls._call_huggingface(model_url, payload)

            # Gradio endpoint
            if "/run/predict" in model_url:
                return cls._call_gradio(model_url, payload)

            # HuggingFace Space (*.hf.space)
            if "hf.space" in parsed.netloc:
                return cls._call_hf_space(model_url, payload)

            # Default REST / Dummy / Unknown
            return cls._call_rest(model_url, payload)

        except Exception as e:
            return {
                "prediction": None,
                "confidence": 0.0,
                "error": str(e),
            }

    # -------------------------------------------------
    @classmethod
    def _call_rest(
        cls,
        model_url: str,
        payload: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if payload is None:
            payload = cls._detect_payload(model_url)

        response = requests.post(
            model_url,
            json=payload,
            timeout=15
        )
        response.raise_for_status()

        return cls._normalize(response.json())

    # -------------------------------------------------
    @classmethod
    def _call_hf_space(
        cls,
        model_url: str,
        payload: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Handles HuggingFace Space REST APIs (*.hf.space)
        """
        if payload is None:
            payload = cls._detect_payload(model_url)

        response = requests.post(
            model_url,
            json=payload,
            timeout=20
        )
        response.raise_for_status()

        return cls._normalize(response.json())

    # -------------------------------------------------
    @classmethod
    def _detect_payload(cls, model_url: str) -> Dict[str, Any]:
        if model_url in cls._payload_cache:
            return cls._payload_cache[model_url]

        for payload in COMMON_PAYLOADS:
            try:
                r = requests.post(model_url, json=payload, timeout=6)
                if r.status_code == 200:
                    cls._payload_cache[model_url] = payload
                    return payload
            except Exception:
                continue

        # Safe fallback
        fallback = {"text": "test"}
        cls._payload_cache[model_url] = fallback
        return fallback

    # -------------------------------------------------
    @staticmethod
    def _call_huggingface(
        model_url: str,
        payload: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if payload is None:
            payload = {"inputs": "test input"}

        response = requests.post(
            model_url,
            json=payload,
            headers={"Accept": "application/json"},
            timeout=20
        )
        response.raise_for_status()

        data = response.json()

        if isinstance(data, list) and data:
            top = data[0]
            return {
                "prediction": top.get("label", "unknown"),
                "confidence": float(top.get("score", 0.5)),
            }

        return {"prediction": "unknown", "confidence": 0.5}

    # -------------------------------------------------
    @staticmethod
    def _call_gradio(
        model_url: str,
        payload: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if payload is None:
            payload = {"data": ["test input"]}

        response = requests.post(
            model_url,
            json=payload,
            timeout=20
        )
        response.raise_for_status()

        data = response.json()
        output = data.get("data", [{}])[0]

        return {
            "prediction": (
                output.get("label")
                or output.get("prediction")
                or "unknown"
            ),
            "confidence": float(output.get("confidence", 0.5)),
        }

    # -------------------------------------------------
    @staticmethod
    def _normalize(data: Any) -> Dict[str, Any]:
        """
        Normalize ANY model output safely.
        Uses explicit None checks to avoid falsy float issues.
        """

        # If list → take first element
        if isinstance(data, list) and data:
            data = data[0]

        if not isinstance(data, dict):
            return {
                "prediction": str(data),
                "confidence": 0.5,
            }

        # ✅ Explicit None check — fixes 0.0/0.1 being treated as falsy
        confidence = data.get("confidence")
        if confidence is None:
            confidence = data.get("score")
        if confidence is None:
            confidence = data.get("probability")
        if confidence is None:
            confidence = 0.5

        prediction = (
            data.get("prediction")
            or data.get("label")
            or data.get("output")
            or "unknown"
        )

        return {
            "prediction": prediction,
            "confidence": float(confidence),
        }
