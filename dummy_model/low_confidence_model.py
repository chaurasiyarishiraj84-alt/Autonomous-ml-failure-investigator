from fastapi import FastAPI
import random

app = FastAPI()

@app.post("/predict")
def predict():
    return {
        "prediction": "uncertain",
        "confidence": round(random.uniform(0.1, 0.3), 3)
    }
