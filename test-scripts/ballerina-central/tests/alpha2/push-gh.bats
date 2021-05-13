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

@test "Push package '$PACKAGE_NAME:$VERSION' from ALPHA2." {
  cd "$PACKAGE_NAME-$VERSION"
  run $ALPHA2/bin/bal push
  assert_line --partial "$TEST_ORGANIZATION/$PACKAGE_NAME:$VERSION pushed to central successfully"
  [ "$status" -eq 0 ]
  cd -
}
