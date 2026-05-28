import pickle

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title="AI Fraud Detection API")
Instrumentator().instrument(app).expose(app)


with open("src/model_training/fraud_model.pkl", "rb") as file:
    model = pickle.load(file)


class Transaction(BaseModel):
    amount: float
    failed_attempts: int
    is_international: int


@app.get("/")
def home():
    return {"message": "AI Fraud Detection API is running"}


@app.post("/predict")
def predict(transaction: Transaction):

    high_amount = 1 if transaction.amount > 100000 else 0

    risk_score = (
        high_amount
        + transaction.is_international
        + transaction.failed_attempts
    )

    features = [[
        transaction.amount,
        transaction.failed_attempts,
        transaction.is_international,
        high_amount,
        risk_score
    ]]

    prediction = model.predict(features)[0]

    result = "Fraud" if prediction == 1 else "Normal"

    return {
        "prediction": int(prediction),
        "result": result
    }