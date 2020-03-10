#!/bin/bash 
 
kubectl delete deployment bpg-watcher-dep -n ballerina-playground
kubectl delete clusterrolebinding bpg-watcher-sa-edit-binding
kubectl delete serviceaccount bpg-watcher-sa -n ballerina-playground