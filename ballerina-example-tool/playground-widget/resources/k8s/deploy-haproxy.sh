#!/bin/bash

if [ -z ${BPG_GCP_PROJECT_ID} ]; then
    echo "Ballerina Playground GCP project ID is not set. Set variable BPG_GCP_PROJECT_ID to the GCP project ID found in the GCP Console."
    exit 1
fi

pushd haproxy > /dev/null 2>&1
    kubectl create ns load-balancer

    kubectl create serviceaccount lb-sa -n load-balancer

    kubectl create clusterrolebinding lb-sa-view-binding --clusterrole=view --serviceaccount=load-balancer:lb-sa

    # Set environment variable values in the YAML file before kubectl create
    envsubst < rc.yaml | kubectl create -n load-balancer -f - 

    kubectl expose rc service-loadbalancer --type=LoadBalancer --name service-loadbalancer -n load-balancer --load-balancer-ip=35.196.203.66

    kubectl get pods,svc,rc -n load-balancer
popd > /dev/null 2>&1
