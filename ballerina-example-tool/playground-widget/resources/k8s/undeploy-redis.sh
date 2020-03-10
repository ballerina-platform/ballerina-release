#!/bin/bash

kubectl delete svc redis-master -n ballerina-playground
kubectl delete deployment redis-master -n ballerina-playground
kubectl delete svc redis-slave -n ballerina-playground
kubectl delete deployment redis-slave -n ballerina-playground