#!/usr/bin/env bash
# Copyright (c) 2017, WSO2 Inc. (http://wso2.com) All Rights Reserved.
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
JVM_ARGS=""
if [ "$ENABLE_DEBUG" == "true" ]; then
    JVM_ARGS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=$DEBUG_PORT"
fi

PARSER_CLASSPATH="/api/playground-parser.jar"
for j in "$BALLERINA_HOME"/bre/lib/*.jar
do
    PARSER_CLASSPATH="$PARSER_CLASSPATH":$j
done

exec java $JVM_ARGS \
    -Dballerina.home=/ballerina/runtime \
    -Dtransports.netty.conf=/api/netty-transports.yml \
    -classpath "$PARSER_CLASSPATH" \
    org.ballerinalang.platform.playground.parser.ServiceRunner
