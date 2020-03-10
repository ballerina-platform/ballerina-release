#!/usr/bin/env bash

set -e

bash deploy-watcher.sh
sleep 2
bash deploy-validator.sh
sleep 2
bash deploy-controller.sh
sleep 3
bash deploy-parser.sh
sleep 1
bash deploy-cache-responder.sh
sleep 1
bash deploy-desiredcheck.sh
sleep 3
bash deploy-maxcheck.sh