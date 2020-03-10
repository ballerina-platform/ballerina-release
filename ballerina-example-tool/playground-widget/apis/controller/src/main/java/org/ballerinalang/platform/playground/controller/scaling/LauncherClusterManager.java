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

package org.ballerinalang.platform.playground.controller.scaling;

import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.ballerinalang.platform.playground.controller.containercluster.ContainerRuntimeClient;
import org.ballerinalang.platform.playground.controller.persistence.Persistence;
import org.ballerinalang.platform.playground.controller.util.Constants;
import org.ballerinalang.platform.playground.utils.EnvUtils;

import java.util.List;

/**
 * Manager class to handle the functionality on managing the Launcher Clusters and URL lists.
 */
public class LauncherClusterManager {

    private static final Log log = LogFactory.getLog(LauncherClusterManager.class);

    /**
     * The number of launcher instances to scale up at a time.
     */
    private int stepUp;

    /**
     * The number of launcher instances to scale down at a time.
     */
    private int stepDown;

    /**
     * The number of launcher instances to keep free at a given time. This will be honoured with more
     * priority than the max count.
     */
    private int freeBufferCount;

    /**
     * The number of maximum launcher instances to maintain.
     */
    private int maxCount;

    /**
     * The number of minimum launcher instances to be maintained at a given time.
     */
    private int desiredCount;

    /**
     * The root domain name of the deployment.
     */
    private String rootDomainName;

    private ContainerRuntimeClient runtimeClient;
    private Persistence persistence;

    public LauncherClusterManager(ContainerRuntimeClient runtimeClient, Persistence persistence) {

        // Auto scaling factors are defaulted to test values
        this.stepUp = EnvUtils.getEnvIntValue(Constants.ENV_STEP_UP, Constants.DEFAULT_STEP_UP);
        this.stepDown = EnvUtils.getEnvIntValue(Constants.ENV_STEP_DOWN, Constants.DEFAULT_STEP_DOWN);
        this.desiredCount = EnvUtils.getEnvIntValue(Constants.ENV_DESIRED_COUNT, Constants.DEFAULT_DESIRED_COUNT);
        this.maxCount = EnvUtils.getEnvIntValue(Constants.ENV_MAX_COUNT, Constants.DEFAULT_MAX_COUNT);
        this.freeBufferCount = EnvUtils.getEnvIntValue(Constants.ENV_FREE_BUFFER, Constants.DEFAULT_FREE_BUFFER);

        // Root domain name should be pronounced in the artifacts to be clear
        this.rootDomainName = EnvUtils.getRequiredEnvStringValue(Constants.ENV_ROOT_DOMAIN_NAME);

        this.runtimeClient = runtimeClient;
        this.persistence = persistence;

        // If there are no launcher URLs in the persistence, try to collect any running valid launchers.
        // This will mostly be effective in the initial startup only, as there will always be a pool of
        // launcher URLs in the persistence.
        if (getTotalLaunchers().size() == 0) {
            log.info("Initializing launcher list with any found existing launchers as free ones...");

            addAllDeploymentsAsFreeLaunchers();
        }
    }

    /**
     * Scale down by stepDown number of times, selecting the most recently created launchers to be killed.
     */
    public void scaleDown() {
        log.info("Scaling down by [Step Down] " + stepDown + " instances...");

        // Scale down by (1 x stepDown) at a time
        for (int i = 0; i < stepDown; i++) {
            // Get free launchers
            List<String> urlsToScaleDown = getFreeLaunchers();

            log.info("URLs to scale down: " + urlsToScaleDown.toString());

            // Sort by launcher url. This will sort the oldest first, making it possible to take the youngest out of the
            // tail
            urlsToScaleDown.sort((o1, o2) -> {
                int mySuffix = Integer.parseInt(o1.split("\\.")[0].substring(
                        (Constants.LAUNCHER_URL_PREFIX + "-").length()));

                int theirSuffix = Integer.parseInt(o2.split("\\.")[0].substring(
                        (Constants.LAUNCHER_URL_PREFIX + "-").length()));

                return Integer.compare(mySuffix, theirSuffix);
            });

            // Get the youngest free launcher URL
            String launcherUrlToDelete = urlsToScaleDown.get(urlsToScaleDown.size() - 1);

            log.info("Cutting down [Launcher URL] " + launcherUrlToDelete + "...");

            // Get object name from launcher URL
            String deploymentName = getObjectNameFromLauncherUrl(launcherUrlToDelete);

            // Delete deployment and service
            if (!deleteLauncher(deploymentName)) {
                log.error("Launcher deletion failed [Object Name] " + deploymentName);
            }
        }
    }

    /**
     * Scale up by stepUp number of launchers
     *
     * @param reason The String reason to scale up.
     */
    public void scaleUp(String reason) {
        log.info("Scaling up by [Step Up] " + stepUp + " instances...");

        // Where to start naming things
        int newNameSuffix = getLatestDeploymentNameSuffix() + 1;

        // scale up by (1 x stepUp) at a time
        for (int i = 0; i < stepUp; i++) {
            int deploymentNameSuffix = newNameSuffix + i;
            String deploymentName = Constants.BPG_APP_TYPE_LAUNCHER + "-" + deploymentNameSuffix;
            if (createLauncher(deploymentNameSuffix, reason)) {
                // Register the newly spawned launcher as a free one
                addFreeLauncher(deploymentName);
            } else {
                log.error("Launcher creation failed for [Object Name] " + deploymentName);
            }

        }
    }

    /**
     * Check max count, free buffer count, and scale down prioritizing free buffer count over
     * max count.
     */
    public void honourMaxCount() {
        // Get free and total counts
        int freeCount = getFreeLaunchers().size();
        int totalCount = getTotalLaunchers().size();

        // Scale down if max is exceeded, irrespective of free buffer count
        if (totalCount > maxCount) {
            log.info("Scaling down until [freeBufferCount] " + freeBufferCount + " is met since [Max Count] "
                    + maxCount + " has been exceeded.");

            while (freeCount <= freeBufferCount){
                log.info("Scaling DOWN: REASON -> [Total Count] " + totalCount + " > [Max Count] " + maxCount);
                scaleDown();
                freeCount = getFreeLaunchers().size();
            }

            totalCount = getTotalLaunchers().size();
            freeCount = getFreeLaunchers().size();

            log.info("Stats after scale down operation: [Total Count] " + totalCount + ", [Free Count] " + freeCount);

            return;
        }

        // Don't scale down if there are not enough free launchers
        if (freeCount <= freeBufferCount) {
            log.info("Not scaling down since [Free Count] " + freeCount + " <= [Free Buffer Size] " +
                    freeBufferCount + "...");
            return;
        }

        // Don't scale down if the desired count is not exceeded
        if (totalCount <= desiredCount) {
            log.info("Not scaling down since [Total Count] " + totalCount + " <= [Desired Count] " +
                    desiredCount + "...");
            return;
        }

        // Scale down if desired count is exceeded, but with more free launchers than buffer count by stepDown count
        // TODO: to test scale down
        if ((freeCount - stepDown) >= freeBufferCount) {
            log.info("Scaling DOWN: REASON -> [Total Count] " + totalCount + " > [Desired Count] " + desiredCount +
                    " AND [Free Count] - [Step Down] " + freeCount + " - " + stepDown +
                    " >= [Free Buffer Count] " + freeBufferCount);

            scaleDown();
            return;
        }

        // If after scaling down there wouldn't be enough free launchers, don't scale down
        log.info("Not scaling down since [Free Count] + [Step Down] " + freeCount + " + " + stepDown +
                " < [Free Buffer Count] " + freeBufferCount);
    }

    /**
     * Check if desired count is honoured, scale up if not.
     */
    public void honourDesiredCount() {
        int totalDeploymentCount = getDeployments().size();
//        log.info("[Total count] " + totalDeploymentCount + " [Desired Count] " + desiredCount);

        while (totalDeploymentCount < desiredCount) {
            log.info("Scaling UP: REASON -> [Total Count] " + totalDeploymentCount + " < [Desired Count] " +
                    desiredCount);

            scaleUp("honourDesiredCount");
            totalDeploymentCount = getDeployments().size();
        }
    }

    /**
     * Check if free buffer count is available.
     */
    public void honourFreeBufferCount() {
        // Check if there are enough free launchers
        int freeCount = getFreeLaunchers().size();

        while (freeCount < freeBufferCount) {
            if (getTotalLaunchers().size() > maxCount) {
                log.warn("Specified Maximum Concurrency has been exceeded, but scaling up will be permitted. If this " +
                        "message appears often increase maximum concurrency.");
            }

            log.info("Scaling UP: REASON -> [Free Count] " + freeCount + " < [Free Gap] " + freeBufferCount);
            scaleUp("honourFreeBufferCount");
            freeCount = getFreeLaunchers().size();
        }
    }

    /**
     * Check if there are Services without corresponding Deployments, and clean them up from the launcher
     * list.
     */
    public void cleanOrphanServices() {
        log.info("Cleaning orphan Services...");
        List<String> serviceNames = getServices();
        for (String serviceName : serviceNames) {
            if (serviceName.startsWith(Constants.BPG_APP_TYPE_LAUNCHER + "-") && !deploymentExists(serviceName)) {
                log.info("Cleaning orphan Service [Name] " + serviceName + "...");

                unregisterLauncherIfExistsByObjectName(serviceName);

                if (!runtimeClient.deleteService(serviceName)) {
                    log.error("Service deletion failed [Service Name] " + serviceName);
                }
            }
        }
    }

    /**
     * Check if there are Deployments without corresponding Services, and clean them up from the launcher
     * list.
     */
    public void cleanOrphanDeployments() {
        log.info("Cleaning orphan Deployments...");
        List<String> deploymentNames = getDeployments();
        for (String deploymentName : deploymentNames) {
            if (deploymentName.startsWith(Constants.BPG_APP_TYPE_LAUNCHER + "-") && !serviceExists(deploymentName)) {
                log.info("Cleaning orphan Deployment [Name] " + deploymentName + "...");

                unregisterLauncherIfExistsByObjectName(deploymentName);

                if (!runtimeClient.deleteDeployment(deploymentName)) {
                    log.error("Deployment deletion failed [Deployment Name] " + deploymentName);
                }
            }
        }
    }

    /**
     * Check if there are valid Services and Deployments for each launcher available on the launcher list.
     */
    public void validateLauncherUrls() {
        log.info("Validating the existing launcher URL list for missing deployments...");

        for (String launcherUrl : getTotalLaunchers()) {
            log.info("Validating [Launcher URL] " + launcherUrl + "...");
            String objectName = getObjectNameFromLauncherUrl(launcherUrl);
            if (!runtimeClient.deploymentExists(objectName) || !runtimeClient.serviceExists(objectName)) {
                log.info("Found an invalid launcher [URL] " + launcherUrl);
                // Just remove the reference to launcher now
                // cleanOrphan* jobs will clean any orphan deployments
                // desired count check will scale up if free count is reduced
                unregisterLauncherIfExists(launcherUrl);
            }
        }
    }

    /**
     * Get the list of Services on the K8S Cluster.
     *
     * @return
     */
    public List<String> getServices() {
        return runtimeClient.getServices();
    }

    /**
     * Get the list of Deployments on the K8S Cluster.
     *
     * @return
     */
    public List<String> getDeployments() {
        return runtimeClient.getDeployments();
    }

    /**
     * Check if a Deploymen exists by the given name.
     *
     * @param deploymentName
     * @return
     */
    public boolean deploymentExists(String deploymentName) {
        return runtimeClient.deploymentExists(deploymentName);
    }

    /**
     * Check if a Service exists by the given name.
     *
     * @param serviceName
     * @return
     */
    public boolean serviceExists(String serviceName) {
        return runtimeClient.serviceExists(serviceName);
    }

    /**
     * Iterate through the Deployments list and add any valid Deployment+Service as a free Launcher.
     */
    private void addAllDeploymentsAsFreeLaunchers() {
        List<String> deployments = getDeployments();
        log.info("Found " + deployments.size() + " deployments to be added");
        for (String deployment : deployments) {
            if (runtimeClient.serviceExists(deployment)) {
                addFreeLauncher(deployment);
            } else {
                log.info("Deployment " + deployment + " doesn't have a Service that exposes it. Not adding as a launcher...");
            }
        }
    }

    /**
     * Get the list of free launchers from the persistence.
     *
     * @return
     */
    public List<String> getFreeLaunchers() {
        return persistence.getFreeLauncherUrls();
    }

    /**
     * Get the full list of launchers from the persistence.
     *
     * @return
     */
    public List<String> getTotalLaunchers() {
        return persistence.getTotalLauncherUrls();
    }

    /**
     * Mark a launcher by the given subdomain as busy.
     *
     * @param launcherSubDomain
     * @return
     */
    public boolean markLauncherAsBusyBySubDomain(String launcherSubDomain) {
        return markLauncherAsBusy(launcherSubDomain + "." + rootDomainName);
    }

    /**
     * Mark the given launcher URL as busy.
     *
     * @param launcherUrl
     * @return
     */
    public boolean markLauncherAsBusy(String launcherUrl) {
        if (persistence.launcherExists(launcherUrl)) {
            return persistence.markLauncherAsBusy(launcherUrl);
        }

        return false;
    }

    /**
     * Mark a launcher by the given subdomain as free.
     *
     * @param launcherSubDomain
     * @return
     */
    public boolean markLauncherAsFreeBySubDomain(String launcherSubDomain) {
        return markLauncherAsFree(launcherSubDomain + "." + rootDomainName);
    }

    /**
     * Makr the given launcher URL as free.
     *
     * @param launcherUrl
     * @return
     */
    public boolean markLauncherAsFree(String launcherUrl) {
        if (persistence.launcherExists(launcherUrl)) {
            return persistence.markLauncherAsFree(launcherUrl);
        }

        return false;
    }

    /**
     * Delete launcher URL derived from the object name, from the list of launchers, if it exists, and delete from the K8S cluster.
     *
     * @param deploymentName
     * @return
     */
    private boolean deleteLauncher(String deploymentName) {
        unregisterLauncherIfExistsByObjectName(deploymentName);

        boolean svcDeleted = runtimeClient.deleteService(deploymentName);
        boolean depDeleted = runtimeClient.deleteDeployment(deploymentName);

        return svcDeleted && depDeleted;
    }

    /**
     * Delete launcher URL, derived from the object name, from the list of launchers, if it exists.
     *
     * @param objectName
     */
    private void unregisterLauncherIfExistsByObjectName(String objectName) {
        // Unregister from launcher list
        String launcherUrl = getLauncherUrlFromObjectName(objectName);
        unregisterLauncherIfExists(launcherUrl);
    }

    /**
     * Delete launcher URL from the list of launchers, if it exists.
     *
     * @param launcherUrl
     */
    private void unregisterLauncherIfExists(String launcherUrl) {
        log.info("Unregistering launcher [URL] " + launcherUrl);
        if (persistence.launcherExists(launcherUrl)) {
            persistence.unregisterLauncher(launcherUrl);
        } else {
            log.debug("Launcher URL not found: " + launcherUrl);
        }
    }

    /**
     * Add a new launcher URL by creating a K8S Deployment+Service pair and adding the entry to persistence.
     *
     * @param deploymentNameSuffix
     * @param reason
     * @return
     */
    private boolean createLauncher(int deploymentNameSuffix, String reason) {
        boolean depCreated = runtimeClient.createDeployment(deploymentNameSuffix, rootDomainName, reason);
        boolean svcCreated = runtimeClient.createService(deploymentNameSuffix, rootDomainName, reason);

        return depCreated && svcCreated;
    }

    /**
     * Add a launcher URL by the given object name to the persistence.
     *
     * @param deploymentName
     */
    private void addFreeLauncher(String deploymentName) {
        persistence.addFreeLauncher(getLauncherUrlFromObjectName(deploymentName));
    }

    /**
     * Get the object name used in the K8S cluster, from the launcher URL.
     *
     * @param launchUrl
     * @return
     */
    private String getObjectNameFromLauncherUrl(String launchUrl) {
        if (launchUrl != null) {
            String[] domainParts = launchUrl.split("\\.");
            return domainParts[0].replace(Constants.LAUNCHER_URL_PREFIX, Constants.BPG_APP_TYPE_LAUNCHER);
        }

        throw new IllegalArgumentException("Null launcher URL cannot be processed.");
    }

    /**
     * Get the launcher URL used in the persistence by the given object name in the K8S cluster.
     *
     * @param objectName
     * @return
     */
    private String getLauncherUrlFromObjectName(String objectName) {
        if (objectName != null) {
            return objectName.replace(Constants.BPG_APP_TYPE_LAUNCHER, Constants.LAUNCHER_URL_PREFIX) +
                    "." +
                    rootDomainName;
        }

        throw new IllegalArgumentException("Null Object name cannot be processed.");
    }

    /**
     * Get the last created increment number of the Deployment/Service in the K8S cluster.
     *
     * @return
     */
    private int getLatestDeploymentNameSuffix() {
        List<String> deploymentList = getDeployments();
//        log.info("Currently have " + deploymentList.size() + " deployments...");
        if (deploymentList.size() > 0) {
            deploymentList.sort((o1, o2) -> {
                int mySuffix = Integer.parseInt(o1.substring((Constants.BPG_APP_TYPE_LAUNCHER + "-").length()));
                int theirSuffix = Integer.parseInt(o2.substring((Constants.BPG_APP_TYPE_LAUNCHER + "-").length()));

                return Integer.compare(mySuffix, theirSuffix);
            });

//            log.info("Sorted deployments: " + deploymentList.toString());
            String lastElement = deploymentList.get(deploymentList.size() - 1);
//            log.info("Last element: " + lastElement);
            String lastLauncherSuffix = lastElement.substring((Constants.BPG_APP_TYPE_LAUNCHER + "-").length());

//            log.info("Picking last deployment suffix: " + lastLauncherSuffix);
            return Integer.parseInt(lastLauncherSuffix);
        }

        return 0;
    }

    /**
     * Start watching the K8S events to see if any related Deployments or Services are being deleted.
     * If found, run a cleanup of the launcher URLs.
     * <p>
     * Note: This is too slow. Events take about 2 minutes to be received.
     */
    public void watchAndClean() {
        runtimeClient.watchWithWatcher(new Watcher<Event>() {

            @Override
            public void eventReceived(Action action, Event resource) {
                if ((resource.getInvolvedObject().getKind().equals("Deployment") ||
                        resource.getInvolvedObject().getKind().equals("Service"))
                        && resource.getInvolvedObject().getName().startsWith(Constants.BPG_APP_TYPE_LAUNCHER)
                        && (action == Action.DELETED || action == Action.MODIFIED)) {

                    log.info("Received "
                            + action.toString() + " event for "
                            + resource.getInvolvedObject().getKind() + " "
                            + resource.getInvolvedObject().getName());

                    cleanOrphanDeployments();
                    cleanOrphanServices();
                } else {
                    log.debug("Received action " + action.toString() + " for resource "
                            + resource.getInvolvedObject().getKind() + ":"
                            + resource.getInvolvedObject().getName());
                }
            }

            @Override
            public void onClose(KubernetesClientException cause) {
                log.info("Shutting down Event Watcher...");
            }
        });
    }
}
