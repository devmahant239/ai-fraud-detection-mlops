import json


DRIFT_RESULT_PATH = "src/monitoring/reports/drift_result.json"


with open(DRIFT_RESULT_PATH) as file:
    result = json.load(file)


if result["drift_detected"]:
    print("\nRetraining Decision")
    print("===================")
    print("Drift detected: YES")
    print("Action: Retraining required")
else:
    print("\nRetraining Decision")
    print("===================")
    print("Drift detected: NO")
    print("Action: Continue using current production model")