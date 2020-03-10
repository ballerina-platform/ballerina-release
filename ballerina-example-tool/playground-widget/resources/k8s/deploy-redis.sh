#!/bin/bash

kubectl create ns ballerina-playground

pushd redis > /dev/null 2>&1 
    kubectl create -f redis-master-service.yaml -n ballerina-playground
    kubectl create -f redis-master-deployment.yaml -n ballerina-playground
    kubectl create -f redis-slave-service.yaml -n ballerina-playground
    kubectl create -f redis-slave-deployment.yaml -n ballerina-playground
popd > /dev/null 2>&1