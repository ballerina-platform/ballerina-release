# --------------------------------------------------------------------
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
# -----------------------------------------------------------------------
FROM openjdk:jre-alpine

RUN apk update && apk add --no-cache bash curl unzip \
    && addgroup ballerina && adduser -g '' -s /bin/bash -D -G ballerina ballerinauser

ENV ENABLE_DEBUG false
ENV DEBUG_PORT 5005

COPY ballerinaKeystore.p12 /security/
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY ballerina-platform.zip /root/

RUN mkdir /ballerina \
    && unzip /root/ballerina-platform.zip -d /ballerina/ \
    && mv /ballerina/ballerina* /ballerina/runtime \
    && mkdir -p /ballerina/runtime/logs \
    && rm /root/ballerina-platform.zip \
    && chmod +x /usr/local/bin/docker-entrypoint.sh

ENV BALLERINA_HOME /ballerina/runtime
ENV PATH $BALLERINA_HOME/bin:$PATH

COPY resources /resources/
COPY services /services/
RUN chmod +x /services/src/build.sh \
    && cd /services/src/ && sh build.sh \
    && cp *.balx ../ \
    && chown -R ballerinauser:ballerina /services/ /ballerina/

COPY netty-transports.yml /api/
COPY playground-launcher.jar /api/

EXPOSE 8080 8443
USER ballerinauser
WORKDIR /ballerina/

# TODO: may need to use a signal aware init system because launchers spawn new processes
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

