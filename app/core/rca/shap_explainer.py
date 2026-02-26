from typing import Dict, Any


class ShapExplainer:
    """
    Placeholder for SHAP-based feature attribution
    """

    @staticmethod
    def explain(model_id: str) -> Dict[str, Any]:
        # Placeholder — real SHAP added later
        return {
            "top_features": [
                {"feature": "amount", "impact": "high"},
                {"feature": "country", "impact": "medium"},
            ],
            "note": "Feature importance based on recent predictions"
        }
