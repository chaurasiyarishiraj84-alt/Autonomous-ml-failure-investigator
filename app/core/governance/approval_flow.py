import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class ApprovalFlow:
    """
    Stores and manages human approval decisions.
    """

    LOG_FILE = Path("data/audit_logs/approvals.json")

    @classmethod
    def _ensure_log_file(cls):
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not cls.LOG_FILE.exists():
            with open(cls.LOG_FILE, "w") as f:
                json.dump([], f)

    @classmethod
    def log_decision(
        cls,
        action: str,
        decision: str,  # "approved" or "rejected"
        reason: str = "",
    ) -> Dict[str, Any]:
        cls._ensure_log_file()

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "decision": decision,
            "reason": reason,
        }

        with open(cls.LOG_FILE, "r") as f:
            logs = json.load(f)

        logs.append(record)

        with open(cls.LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)

        return record

    @classmethod
    def get_logs(cls) -> List[Dict[str, Any]]:
        cls._ensure_log_file()
        with open(cls.LOG_FILE, "r") as f:
            return json.load(f)
        