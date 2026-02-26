from typing import Dict, Any, List
from app.core.recommendation.rule_engine import RecommendationRuleEngine


class RecommendationEngine:
    """
    Produces final, structured recommendations
    based on root cause analysis.
    """

    @staticmethod
    def recommend(rca_output: Dict[str, Any]) -> Dict[str, Any]:
        root_causes: List[str] = rca_output.get("root_causes", [])

        actions = RecommendationRuleEngine.generate(root_causes)

        return {
            "summary": "Recommended actions based on detected issues",
            "root_causes": root_causes,
            "actions": actions
        }
