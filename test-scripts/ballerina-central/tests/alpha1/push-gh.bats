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

@test "Push package '$PACKAGE_NAME:$VERSION' with curl as from ALPHA1." {
  cd "$PACKAGE_NAME-$VERSION"
  local hostname="api.central.ballerina.io"
  if [ "$BALLERINA_DEV_CENTRAL" = "true" ]; then
    hostname="api.dev-central.ballerina.io"
  fi

  if [ "$BALLERINA_STAGE_CENTRAL" = "true" ]; then
    hostname="api.staging-central.ballerina.io"
  fi
  run curl -v -H "Authorization: Bearer $BALLERINA_CENTRAL_ACCESS_TOKEN" -H "Content-Type: application/octet-stream" -H "User-Agent: slalpha1" --data-binary "@target/balo/$TEST_ORGANIZATION-$PACKAGE_NAME-any-$VERSION.balo" https://$hostname/2.0/registry/packages
  assert_line --partial "HTTP/2 204"
  [ "$status" -eq 0 ]
  cd -
}
