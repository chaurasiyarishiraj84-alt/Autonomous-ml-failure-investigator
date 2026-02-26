from typing import Dict, Any, List
from datetime import datetime
import uuid


class FailureMemory:
    """
    Stores and retrieves historical failure events.
    
    """

    _memory: List[Dict[str, Any]] = []

    @classmethod
    def record(
        cls,
        model_id: str,
        root_causes: List[str],
        actions: List[Dict[str, Any]],
        metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Records a failure incident with metadata.
        """

        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "model_id": model_id,
            "root_causes": root_causes,
            "actions": actions,
            "metrics": metrics,
        }

        cls._memory.append(event)
        return event

    @classmethod
    def history(cls) -> List[Dict[str, Any]]:
        """
        Returns all recorded failures.
        """
        return cls._memory

    @classmethod
    def find_similar(cls, root_causes: List[str]) -> List[Dict[str, Any]]:
        """
        Finds past failures with overlapping root causes.
        """

        matches = []

        for event in cls._memory:
            overlap = set(event.get("root_causes", [])) & set(root_causes)
            if overlap:
                matches.append(event)

        return matches
