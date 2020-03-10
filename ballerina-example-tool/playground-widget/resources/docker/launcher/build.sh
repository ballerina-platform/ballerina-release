#!/usr/bin/env bash

if [ -z ${BPG_GCP_PROJECT_ID} ]; then
    echo "Ballerina Playground GCP project ID is not set. Set variable BPG_GCP_PROJECT_ID to the GCP project ID found in the GCP Console."
    exit 1
fi

docker build --no-cache=true -t gcr.io/${BPG_GCP_PROJECT_ID}/launcher:v0.1-${1} .