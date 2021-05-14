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

export PACKAGE_NAME="bctest$(random)"

rm -rf bctest*

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>>> Test with 1.2.x <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with 1.2.x
export JAVA_HOME=$JAVA8
VERSION=0.2.4 ./libs/bats/bin/bats 1.2.x/init-gh.bats
VERSION=0.2.4 ./libs/bats/bin/bats 1.2.x/push-gh.bats
VERSION=0.2.4 ./libs/bats/bin/bats 1.2.x/pull-gh.bats
VERSION=0.2.4 ./libs/bats/bin/bats 1.2.x/pull-latest-gh.bats

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>>> Test with SLP8 <<<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with slp8
export JAVA_HOME=$JAVA11
VERSION=1.3.3 ./libs/bats/bin/bats slp8/init-gh.bats
VERSION=1.3.3 ./libs/bats/bin/bats slp8/push-gh.bats
VERSION=1.3.3 ./libs/bats/bin/bats slp8/pull-gh.bats
VERSION=1.3.3 ./libs/bats/bin/bats slp8/pull-latest-gh.bats
VERSION=4.2.3 ./libs/bats/bin/bats slp8/init-gh.bats
VERSION=4.2.3 ./libs/bats/bin/bats slp8/push-gh.bats
VERSION=4.2.3 ./libs/bats/bin/bats slp8/pull-gh.bats
VERSION=4.2.3 ./libs/bats/bin/bats slp8/pull-latest-gh.bats
VERSION=1.3.3 ./libs/bats/bin/bats slp8/pull-gh.bats

# Test pull from 1.2.x
export JAVA_HOME=$JAVA8
VERSION=0.2.4 ./libs/bats/bin/bats 1.2.x/pull-latest-gh.bats

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with ALPHA1 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with alpha1
export JAVA_HOME=$JAVA11
VERSION=5.1.6 ./libs/bats/bin/bats alpha1/init-gh.bats
VERSION=5.1.6 ./libs/bats/bin/bats alpha1/push-gh.bats
VERSION=5.1.6 ./libs/bats/bin/bats alpha1/pull-gh.bats
VERSION=5.1.6 ./libs/bats/bin/bats alpha1/pull-latest-gh-not-found.bats # This fails as pushed package is considered an SLP8
VERSION=5.1.9 ./libs/bats/bin/bats alpha1/init-gh.bats
VERSION=5.1.9 ./libs/bats/bin/bats alpha1/push-gh.bats
VERSION=5.1.9 ./libs/bats/bin/bats alpha1/pull-gh.bats
VERSION=5.1.9 ./libs/bats/bin/bats alpha1/pull-latest-gh-not-found.bats # This fails as pushed package is considered an SLP8
VERSION=5.1.6 ./libs/bats/bin/bats alpha1/pull-gh.bats

# Test pull from SLP8
VERSION=4.2.3 ./libs/bats/bin/bats slp8/pull-gh.bats

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with ALPHA2 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with alpha2
VERSION=7.5.5 ./libs/bats/bin/bats alpha2/init-gh.bats
VERSION=7.5.5 ./libs/bats/bin/bats alpha2/push-gh.bats
VERSION=7.5.5 ./libs/bats/bin/bats alpha2/pull-gh.bats
VERSION=7.5.5 ./libs/bats/bin/bats alpha2/pull-latest-gh.bats
VERSION=8.6.2 ./libs/bats/bin/bats alpha2/init-gh.bats
VERSION=8.6.2 ./libs/bats/bin/bats alpha2/push-gh.bats
VERSION=8.6.2 ./libs/bats/bin/bats alpha2/pull-gh.bats
VERSION=8.6.2 ./libs/bats/bin/bats alpha2/pull-latest-gh.bats
VERSION=7.5.5 ./libs/bats/bin/bats alpha2/pull-gh.bats

# Test pull with SLP8
VERSION=4.2.3 ./libs/bats/bin/bats slp8/pull-gh.bats

# Test pull with alpha1
VERSION=8.6.2 ./libs/bats/bin/bats alpha1/pull-latest-gh.bats

# Test push from alpha1 and pull from alpha2
VERSION=9.1.1 ./libs/bats/bin/bats alpha1/init-gh.bats
VERSION=9.1.1 ./libs/bats/bin/bats alpha1/push-gh.bats
VERSION=9.1.1 ./libs/bats/bin/bats alpha2/pull-gh.bats

# Test push with SLP8 and pull with alpha1 and alpha2
VERSION=9.5.5 ./libs/bats/bin/bats slp8/init-gh.bats
VERSION=9.5.5 ./libs/bats/bin/bats slp8/push-gh.bats
VERSION=9.1.1 ./libs/bats/bin/bats alpha1/pull-gh.bats
VERSION=9.1.1 ./libs/bats/bin/bats alpha2/pull-gh.bats

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with ALPHA3 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with alpha3
VERSION=9.6.2 ./libs/bats/bin/bats alpha3/init-gh.bats
VERSION=9.6.2 ./libs/bats/bin/bats alpha3/push-gh.bats
VERSION=9.6.2 ./libs/bats/bin/bats alpha3/pull-gh.bats
VERSION=9.6.2 ./libs/bats/bin/bats alpha3/search-gh.bats
VERSION=9.6.2 ./libs/bats/bin/bats alpha3/pull-latest-gh.bats
VERSION=9.7.5 ./libs/bats/bin/bats alpha3/init-gh.bats
VERSION=9.7.5 ./libs/bats/bin/bats alpha3/push-gh.bats
VERSION=9.7.5 ./libs/bats/bin/bats alpha3/pull-gh.bats
VERSION=9.7.5 ./libs/bats/bin/bats alpha3/pull-latest-gh.bats
VERSION=9.6.2 ./libs/bats/bin/bats alpha3/pull-gh.bats

# Test pull with SLP8
VERSION=9.5.5 ./libs/bats/bin/bats slp8/pull-latest-gh.bats

# Test pull with alpha1
VERSION=8.6.2 ./libs/bats/bin/bats alpha1/pull-latest-gh.bats

# Test pull with alpha2
VERSION=8.6.2 ./libs/bats/bin/bats alpha2/pull-latest-gh.bats

# Test push with alpha2 and pull with alpha3
VERSION=9.8.4 ./libs/bats/bin/bats alpha2/init-gh.bats
VERSION=9.8.4 ./libs/bats/bin/bats alpha2/push-gh.bats
VERSION=9.8.4 ./libs/bats/bin/bats alpha2/pull-latest-gh.bats
VERSION=9.8.4 ./libs/bats/bin/bats alpha3/pull-latest-gh.bats

echo "-----------------------------------------------------------"
echo ">>>>>>>>>>>>>>>>>>>> Test with ALPHA4 <<<<<<<<<<<<<<<<<<<<<"
echo "-----------------------------------------------------------"

# Test push and pull with alpha4
VERSION=10.0.1 ./libs/bats/bin/bats alpha4/init-gh.bats
VERSION=10.0.1 ./libs/bats/bin/bats alpha4/push-gh.bats
VERSION=10.0.1 ./libs/bats/bin/bats alpha4/pull-gh.bats
VERSION=10.0.1 ./libs/bats/bin/bats alpha4/search-gh.bats
VERSION=10.0.1 ./libs/bats/bin/bats alpha4/pull-latest-gh.bats
VERSION=10.3.6 ./libs/bats/bin/bats alpha4/init-gh.bats
VERSION=10.3.6 ./libs/bats/bin/bats alpha4/push-gh.bats
VERSION=10.3.6 ./libs/bats/bin/bats alpha4/pull-gh.bats
VERSION=10.3.6 ./libs/bats/bin/bats alpha4/pull-latest-gh.bats
VERSION=10.3.6 ./libs/bats/bin/bats alpha4/pull-gh.bats

# Test pull with SLP8
VERSION=9.5.5 ./libs/bats/bin/bats slp8/pull-latest-gh.bats

# Test pull with alpha2
VERSION=9.8.4 ./libs/bats/bin/bats alpha2/pull-latest-gh.bats

# Test pull with alpha3
VERSION=10.3.6 ./libs/bats/bin/bats alpha3/pull-latest-gh.bats

# Test push with alpha3 and pull with alpha4
VERSION=11.4.7 ./libs/bats/bin/bats alpha3/init-gh.bats
VERSION=11.4.7 ./libs/bats/bin/bats alpha3/push-gh.bats
VERSION=11.4.7 ./libs/bats/bin/bats alpha3/pull-latest-gh.bats
VERSION=10.3.6 ./libs/bats/bin/bats alpha4/pull-latest-gh.bats

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

# Test pull with SLP8
VERSION=9.5.5 ./libs/bats/bin/bats slp8/pull-latest-gh.bats

# Test pull with alpha2
VERSION=9.8.4 ./libs/bats/bin/bats alpha2/pull-latest-gh.bats

# Test pull with alpha3
VERSION=12.9.1 ./libs/bats/bin/bats alpha3/pull-latest-gh.bats

# Test pull with alpha4
VERSION=10.3.6 ./libs/bats/bin/bats alpha4/pull-latest-gh.bats

# Test push with alpha3 and pull with alpha4 and alpha5
VERSION=13.5.7 ./libs/bats/bin/bats alpha3/init-gh.bats
VERSION=13.5.7 ./libs/bats/bin/bats alpha3/push-gh.bats
VERSION=13.5.7 ./libs/bats/bin/bats alpha3/pull-latest-gh.bats
VERSION=10.3.6 ./libs/bats/bin/bats alpha4/pull-latest-gh.bats
VERSION=12.9.1 ./libs/bats/bin/bats alpha5/pull-latest-gh.bats

rm -rf bctest*
