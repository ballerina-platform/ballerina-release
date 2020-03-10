#!/bin/bash 
 
kubectl delete svc bpg-controller -n ballerina-playground
kubectl delete svc bpg-controller-internal -n ballerina-playground
kubectl delete deployment bpg-controller-dep -n ballerina-playground
kubectl delete clusterrolebinding bpg-controller-sa-edit-binding 
kubectl delete serviceaccount bpg-controller-sa -n ballerina-playground 