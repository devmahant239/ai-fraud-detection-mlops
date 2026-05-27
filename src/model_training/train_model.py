import mlflow
import mlflow.sklearn
import pandas as pd
import pickle
import yaml

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

mlflow.set_tracking_uri("file:./mlruns")
df = pd.read_csv("data/processed/transactions_features.csv")

with open("data/processed/transactions_features.csv.dvc") as file:
    dvc_metadata = yaml.safe_load(file)

dataset_version = dvc_metadata["outs"][0]["md5"]


features = [
    "amount",
    "failed_attempts",
    "is_international",
    "high_amount",
    "risk_score"
]

target = "is_fraud"

X = df[features]
y = df[target]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


mlflow.set_experiment("fraud-detection-experiments")


models = {
    "logistic_regression": LogisticRegression(max_iter=1000),
    "decision_tree": DecisionTreeClassifier(max_depth=5, random_state=42),
    "random_forest_50": RandomForestClassifier(n_estimators=50, random_state=42),
    "random_forest_100": RandomForestClassifier(n_estimators=100, random_state=42),
    "random_forest_200": RandomForestClassifier(n_estimators=200, random_state=42),
    "gradient_boosting": GradientBoostingClassifier(random_state=42),
}


best_model = None
best_model_name = None
best_f1_score = 0


for model_name, model in models.items():

    with mlflow.start_run(run_name=model_name):

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_param("model_name", model_name)

        mlflow.log_param("dataset_version", dataset_version)
        mlflow.log_param("dataset_path", "data/processed/transactions_features.csv")
        mlflow.log_param("row_count", len(df))
        mlflow.log_param("feature_count", len(features))

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(
            sk_model=model,
            name=model_name,
            registered_model_name="fraud_detection_model"
        )

        print(f"\nModel: {model_name}")
        print(f"Accuracy: {accuracy}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1 Score: {f1}")

        if f1 > best_f1_score:
            best_f1_score = f1
            best_model = model
            best_model_name = model_name


with open("src/model_training/fraud_model.pkl", "wb") as file:
    pickle.dump(best_model, file)


print(f"\nBest Model: {best_model_name}")
print(f"Best F1 Score: {best_f1_score}")
print("Best model saved at src/model_training/fraud_model.pkl")