#!/bin/bash

kubectl delete svc bpg-launcher -n ballerina-playground
kubectl delete deployment bpg-launcher-dep -n ballerina-playground