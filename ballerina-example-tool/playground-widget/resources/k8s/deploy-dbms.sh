#!/bin/bash

pushd dbms > /dev/null 2>&1
    kubectl create -f dbms-service.yaml -n ballerina-playground
popd > /dev/null 2>&1