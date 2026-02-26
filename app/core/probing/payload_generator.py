from typing import List, Dict, Any
import random
import string


class PayloadGenerator:
    """
    Generates diverse test payloads for probing ML model robustness.
    """

    @staticmethod
    def generate() -> List[Dict[str, Any]]:
        payloads: List[Dict[str, Any]] = []

        # Normal inputs
        payloads.extend([
            {"text": "hello"},
            {"text": "free money offer"},
            {"text": "meeting at 5 pm"},
        ])

        # Edge cases
        payloads.extend([
            {"text": ""},
            {"text": "   "},
            {"text": "!" * 50},
            {"text": "a" * 300},
        ])

        # Adversarial / tricky
        payloads.extend([
            {"text": "DROP TABLE users;"},
            {"text": "The movie was not bad"},
            {"text": "Congratulations!!! You won $$$"},
        ])

        # Random noise
        for _ in range(3):
            payloads.append({
                "text": "".join(
                    random.choice(string.ascii_letters)
                    for _ in range(random.randint(5, 40))
                )
            })

        return payloads
