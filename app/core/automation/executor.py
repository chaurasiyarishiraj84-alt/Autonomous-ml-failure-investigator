from typing import Dict, Any
from app.core.automation.retrain_pipeline import RetrainPipeline
from app.core.automation.model_validator import ModelValidator
from app.core.automation.deploy_manager import DeployManager
from app.utils.logger import logger


class AutomationExecutor:
    """
    Executes decisions safely and sequentially.
    """

    @staticmethod
    def execute(decision: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a system decision.

        context must contain:
        - model_id
        - baseline_metrics
        - current_metrics
        """

        action = decision.get("action")
        model_id = context.get("model_id")

        logger.info(f"Automation decision received: {action} | model={model_id}")

        if action == "monitor":
            return {
                "status": "no_action",
                "message": "Monitoring only",
            }

        if action == "pause_model":
            result = DeployManager.rollback(model_id)
            return {
                "status": "paused",
                "result": result,
            }

        if action == "rollback":
            result = DeployManager.rollback(model_id)
            return {
                "status": "rolled_back",
                "result": result,
            }

        if action == "retrain_model":
            retrain_result = RetrainPipeline.retrain(model_id)

            old_metrics = context.get("baseline_metrics", {})
            new_metrics = context.get("current_metrics", {})

            is_valid = ModelValidator.validate(old_metrics, new_metrics)

            if not is_valid:
                rollback_result = DeployManager.rollback(model_id)
                return {
                    "status": "retrain_failed",
                    "rollback": rollback_result,
                }

            deploy_result = DeployManager.deploy(
                model_id,
                retrain_result.get("new_model_version"),
            )

            return {
                "status": "retrained_and_deployed",
                "deploy": deploy_result,
            }

        return {
            "status": "unknown_action",
            "action": action,
        }
