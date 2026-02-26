from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

router = APIRouter(prefix="/models", tags=["models"])


class ModelRegistration(BaseModel):
    model_name: str
    prediction_url: HttpUrl
    description: str | None = None


@router.post("/register")
def register_model(data: ModelRegistration):
    """
    Registers an external model for monitoring
    """
    return {
        "status": "registered",
        "model_name": data.model_name,
        "prediction_url": data.prediction_url,
    }
