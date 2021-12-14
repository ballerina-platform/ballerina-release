#!/bin/bash
# ---------------------------------------------------------------------------
#  Copyright (c) 2021, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

trap ctrl_c INT
set -e

function ctrl_c() {
    echo "cancelling build"
    exit 2;
}


random() {
    echo $(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w ${1:-10} | head -n 1 | tr '[:upper:]' '[:lower:]');
}

export PACKAGE_NAME="bc$(random)"

rm -rf bc*

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with ALPHA5 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with alpha5
VERSION=12.8.3 ./libs/bats/bin/bats alpha5/init-gh.bats
VERSION=12.8.3 ./libs/bats/bin/bats alpha5/push-gh.bats
VERSION=12.8.3 ./libs/bats/bin/bats alpha5/pull-gh.bats
VERSION=12.8.3 ./libs/bats/bin/bats alpha5/search-gh.bats
VERSION=12.8.3 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats
VERSION=12.9.1 ./libs/bats/bin/bats alpha5/init-gh.bats
VERSION=12.9.1 ./libs/bats/bin/bats alpha5/push-gh.bats
VERSION=12.9.1 ./libs/bats/bin/bats alpha5/pull-gh.bats
VERSION=12.9.1 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats
VERSION=12.9.1 ./libs/bats/bin/bats alpha5/pull-gh.bats

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with BETA1 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with beta1
VERSION=14.8.2 ./libs/bats/bin/bats beta1/init-gh.bats
VERSION=14.8.2 ./libs/bats/bin/bats beta1/push-gh.bats
VERSION=14.8.2 ./libs/bats/bin/bats beta1/pull-gh.bats
VERSION=14.8.2 ./libs/bats/bin/bats beta1/search-gh.bats
VERSION=14.8.2 ./libs/bats/bin/bats beta1/pull-latest-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/init-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/push-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-gh.bats

# Test pull with alpha5
VERSION=12.9.1 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats

# Test push with beta1 and pull with alpha5 and beta1
VERSION=15.3.5 ./libs/bats/bin/bats alpha5/init-gh.bats
VERSION=15.3.5 ./libs/bats/bin/bats alpha5/push-gh.bats
VERSION=15.3.5 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with BETA2 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with beta2
VERSION=16.7.2 ./libs/bats/bin/bats beta2/init-gh.bats
VERSION=16.7.2 ./libs/bats/bin/bats beta2/push-gh.bats
VERSION=16.7.2 ./libs/bats/bin/bats beta2/pull-gh.bats
VERSION=16.7.2 ./libs/bats/bin/bats beta2/search-gh.bats
VERSION=16.7.2 ./libs/bats/bin/bats beta2/pull-latest-gh.bats
VERSION=16.8.5 ./libs/bats/bin/bats beta2/init-gh.bats
VERSION=16.8.5 ./libs/bats/bin/bats beta2/push-gh.bats
VERSION=16.8.5 ./libs/bats/bin/bats beta2/pull-gh.bats
VERSION=16.8.5 ./libs/bats/bin/bats beta2/pull-latest-gh.bats
VERSION=16.8.5 ./libs/bats/bin/bats beta2/pull-gh.bats

# Test pull with alpha5
VERSION=15.3.5 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats

# Test pull with beta1
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats

# Test push with alpha5 and pull with beta1 and beta2
VERSION=17.4.4 ./libs/bats/bin/bats alpha5/init-gh.bats
VERSION=17.4.4 ./libs/bats/bin/bats alpha5/push-gh.bats
VERSION=17.4.4 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats
VERSION=17.4.4 ./libs/bats/bin/bats beta2/pull-latest-gh.bats

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with BETA3 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with beta3
VERSION=18.3.7 ./libs/bats/bin/bats beta3/init-gh.bats
VERSION=18.3.7 ./libs/bats/bin/bats beta3/push-gh.bats
VERSION=18.3.7 ./libs/bats/bin/bats beta3/pull-gh.bats
VERSION=18.3.7 ./libs/bats/bin/bats beta3/search-gh.bats
VERSION=18.3.7 ./libs/bats/bin/bats beta3/pull-latest-gh.bats
VERSION=18.6.1 ./libs/bats/bin/bats beta3/init-gh.bats
VERSION=18.6.1 ./libs/bats/bin/bats beta3/push-gh.bats
VERSION=18.6.1 ./libs/bats/bin/bats beta3/pull-gh.bats
VERSION=18.6.1 ./libs/bats/bin/bats beta3/pull-latest-gh.bats
VERSION=18.6.1 ./libs/bats/bin/bats beta3/pull-gh.bats

# Test pull with alpha5
VERSION=17.4.4 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats

# Test pull with beta1
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats

# Test pull with beta2
VERSION=17.4.4 ./libs/bats/bin/bats beta2/pull-latest-gh.bats

# Test push with alpha5 and pull with beta1, beta2 and beta3
VERSION=19.7.4 ./libs/bats/bin/bats alpha5/init-gh.bats
VERSION=19.7.4 ./libs/bats/bin/bats alpha5/push-gh.bats
VERSION=19.7.4 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats
VERSION=19.7.4 ./libs/bats/bin/bats beta2/pull-latest-gh.bats
VERSION=19.7.4 ./libs/bats/bin/bats beta3/pull-latest-gh.bats

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with BETA4 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with beta4
VERSION=20.6.2 ./libs/bats/bin/bats beta4/init-gh.bats
VERSION=20.6.2 ./libs/bats/bin/bats beta4/push-gh.bats
VERSION=20.6.2 ./libs/bats/bin/bats beta4/pull-gh.bats
VERSION=20.6.2 ./libs/bats/bin/bats beta4/search-gh.bats
VERSION=20.6.2 ./libs/bats/bin/bats beta4/pull-latest-gh.bats
VERSION=20.7.5 ./libs/bats/bin/bats beta4/init-gh.bats
VERSION=20.7.5 ./libs/bats/bin/bats beta4/push-gh.bats
VERSION=20.7.5 ./libs/bats/bin/bats beta4/pull-gh.bats
VERSION=20.7.5 ./libs/bats/bin/bats beta4/pull-latest-gh.bats
VERSION=20.7.5 ./libs/bats/bin/bats beta4/pull-gh.bats

# Test pull with alpha5
VERSION=19.7.4 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats

# Test pull with beta1
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats

# Test pull with beta2
VERSION=19.7.4 ./libs/bats/bin/bats beta2/pull-latest-gh.bats

# Test pull with beta3
VERSION=19.7.4 ./libs/bats/bin/bats beta3/pull-latest-gh.bats

# Test push with alpha5 and pull with beta1, beta2, beta3 and beta4
VERSION=21.7.4 ./libs/bats/bin/bats alpha5/init-gh.bats
VERSION=21.7.4 ./libs/bats/bin/bats alpha5/push-gh.bats
VERSION=21.7.4 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats
VERSION=21.7.4 ./libs/bats/bin/bats beta2/pull-latest-gh.bats
VERSION=21.7.4 ./libs/bats/bin/bats beta3/pull-latest-gh.bats
VERSION=21.7.4 ./libs/bats/bin/bats beta4/pull-latest-gh.bats

# Test push with beta3 and pull with beta4
VERSION=22.7.4 ./libs/bats/bin/bats beta3/init-gh.bats
VERSION=22.7.4 ./libs/bats/bin/bats beta3/push-gh.bats
VERSION=22.7.4 ./libs/bats/bin/bats beta3/pull-latest-gh.bats
VERSION=22.7.4 ./libs/bats/bin/bats beta4/pull-latest-gh.bats


echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with BETA6 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with beta6
VERSION=23.8.2 ./libs/bats/bin/bats beta6/init-gh.bats
VERSION=23.8.2 ./libs/bats/bin/bats beta6/push-gh.bats
VERSION=23.8.2 ./libs/bats/bin/bats beta6/pull-gh.bats
VERSION=23.8.2 ./libs/bats/bin/bats beta6/search-gh.bats
VERSION=23.8.2 ./libs/bats/bin/bats beta6/pull-latest-gh.bats
VERSION=23.9.5 ./libs/bats/bin/bats beta6/init-gh.bats
VERSION=23.9.5 ./libs/bats/bin/bats beta6/push-gh.bats
VERSION=23.9.5 ./libs/bats/bin/bats beta6/pull-gh.bats
VERSION=23.9.5 ./libs/bats/bin/bats beta6/pull-latest-gh.bats
VERSION=23.9.5 ./libs/bats/bin/bats beta6/pull-gh.bats

# Test pull with alpha5
VERSION=21.7.4 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats

# Test pull with beta1
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats

# Test pull with beta2
VERSION=21.7.4 ./libs/bats/bin/bats beta2/pull-latest-gh.bats

# Test pull with beta3
VERSION=22.7.4 ./libs/bats/bin/bats beta3/pull-latest-gh.bats

# Test pull with beta4
VERSION=22.7.4 ./libs/bats/bin/bats beta4/pull-latest-gh.bats

# Test push with alpha5 and pull with beta1, beta2, beta3, beta4 and beta6
VERSION=24.8.4 ./libs/bats/bin/bats alpha5/init-gh.bats
VERSION=24.8.4 ./libs/bats/bin/bats alpha5/push-gh.bats
VERSION=24.8.4 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats
VERSION=14.9.5 ./libs/bats/bin/bats beta1/pull-latest-gh.bats
VERSION=24.8.4 ./libs/bats/bin/bats beta2/pull-latest-gh.bats
VERSION=24.8.4 ./libs/bats/bin/bats beta3/pull-latest-gh.bats
VERSION=24.8.4 ./libs/bats/bin/bats beta4/pull-latest-gh.bats
VERSION=24.8.4 ./libs/bats/bin/bats beta6/pull-latest-gh.bats

# Test push with beta3 and pull with beta4
VERSION=25.8.4 ./libs/bats/bin/bats beta3/init-gh.bats
VERSION=25.8.4 ./libs/bats/bin/bats beta3/push-gh.bats
VERSION=25.8.4 ./libs/bats/bin/bats beta3/pull-latest-gh.bats
VERSION=25.8.4 ./libs/bats/bin/bats beta4/pull-latest-gh.bats
VERSION=25.8.4 ./libs/bats/bin/bats beta6/pull-latest-gh.bats

rm -rf bc*
