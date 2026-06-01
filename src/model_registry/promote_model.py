import mlflow
from mlflow.tracking import MlflowClient


# MLflow tracking location
mlflow.set_tracking_uri("file:./mlruns")


MODEL_NAME = "fraud_detection_model"


client = MlflowClient()


# Get all versions of this model
versions = client.search_model_versions(
    f"name='{MODEL_NAME}'"
)


if not versions:
    raise Exception("No registered model versions found")


# Find latest registered version
latest_version = max(
    [int(model.version) for model in versions]
)


print(f"Latest model version found: {latest_version}")


# Promote latest version to Production
client.transition_model_version_stage(
    name=MODEL_NAME,
    version=latest_version,
    stage="Production",
    archive_existing_versions=True
)


print(
    f"Model {MODEL_NAME} version {latest_version} promoted to Production"
)