#!./test-libs/bats/bin/bats
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

load '../libs/bats-support/load'
load '../libs/bats-assert/load'

@test "Pull package '$PACKAGE_NAME:*' from ALPHA3." {
  local user_dir="$(eval echo ~$USER)"
  rm -rf "$user_dir/.ballerina/repositories/central.ballerina.io/bala/$TEST_ORGANIZATION/$PACKAGE_NAME/$VERSION"
  run $ALPHA3/bin/bal pull "$TEST_ORGANIZATION/$PACKAGE_NAME"
  assert_line --partial "$TEST_ORGANIZATION/$PACKAGE_NAME:$VERSION pulled from central successfully"
  [ "$status" -eq 0 ]
  local package_file="$user_dir/.ballerina/repositories/central.ballerina.io/bala/$TEST_ORGANIZATION/$PACKAGE_NAME/$VERSION/any/package.json"
  if [ ! -f "$package_file" ]; then
      assert_failure
  fi
  rm -rf "$user_dir/.ballerina/repositories/"
}
