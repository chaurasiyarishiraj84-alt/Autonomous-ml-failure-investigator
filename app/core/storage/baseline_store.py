import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List


class BaselineStore:
    BASE_DIR = Path("baselines")

    @classmethod
    def _model_dir(cls, model_url: str) -> Path:
        model_hash = hashlib.md5(model_url.encode()).hexdigest()
        return cls.BASE_DIR / model_hash

    @classmethod
    def save(cls, model_url: str, metrics: Dict[str, Any]) -> None:
        model_dir = cls._model_dir(model_url)
        model_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        baseline_file = model_dir / f"baseline_{timestamp}.json"

        with open(baseline_file, "w") as f:
            json.dump(metrics, f, indent=2)

    @classmethod
    def load(cls, model_url: str) -> Optional[Dict[str, Any]]:
        model_dir = cls._model_dir(model_url)

        if not model_dir.exists():
            return None

        baselines = sorted(model_dir.glob("baseline_*.json"))
        if not baselines:
            return None

        # Load latest baseline
        with open(baselines[-1], "r") as f:
            return json.load(f)

    @classmethod
    def list_versions(cls, model_url: str) -> List[str]:
        model_dir = cls._model_dir(model_url)
        if not model_dir.exists():
            return []

        return [f.name for f in sorted(model_dir.glob("baseline_*.json"))]
