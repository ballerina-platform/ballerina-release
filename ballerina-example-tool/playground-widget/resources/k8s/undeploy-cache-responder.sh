#!/bin/bash

kubectl delete svc bpg-cache-responder -n ballerina-playground
kubectl delete deployment bpg-cache-responder-dep -n ballerina-playground