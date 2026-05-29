#!/bin/bash

echo "Fraud API logs:"
kubectl logs deployment/fraud-api -n fraud-detection