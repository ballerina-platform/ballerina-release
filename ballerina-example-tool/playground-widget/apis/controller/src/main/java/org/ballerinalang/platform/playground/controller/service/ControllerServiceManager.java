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

package org.ballerinalang.platform.playground.controller.service;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.ballerinalang.platform.playground.controller.scaling.LauncherClusterManager;
import org.ballerinalang.platform.playground.controller.util.Constants;
import org.ballerinalang.platform.playground.utils.EnvUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

/**
 * Perform business logic to help the Controller API.
 */
public class ControllerServiceManager {
    private static final Log log = LogFactory.getLog(ControllerServiceManager.class);

    private LauncherClusterManager clusterManager;

    public ControllerServiceManager(LauncherClusterManager clusterManager) {
        this.clusterManager = clusterManager;
    }

    /**
     * Provide a launcher URL.
     *
     * @return A String URL pointing to a communicable launcher instance.
     */
    synchronized String allocateFreeLauncher() {
        log.info("Looking for free Launchers to allocate...");
        List<String> freeLaunchers = clusterManager.getFreeLaunchers();

        if (freeLaunchers == null || freeLaunchers.size() == 0) {
            log.error("No free launchers available. Increase Max Launcher Count.");

            return null;
        }

        // Get a launcher URL and mark it as busy
        String launcherToAllocate = freeLaunchers.get(0);
        clusterManager.markLauncherAsBusy(launcherToAllocate);

        // Scale check and scale up if needed
        clusterManager.honourFreeBufferCount();

        log.info("Allocating launcher URL: " + launcherToAllocate + "...");
        return launcherToAllocate;
    }

    /**
     * Mark a particular launcher as a free one, to be allocated to a subsequent request.
     *
     * @param launcherSubDomain The subdomain, ex: launcher-1, of the launcher to be marked.
     * @return True if the launcher was successfully marked as free, False if launcher was
     * not found, or failed to be marked as free
     */
    synchronized boolean markLauncherFree(String launcherSubDomain) {
        return clusterManager.markLauncherAsFreeBySubDomain(launcherSubDomain);
    }

    /**
     * Mark a particular launcher as a busy one, to avoid being allocated to a subsequent request.
     *
     * @param launcherSubDomain The subdomain, ex: launcher-1, of the launcher to be marked.
     * @return True if the launcher was successfully marked as busy, False if launcher was
     * not found, or failed to be marked as busy
     */
    synchronized boolean markLauncherBusy(String launcherSubDomain) {
        return clusterManager.markLauncherAsBusyBySubDomain(launcherSubDomain);
    }

    /**
     * Get the URL to the Cache responder.
     *
     * @return The String URL to the Cache Responder
     */
    String getCacheResponderUrl() {
        String cacheResponderSubDomain = "cache";
        String rootDomainName = EnvUtils.getRequiredEnvStringValue(Constants.ENV_ROOT_DOMAIN_NAME);

        return cacheResponderSubDomain + "." + rootDomainName;
    }
}
