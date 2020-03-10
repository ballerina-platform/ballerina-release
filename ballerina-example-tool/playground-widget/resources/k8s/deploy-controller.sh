#!/bin/bash 
 
if [ -z ${BPG_GCP_PROJECT_ID} ]; then 
    echo "Ballerina Playground GCP project ID is not set. Set variable BPG_GCP_PROJECT_ID to the GCP project ID found in the GCP Console." 
    exit 1 
fi 
 
pushd controller > /dev/null 2>&1 
    kubectl create ns ballerina-playground
    kubectl create serviceaccount bpg-controller-sa -n ballerina-playground
    kubectl create clusterrolebinding bpg-controller-sa-edit-binding --clusterrole=edit --serviceaccount=ballerina-playground:bpg-controller-sa 
 
    kubectl create -f controller-service.yaml -n ballerina-playground
    kubectl create -f controller-service-internal.yaml -n ballerina-playground
    envsubst < controller-deployment.yaml | kubectl create -n ballerina-playground -f -

    kubectl get pods,svc,rc -n ballerina-playground 
popd > /dev/null 2>&1 