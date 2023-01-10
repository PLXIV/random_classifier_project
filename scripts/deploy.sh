#!/usr/bin/env bash

docker build . -t myclassifier:0.0.1

minikube start --no-vtx-check --driver=virtualbox

minikube image load myclassifier:0.0.1

kubectl apply -f namespace.yaml -f deployment.yaml -f service.yaml

kubectl get service -o wide --namespace myclassifier-namespace