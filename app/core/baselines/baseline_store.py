from typing import Dict, Any


class BaselineStore:
    """
    In-memory baseline store (DB later)
    """

    _store: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def save(cls, model_id: str, baseline: Dict[str, Any]):
        cls._store[model_id] = baseline

    @classmethod
    def get(cls, model_id: str):
        return cls._store.get(model_id)
