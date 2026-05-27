import pandas as pd


df = pd.read_csv("data/raw/transactions_from_db.csv")


df["high_amount"] = df["amount"].apply(
    lambda amount: 1 if amount > 100000 else 0
)


df["risk_score"] = (
    df["high_amount"]
    + df["is_international"]
    + df["failed_attempts"]
)


df.to_csv("data/processed/transactions_features.csv", index=False)


print("Feature engineering completed.")
print("Processed data saved to data/processed/transactions_features.csv")