import json
import pandas as pd
from scipy.stats import ks_2samp


REFERENCE_DATA_PATH = "data/processed/transactions_features.csv"
CURRENT_DATA_PATH = "data/production/current_transactions.csv"
DRIFT_RESULT_PATH = "src/monitoring/reports/drift_result.json"

features = [
    "amount",
    "failed_attempts",
    "is_international",
    "high_amount",
    "risk_score"
]

reference_data = pd.read_csv(REFERENCE_DATA_PATH)[features]
current_data = pd.read_csv(CURRENT_DATA_PATH)[features]

drift_results = {}

for feature in features:
    stat, p_value = ks_2samp(
        reference_data[feature],
        current_data[feature]
    )

    drift_detected = p_value < 0.05

    drift_results[feature] = {
        "p_value": float(p_value),
        "drift_detected": bool(drift_detected)
    }

total_drifted_features = sum(
    1 for result in drift_results.values()
    if result["drift_detected"]
)

overall_drift_detected = total_drifted_features > 0

final_result = {
    "drift_detected": overall_drift_detected,
    "drifted_features": total_drifted_features,
    "total_features": len(features),
    "features": drift_results
}

with open(DRIFT_RESULT_PATH, "w") as file:
    json.dump(final_result, file, indent=4)

print("\nData Drift Detection Result")
print("==========================")

for feature, result in drift_results.items():
    status = "YES" if result["drift_detected"] else "NO"
    print(f"{feature}: Drift = {status}, p-value = {result['p_value']:.5f}")

print("\nFinal Result")
print("============")
print(f"Drift detected: {'YES' if overall_drift_detected else 'NO'}")
print(f"Drifted features: {total_drifted_features}/{len(features)}")
print(f"Result saved at: {DRIFT_RESULT_PATH}")