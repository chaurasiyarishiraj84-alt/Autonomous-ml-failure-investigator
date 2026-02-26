from typing import Dict, Any


class DeployManager:
    """
    Handles deployment & rollback
    """

    @staticmethod
    def backup_current(model_id: str):
        return f"{model_id}_backup_saved"

    @staticmethod
    def deploy(model_id: str, version: str):
        return f"{model_id} deployed with version {version}"

    @staticmethod
    def rollback(model_id: str):
        return f"{model_id} rolled back to previous version"
