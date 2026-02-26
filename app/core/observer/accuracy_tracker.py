from typing import List, Any, Dict


class AccuracyTracker:
    """
    Tracks model accuracy using ground-truth labels.
    """

    @staticmethod
    def evaluate(
        predictions: List[Any],
        ground_truth: List[Any],
    ) -> Dict[str, float]:
        if not predictions or not ground_truth:
            return {"accuracy": None}

        correct = 0
        total = min(len(predictions), len(ground_truth))

        for p, y in zip(predictions, ground_truth):
            if p == y:
                correct += 1

        accuracy = correct / total if total > 0 else None

        return {
            "accuracy": round(accuracy, 4) if accuracy is not None else None,
            "total_samples": total,
        }
