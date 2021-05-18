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

FROM ballerina/ballerina:1.2.11 AS b12x-pack
FROM ballerina/ballerina:swan-lake-preview8 AS slp8-pack
FROM ballerina/ballerina:swan-lake-alpha1 AS alpha1-pack
FROM ballerina/ballerina:swan-lake-alpha2 AS alpha2-pack
FROM ballerina/ballerina:swan-lake-alpha3 AS alpha3-pack
FROM ballerina/ballerina:swan-lake-alpha4 AS alpha4-pack
FROM ballerina/ballerina:swan-lake-alpha5 AS alpha5-pack

FROM adoptopenjdk/openjdk11:alpine

RUN apk -q update && \
    apk --no-cache -q add bash curl openjdk8

COPY --from=b12x-pack /ballerina/runtime /ballerina/b12x
COPY --from=slp8-pack /ballerina/runtime /ballerina/slp8
COPY --from=alpha1-pack /ballerina/runtime /ballerina/alpha1
COPY --from=alpha2-pack /ballerina/runtime /ballerina/alpha2
COPY --from=alpha3-pack /ballerina/runtime /ballerina/alpha3
COPY --from=alpha4-pack /ballerina/runtime /ballerina/alpha4
COPY --from=alpha5-pack /ballerina/runtime /ballerina/alpha5

ARG BALLERINA_CENTRAL_ACCESS_TOKEN=""
ARG TEST_ORGANIZATION="bc2testorg"

ENV BALLERINA_CENTRAL_ACCESS_TOKEN=$BALLERINA_CENTRAL_ACCESS_TOKEN
ENV TEST_ORGANIZATION=$TEST_ORGANIZATION

ENV B12X=/ballerina/b12x
ENV SLP8=/ballerina/slp8
ENV ALPHA1=/ballerina/alpha1
ENV ALPHA2=/ballerina/alpha2
ENV ALPHA3=/ballerina/alpha3
ENV ALPHA4=/ballerina/alpha4
ENV ALPHA5=/ballerina/alpha5

ENV JAVA11=/opt/java/openjdk
ENV JAVA8=/usr/lib/jvm/java-1.8-openjdk

WORKDIR /tests

COPY tests /tests
COPY --from=bats-libs /libs libs

RUN sh run-tests.sh
