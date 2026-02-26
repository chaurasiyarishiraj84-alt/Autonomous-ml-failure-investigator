from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="Dummy ML Model")

class ModelInput(BaseModel):
    text: str

@app.post("/predict")
def predict(data: ModelInput):
    return {
        "prediction": random.choice(["spam", "ham"]),
        "confidence": round(random.uniform(0.7, 0.99), 2)
    }
