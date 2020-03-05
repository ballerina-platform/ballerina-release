#!/usr/bin/env bash

kubectl get deployment -n ballerina-playground | grep bpg-launcher | awk '{print $1}' | xargs kubectl delete deployment -n ballerina-playground

kubectl get svc -n ballerina-playground | grep bpg-launcher | awk '{print $1}' | xargs kubectl delete svc -n ballerina-playground

kubectl get deployment,svc -n ballerina-playground