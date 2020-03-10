#!/usr/bin/env bash

bash undeploy-parser.sh
bash undeploy-cache-responder.sh
bash undeploy-controller.sh
bash undeploy-desiredcheck.sh
bash undeploy-maxcheck.sh
bash undeploy-validator.sh
sleep 2
bash undeploy-watcher.sh