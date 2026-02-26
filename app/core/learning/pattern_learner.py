from typing import Dict, Any, List
from collections import Counter
from app.core.learning.failure_memory import FailureMemory


class PatternLearner:
    """
    Learns recurring failure patterns and effective actions
    from historical incidents.
    
    """

    @staticmethod
    def learn(
        min_occurrences: int = 2
    ) -> Dict[str, Any]:
        """
        Extracts common root causes and actions
        seen across past failures.
        """

        history = FailureMemory.history()

        if not history:
            return {
                "status": "no_history",
                "message": "No failure data available yet"
            }

        root_causes: List[str] = []
        actions: List[str] = []

        for event in history:
            root_causes.extend(event.get("root_causes", []))
            actions.extend(
                action.get("action")
                for action in event.get("actions", [])
                if action.get("action")
            )

        root_cause_counter = Counter(root_causes)
        action_counter = Counter(actions)

        common_causes = [
            cause for cause, count in root_cause_counter.items()
            if count >= min_occurrences
        ]

        common_actions = [
            action for action, count in action_counter.items()
            if count >= min_occurrences
        ]

        return {
            "status": "learned",
            "total_incidents": len(history),
            "common_root_causes": common_causes,
            "common_actions": common_actions
        }
