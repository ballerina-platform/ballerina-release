#!/usr/bin/env bash

if [ -z ${BPG_GCP_PROJECT_ID} ]; then
    echo "Ballerina Playground GCP project ID is not set. Set variable BPG_GCP_PROJECT_ID to the GCP project ID found in the GCP Console."
    exit 1
fi

pushd cron_jobs > /dev/null 2>&1
    kubectl create ns ballerina-playground
    kubectl create serviceaccount bpg-controller-sa -n ballerina-playground
    kubectl create clusterrolebinding bpg-controller-sa-edit-binding --clusterrole=edit --serviceaccount=ballerina-playground:bpg-controller-sa

    envsubst < maxcheck-cron.yaml | kubectl create -n ballerina-playground -f -
popd > /dev/null 2>&1