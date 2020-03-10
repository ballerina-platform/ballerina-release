#!/bin/bash

if [ -z ${BPG_GCP_PROJECT_ID} ]; then
    echo "Ballerina Playground GCP project ID is not set. Set variable BPG_GCP_PROJECT_ID to the GCP project ID found in the GCP Console."
    exit 1
fi

#go fmt
#CGO_ENABLED=0 GOOS=linux godep go build -a -installsuffix cgo -ldflags '-w' -o service_loadbalancer ./service_loadbalancer.go ./loadbalancer_log.go || exit 1

docker build -t gcr.io/${BPG_GCP_PROJECT_ID}/haproxy:0.4-preprod-${1} --no-cache=true .  || exit 1

#gcloud docker -- push gcr.io/${BPG_GCP_PROJECT_ID}/haproxy:0.4v1  || exit 1
