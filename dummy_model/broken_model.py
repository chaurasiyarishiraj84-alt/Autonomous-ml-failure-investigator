from fastapi import FastAPI
import time

app = FastAPI()

@app.post("/predict")
def predict():
    time.sleep(15)  # force timeout
    return {"error": "timeout"}
