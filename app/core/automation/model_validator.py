from typing import Dict, Any


class ModelValidator:
    """
    Validates whether a new model is safe to deploy
    compared to the currently running model.
    """

    @staticmethod
    def validate(
        old_metrics: Dict[str, Any],
        new_metrics: Dict[str, Any],
    ) -> bool:
        """
        Returns True only if the new model is not worse
        than the old model on critical metrics.
        """

        # 1️⃣ Confidence must not degrade
        old_conf = old_metrics.get("avg_confidence")
        new_conf = new_metrics.get("avg_confidence")

        if old_conf is not None and new_conf is not None:
            if new_conf < old_conf:
                return False

        # 2️⃣ Accuracy must meet minimum bar (if available)
        new_acc = new_metrics.get("accuracy")
        if new_acc is not None and new_acc < 0.7:
            return False

        return True
