# AI Fraud Detection Platform Architecture

## High-Level Flow

User / Bank Transaction System
↓
Transaction Data Generator
↓
Kafka
↓
Kafka Consumer
↓
PostgreSQL
↓
Data Validation
↓
DVC Dataset Versioning
↓
Feature Engineering
↓
Model Training
↓
MLflow Experiment Tracking
↓
Model Registry
↓
FastAPI Model API
↓
Docker
↓
Kubernetes
↓
AWS EKS Deployment
↓
Monitoring with Prometheus and Grafana

## Components

### 1. Transaction Data Generator
Creates fake financial transaction data for testing.

### 2. Kafka
Streams transaction data in real time.

### 3. Kafka Consumer
Reads transaction data from Kafka and stores it in PostgreSQL.

### 4. PostgreSQL
Stores raw and processed transaction data.

### 5. Data Validation
Checks data quality using Great Expectations.

### 6. DVC
Versions datasets and tracks changes in data.

### 7. Feature Engineering
Converts raw transaction data into ML-ready features.

### 8. Model Training
Trains fraud detection models.

### 9. MLflow
Tracks experiments, parameters, metrics, and models.

### 10. Model Registry
Stores the best model version.

### 11. FastAPI
Serves the trained model as an API.

### 12. Docker
Packages services into containers.

### 13. Kubernetes
Runs and manages containers.

### 14. AWS
Hosts the production-style infrastructure.

### 15. Monitoring
Tracks application, infrastructure, and model behavior.