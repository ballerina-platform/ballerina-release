#!/bin/bash

kubectl delete svc service-loadbalancer -n load-balancer
kubectl delete rc service-loadbalancer -n load-balancer
kubectl delete clusterrolebinding lb-sa-view-binding
kubectl delete serviceaccount lb-sa -n load-balancer
