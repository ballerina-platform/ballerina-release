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

FROM gcr.io/google_containers/haproxy:0.4
MAINTAINER dev@wso2.com

USER root

RUN mkdir -p /etc/haproxy/errors /var/state/haproxy
RUN for ERROR_CODE in 400 403 404 408 500 502 503 504;do curl -sSL -o /etc/haproxy/errors/$ERROR_CODE.http \
	https://raw.githubusercontent.com/haproxy/haproxy-1.5/master/examples/errorfiles/$ERROR_CODE.http;done

# https://blog.phusion.nl/2015/01/20/docker-and-the-pid-1-zombie-reaping-problem
COPY dumb-init_1.2.1_amd64 /sbin/dumb-init
RUN chmod +x /sbin/dumb-init

ENTRYPOINT ["dumb-init", "/service_loadbalancer"]

COPY haproxy.cfg /etc/haproxy/haproxy.cfg
COPY service_loadbalancer service_loadbalancer
COPY service_loadbalancer.go service_loadbalancer.go
COPY template.cfg template.cfg
COPY loadbalancer.json loadbalancer.json
COPY haproxy_reload haproxy_reload
COPY README.md README.md

RUN chown root:root /*.*
RUN chmod +x /haproxy_reload

# Adding Certificates
RUN mkdir -p /etc/certs/sslterm
COPY certs/*.pem /etc/certs/sslterm/
COPY certs/*.crt /etc/certs/sslterm/

RUN touch /var/run/haproxy.pid
