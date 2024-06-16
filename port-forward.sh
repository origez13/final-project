#!/bin/bash

# Start port-forward for Jenkins
kubectl port-forward svc/jenkins 8080:8080 --namespace jenkins &

# Start port-forward for Grafana
kubectl port-forward grafana-8d4f94575-6b4pw 3000:3000 -n monitoring &

# Start port-forward for ArgoCD
kubectl port-forward svc/argocd-server -n argocd 8081:443 &