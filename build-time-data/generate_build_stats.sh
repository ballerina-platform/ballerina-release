#!/bin/bash

# Copyright (c) 2022 WSO2 Inc. (http:#www.wso2.org) All Rights Reserved.
#
# WSO2 Inc. licenses this file to you under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
# You may obtain a copy of the License at
#
# http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


examples_list=("nballerina" "hello_world" "hello_world_service")

#Github Folder
ROOT_DIR=$(pwd)

#Remove old json files and copy new files
rm -rf $ROOT_DIR/build-time-data/*.json

#Making directories to download examples from remote repo
mkdir examples
cd examples
git clone https://github.com/ballerina-platform/ballerina-distribution.git
cd ballerina-distribution
git checkout bbe-refactor
cd ..

git clone https://github.com/ballerina-platform/nballerina.git

for t in ${examples_list[@]}; do
  if [[ "$t" == "nballerina" ]]; then
    cd nballerina/compiler
    bal build --dump-build-time
    cp ./target/build-time.json $ROOT_DIR"/build-time-data/nballerina.json"
    cd $ROOT_DIR/examples
  else 
    bal_file=$t".bal"
    bal_file=$(find $PWD -name $bal_file)
    cd $ROOT_DIR/build-time-data/
    bal build --dump-build-time $bal_file
    rm -rf *.jar
    mv build-time.json $t".json"
    cd $ROOT_DIR/examples
  fi

done
