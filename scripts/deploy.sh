#!/bin/bash

set -e

echo "Applying Kubernetes manifests..."

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/fraud-api-deployment.yaml
kubectl apply -f k8s/fraud-api-service.yaml

kubectl apply -f monitoring/prometheus-config.yaml
kubectl apply -f monitoring/prometheus-deployment.yaml
kubectl apply -f monitoring/prometheus-service.yaml
kubectl apply -f monitoring/grafana-deployment.yaml
kubectl apply -f monitoring/grafana-service.yaml

echo "Deployment completed."