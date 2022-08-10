# --------------------------------------------------------------------
# Copyright (c) 2021, WSO2 Inc. (http://wso2.com) All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------

FROM alpine/git AS bats-libs

WORKDIR /libs

RUN git clone https://github.com/sstephenson/bats /libs/bats && \
    git clone https://github.com/ztombol/bats-support /libs/bats-support && \
    git clone https://github.com/ztombol/bats-assert /libs/bats-assert

# Get Ballerina releases
FROM ballerina/ballerina:swan-lake-alpha5 AS alpha5-pack
FROM ballerina/ballerina:swan-lake-beta1 AS beta1-pack
FROM ballerina/ballerina:swan-lake-beta2 AS beta2-pack
FROM ballerina/ballerina:swan-lake-beta3 AS beta3-pack
FROM ballerina/ballerina:swan-lake-beta4 AS beta4-pack
FROM ballerina/ballerina:swan-lake-beta6 AS beta6-pack

FROM adoptopenjdk/openjdk11:alpine

RUN apk -q update && \
    apk --no-cache -q add bash curl

# Copy Ballerina runtimes
COPY --from=alpha5-pack /ballerina/runtime /ballerina/alpha5
COPY --from=beta1-pack /ballerina/runtime /ballerina/beta1
COPY --from=beta2-pack /ballerina/runtime /ballerina/beta2
COPY --from=beta3-pack /ballerina/runtime /ballerina/beta3
COPY --from=beta4-pack /ballerina/runtime /ballerina/beta4
COPY --from=beta6-pack /ballerina/runtime /ballerina/beta6

ARG BALLERINA_CENTRAL_ACCESS_TOKEN=""
ARG TEST_ORGANIZATION="bctestorg"
ARG BALLERINA_STAGE_CENTRAL="false"
ARG BALLERINA_DEV_CENTRAL="false"

ENV BALLERINA_CENTRAL_ACCESS_TOKEN=$BALLERINA_CENTRAL_ACCESS_TOKEN
ENV TEST_ORGANIZATION=$TEST_ORGANIZATION
ENV BALLERINA_STAGE_CENTRAL=$BALLERINA_STAGE_CENTRAL
ENV BALLERINA_DEV_CENTRAL=$BALLERINA_DEV_CENTRAL

# Set environment variables
ENV ALPHA5=/ballerina/alpha5
ENV BETA1=/ballerina/beta1
ENV BETA2=/ballerina/beta2
ENV BETA3=/ballerina/beta3
ENV BETA4=/ballerina/beta4
ENV BETA6=/ballerina/beta6

WORKDIR /tests

COPY tests /tests
COPY --from=bats-libs /libs libs

RUN sh run-tests.sh
