from fastapi import FastAPI
import random

app = FastAPI()

@app.post("/predict")
def predict():
    return {
        "prediction": "positive",
        "confidence": round(random.uniform(0.8, 0.95), 3)
    }
