#!/bin/bash

kubectl delete svc bpg-parser -n ballerina-playground
kubectl delete deployment bpg-parser-dep -n ballerina-playground