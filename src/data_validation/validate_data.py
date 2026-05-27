import pandas as pd


df = pd.read_csv("data/raw/transactions_from_db.csv")


validation_results = []


validation_results.append({
    "check": "transaction_id should not be null",
    "success": df["transaction_id"].notnull().all()
})

validation_results.append({
    "check": "amount should be greater than or equal to 0",
    "success": (df["amount"] >= 0).all()
})

validation_results.append({
    "check": "is_fraud should be only 0 or 1",
    "success": df["is_fraud"].isin([0, 1]).all()
})

validation_results.append({
    "check": "failed_attempts should be between 0 and 5",
    "success": df["failed_attempts"].between(0, 5).all()
})


print("\nValidation Results:\n")

all_passed = True

for result in validation_results:
    print(f"{result['check']} : {result['success']}")

    if result["success"] is False:
        all_passed = False


if all_passed:
    print("\nAll data validation checks passed.")
else:
    print("\nSome data validation checks failed.")