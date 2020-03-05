/*
 * Copyright (c) 2018, WSO2 Inc. (http://wso2.com) All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.ballerinalang.platform.playground.controller.containercluster;

import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.client.Watcher;

import java.util.List;

/**
 * Container runtime client contract.
 */
public interface ContainerRuntimeClient {

    public boolean createDeployment(int deploymentNameSuffix, String rootDomainName, String reason);

    public boolean createService(int serviceNameSuffix, String rootDomainName, String reason);

    public boolean deleteDeployment(String deploymentName);

    public boolean deleteService(String serviceName);

    public List<String> getDeployments();

    public List<String> getServices();

    public boolean deploymentExists(String deploymentName);

    public boolean serviceExists(String serviceName);

    public void watchWithWatcher(Watcher<Event> watcher);
}