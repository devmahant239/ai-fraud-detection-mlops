import os
from kfp import dsl, compiler


BASE_IMAGE = os.getenv(
    "BASE_IMAGE",
    "dev239/fraud-detection-api:dev"
)


@dsl.component(base_image=BASE_IMAGE)
def export_data_component():
    import subprocess
    subprocess.run(["python", "src/data_ingestion/export_db_to_csv.py"], check=True)


@dsl.component(base_image=BASE_IMAGE)
def validate_data_component():
    import subprocess
    subprocess.run(["python", "src/data_validation/validate_data.py"], check=True)


@dsl.component(base_image=BASE_IMAGE)
def feature_engineering_component():
    import subprocess
    subprocess.run(["python", "src/feature_engineering/feature_engineering.py"], check=True)


@dsl.component(base_image=BASE_IMAGE)
def train_model_component():
    import subprocess
    subprocess.run(["python", "src/model_training/train_model.py"], check=True)


@dsl.component(base_image=BASE_IMAGE)
def promote_model_component():
    import subprocess
    subprocess.run(["python", "src/model_registry/promote_model.py"], check=True)


@dsl.component(base_image=BASE_IMAGE)
def drift_detection_component():
    import subprocess
    subprocess.run(["python", "src/monitoring/drift_detection.py"], check=True)


@dsl.component(base_image=BASE_IMAGE)
def drift_decision_component():
    import subprocess
    subprocess.run(["python", "src/monitoring/drift_decision.py"], check=True)


@dsl.pipeline(
    name="ai-fraud-detection-mlops-pipeline",
    description="End-to-end MLOps pipeline for fraud detection"
)
def fraud_detection_pipeline():
    export_task = export_data_component()
    validation_task = validate_data_component().after(export_task)
    feature_task = feature_engineering_component().after(validation_task)
    training_task = train_model_component().after(feature_task)
    promotion_task = promote_model_component().after(training_task)
    drift_task = drift_detection_component().after(promotion_task)
    drift_decision_component().after(drift_task)


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=fraud_detection_pipeline,
        package_path="src/pipelines/fraud_detection_pipeline.yaml"
    )

    print("Kubeflow pipeline YAML generated")
    print(f"Base image used: {BASE_IMAGE}")