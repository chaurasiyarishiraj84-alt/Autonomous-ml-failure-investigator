from fastapi import FastAPI
import random

app = FastAPI()

@app.post("/predict")
def predict():
    return {
        "prediction": random.choice(["A", "B", "C"]),
        "confidence": round(random.uniform(0.0, 1.0), 3)
    }
