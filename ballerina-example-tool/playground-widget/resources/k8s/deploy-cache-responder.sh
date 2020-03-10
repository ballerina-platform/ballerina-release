#!/bin/bash

if [ -z ${BPG_GCP_PROJECT_ID} ]; then
    echo "Ballerina Playground GCP project ID is not set. Set variable BPG_GCP_PROJECT_ID to the GCP project ID found in the GCP Console."
    exit 1
fi

kubectl create ns ballerina-playground 

pushd cache_responder > /dev/null 2>&1 
    kubectl create -f cache-responder-service.yaml -n ballerina-playground
    envsubst < cache-responder-deployment.yaml | kubectl create -n ballerina-playground -f -
popd > /dev/null 2>&1