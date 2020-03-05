# Copyright (c) 2018, WSO2 Inc. (http://wso2.com) All Rights Reserved.
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

FROM anapsix/alpine-java:8_jdk

# Set project version
ENV CONTROLLER_VERSION "0.8-SNAPSHOT"

LABEL maintainer="ballerina-dev@googlegroups.com"

# Add a non-privileged user
RUN mkdir -p /api && \
    addgroup troupe && \
    adduser -g '' -s /bin/bash -D -G troupe ballerina

# Copy artifacts
COPY * /api/

# Change permission
RUN chown -R ballerina:troupe /api && \
    chmod +x /api/init.sh

# Change user
USER ballerina

CMD [ "bash", "/api/init.sh" ]