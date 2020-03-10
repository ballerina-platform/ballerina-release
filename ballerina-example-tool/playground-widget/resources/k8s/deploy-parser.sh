#!/bin/bash

if [ -z ${BPG_GCP_PROJECT_ID} ]; then
    echo "Ballerina Playground GCP project ID is not set. Set variable BPG_GCP_PROJECT_ID to the GCP project ID found in the GCP Console."
    exit 1
fi

kubectl create ns ballerina-playground 

pushd parser > /dev/null 2>&1
    kubectl create -f parser-service.yaml -n ballerina-playground
    envsubst < parser-deployment.yaml | kubectl create -n ballerina-playground -f -
popd > /dev/null 2>&1