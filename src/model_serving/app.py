import os
import csv
import mlflow
import mlflow.pyfunc

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator


mlflow.set_tracking_uri("file:./mlruns")

MODEL_URI = "models:/fraud_detection_model@production"

PRODUCTION_DATA_PATH = "data/production/current_transactions.csv"

app = FastAPI(title="AI Fraud Detection API")
Instrumentator().instrument(app).expose(app)


model = mlflow.pyfunc.load_model(MODEL_URI)


class Transaction(BaseModel):
    amount: float
    failed_attempts: int
    is_international: int


@app.get("/")
def home():
    return {"message": "AI Fraud Detection API is running"}


def save_production_data(transaction, high_amount, risk_score):
    os.makedirs("data/production", exist_ok=True)

    file_exists = os.path.isfile(PRODUCTION_DATA_PATH)
    file_is_empty = os.path.getsize(PRODUCTION_DATA_PATH) == 0 if file_exists else True

    with open(PRODUCTION_DATA_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)

        if file_is_empty:
            writer.writerow([
                "amount",
                "failed_attempts",
                "is_international",
                "high_amount",
                "risk_score"
            ])

        writer.writerow([
            transaction.amount,
            transaction.failed_attempts,
            transaction.is_international,
            high_amount,
            risk_score
        ])


@app.post("/predict")
def predict(transaction: Transaction):

    high_amount = 1 if transaction.amount > 100000 else 0

    risk_score = (
        high_amount
        + transaction.is_international
        + transaction.failed_attempts
    )

    save_production_data(transaction, high_amount, risk_score)

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