#!/bin/bash

set -e

echo "Starting data drift monitoring..."

python src/monitoring/drift_detection.py

python src/monitoring/drift_decision.py

echo "Data drift monitoring completed."