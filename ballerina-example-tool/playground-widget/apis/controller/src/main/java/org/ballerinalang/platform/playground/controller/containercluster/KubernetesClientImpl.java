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

import io.fabric8.kubernetes.api.model.Container;
import io.fabric8.kubernetes.api.model.ContainerPort;
import io.fabric8.kubernetes.api.model.ContainerPortBuilder;
import io.fabric8.kubernetes.api.model.EnvVar;
import io.fabric8.kubernetes.api.model.EnvVarBuilder;
import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.api.model.IntOrString;
import io.fabric8.kubernetes.api.model.NFSVolumeSource;
import io.fabric8.kubernetes.api.model.ObjectMeta;
import io.fabric8.kubernetes.api.model.ObjectMetaBuilder;
import io.fabric8.kubernetes.api.model.PodSpec;
import io.fabric8.kubernetes.api.model.PodSpecBuilder;
import io.fabric8.kubernetes.api.model.PodTemplateSpec;
import io.fabric8.kubernetes.api.model.PodTemplateSpecBuilder;
import io.fabric8.kubernetes.api.model.Quantity;
import io.fabric8.kubernetes.api.model.ResourceRequirementsBuilder;
import io.fabric8.kubernetes.api.model.Service;
import io.fabric8.kubernetes.api.model.ServiceBuilder;
import io.fabric8.kubernetes.api.model.ServiceList;
import io.fabric8.kubernetes.api.model.ServicePort;
import io.fabric8.kubernetes.api.model.ServiceSpec;
import io.fabric8.kubernetes.api.model.ServiceSpecBuilder;
import io.fabric8.kubernetes.api.model.Volume;
import io.fabric8.kubernetes.api.model.VolumeBuilder;
import io.fabric8.kubernetes.api.model.VolumeMount;
import io.fabric8.kubernetes.api.model.extensions.Deployment;
import io.fabric8.kubernetes.api.model.extensions.DeploymentBuilder;
import io.fabric8.kubernetes.api.model.extensions.DeploymentList;
import io.fabric8.kubernetes.api.model.extensions.DeploymentSpec;
import io.fabric8.kubernetes.api.model.extensions.DeploymentSpecBuilder;
import io.fabric8.kubernetes.client.DefaultKubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.Watcher;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.ballerinalang.platform.playground.controller.util.Constants;
import org.ballerinalang.platform.playground.utils.EnvUtils;
import org.ballerinalang.platform.playground.utils.EnvVariables;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * K8S implementation of the Container Runtime Client.
 */
public class KubernetesClientImpl implements ContainerRuntimeClient {

    private static final Log log = LogFactory.getLog(KubernetesClientImpl.class);

    private KubernetesClient k8sClient;
    private String namespace;

    public KubernetesClientImpl(String namespace) {
        this.k8sClient = new DefaultKubernetesClient();
        this.namespace = namespace;
    }

    @Override
    public boolean createDeployment(int deploymentNameSuffix, String rootDomainName, String reason) {
        String deploymentName = Constants.BPG_APP_TYPE_LAUNCHER + "-" + deploymentNameSuffix;

        String serviceSubDomain = Constants.LAUNCHER_URL_PREFIX + "-" + deploymentNameSuffix;
        String launcherSelfUrl = serviceSubDomain + "." + rootDomainName;

        log.info("Creating Deployment [Name] " + deploymentName + "...");

        // Lookup launcher image name
        String launcherImageName = EnvUtils.getRequiredEnvStringValue(Constants.ENV_LAUNCHER_IMAGE_NAME);

        // Labels for the to be created deployment
        Map<String, String> labels = new HashMap<>();
        labels.put("app", deploymentName);
        labels.put("appType", Constants.BPG_APP_TYPE_LAUNCHER);
        labels.put("creator", EnvUtils.getEnvStringValue(Constants.ENV_CONTROLLER_ROLE));
        labels.put("reason", reason);

        // Container spec
        Container launcherContainer = new Container();

        // Add container info
        launcherContainer.setName(Constants.BPG_APP_TYPE_LAUNCHER + "-container");
        launcherContainer.setImage(launcherImageName);
        launcherContainer.setImagePullPolicy("Always");

        // MSF4J port
        List<ContainerPort> containerPorts = new ArrayList<>();
        containerPorts.add(new ContainerPortBuilder()
                .withContainerPort(8080)
                .build());

        launcherContainer.setPorts(containerPorts);

        String cpuLimit = EnvUtils.getEnvStringValue(EnvVariables.ENV_BPG_LAUNCHER_CPU_LIMIT,
                Constants.DEFAULT_CPU_LIMIT);
        String cpuRequest = EnvUtils.getEnvStringValue(EnvVariables.ENV_BPG_LAUNCHER_CPU_REQUEST,
                Constants.DEFAULT_CPU_REQUEST);
        Map<String, Quantity> limits = new HashMap<>();
        limits.put(Constants.CPU_RESOURCE, new Quantity(cpuLimit));

        Map<String, Quantity> requests = new HashMap<>();
        requests.put(Constants.CPU_RESOURCE, new Quantity(cpuRequest));

        ResourceRequirementsBuilder resourceRequirementsBuilder = new ResourceRequirementsBuilder();
        // resourceRequirementsBuilder.withLimits(limits);
        // resourceRequirementsBuilder.withRequests(requests);
        launcherContainer.setResources(resourceRequirementsBuilder.build());

        // Volume mount to container
        List<VolumeMount> volumeMounts = new ArrayList<>();
        VolumeMount nfsVolumeMount = new VolumeMount("/mnt/build/cache", "nfs-build-cache",
                false, "");
        volumeMounts.add(nfsVolumeMount);

        launcherContainer.setVolumeMounts(volumeMounts);

        List<Container> containers = new ArrayList<>();
        containers.add(launcherContainer);

        // Env vars should be set so that the launcher is able to
        // 1. Communicate with the persistence
        // 2. Register itself as free when a job is done
        // 3. Perform proper role (cache node vs build node)
        List<EnvVar> envVarList = new ArrayList<>();

        try {
            envVarList.add(buildEnvVar(EnvVariables.ENV_BPG_REDIS_WRITE_HOST,
                    EnvUtils.getRequiredEnvStringValue(EnvVariables.ENV_BPG_REDIS_WRITE_HOST)));
            envVarList.add(buildEnvVar(EnvVariables.ENV_BPG_REDIS_WRITE_PORT,
                    EnvUtils.getRequiredEnvStringValue(EnvVariables.ENV_BPG_REDIS_WRITE_PORT)));
            envVarList.add(buildEnvVar(EnvVariables.ENV_BPG_REDIS_READ_HOST,
                    EnvUtils.getRequiredEnvStringValue(EnvVariables.ENV_BPG_REDIS_READ_HOST)));
            envVarList.add(buildEnvVar(EnvVariables.ENV_BPG_REDIS_READ_PORT,
                    EnvUtils.getRequiredEnvStringValue(EnvVariables.ENV_BPG_REDIS_READ_PORT)));
            envVarList.add(buildEnvVar(Constants.ENV_BPG_NAMESPACE, namespace));
            envVarList.add(buildEnvVar(EnvVariables.ENV_BPG_LAUNCHER_SELF_URL, launcherSelfUrl));
            envVarList.add(buildEnvVar(EnvVariables.ENV_IS_LAUNCHER_CACHE, "false"));
            envVarList.add(buildEnvVar(EnvVariables.ENV_BPG_CONTROLLER_INTERNAL_URL,
                    EnvUtils.getRequiredEnvStringValue(EnvVariables.ENV_BPG_CONTROLLER_INTERNAL_URL)));
        } catch (IllegalArgumentException e) {
            log.error("Error while populating environment variables for the launcher. Aborting creation.", e);
            return false;
        }

        launcherContainer.setEnv(envVarList);

        // NFS volume
        String nfsServerIP = EnvUtils.getRequiredEnvStringValue(Constants.ENV_BGP_NFS_SERVER_IP);

        List<Volume> volumes = new ArrayList<>();
        Volume nfsVolume = new VolumeBuilder()
                .withName("nfs-build-cache")
                .withNfs(new NFSVolumeSource("/exports/build-cache", false, nfsServerIP))
                .build();
        volumes.add(nfsVolume);

        PodSpec podSpec = new PodSpecBuilder()
                .withContainers(containers)
                .withVolumes(volumes)
                .build();

        PodTemplateSpec podTemplateSpec = new PodTemplateSpecBuilder()
                .withMetadata(new ObjectMetaBuilder()
                        .withLabels(labels)
                        .build())
                .withSpec(podSpec)
                .build();

        DeploymentSpec deploymentSpec = new DeploymentSpecBuilder()
                .withReplicas(1)
                .withTemplate(podTemplateSpec)
                .build();

        Deployment deployment = new DeploymentBuilder()
                .withKind("Deployment")
                .withMetadata(new ObjectMetaBuilder()
                        .withName(deploymentName)
                        .build())
                .withSpec(deploymentSpec)
                .build();

        // Make API call to create deployment
        Deployment createdDeployment = k8sClient.extensions().deployments().inNamespace(namespace).create(deployment);

        if (createdDeployment != null) {
            // Wait until deployment object is properly created
            while (!getDeployments().contains(deploymentName)) {
                log.info("Waiting until the deployment is completed...");
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    log.error("Wait interrupted. Unlikely.");
                }
            }

            return true;
        }

        return false;
    }

    @Override
    public boolean createService(int serviceNameSuffix, String rootDomainName, String reason) {
        String serviceSubDomain = Constants.LAUNCHER_URL_PREFIX + "-" + serviceNameSuffix;
        String serviceName = Constants.BPG_APP_TYPE_LAUNCHER + "-" + serviceNameSuffix;

        log.info("Creating Service with [Name] " + serviceName + " for [Sub Domain]" + serviceSubDomain + "...");

        // Service load balancer annotations
        Map<String, String> annotations = new HashMap<>();
        annotations.put("serviceloadbalancer/lb.cookie-sticky-session", "true");
        annotations.put("serviceloadbalancer/lb.host", serviceSubDomain + "." + rootDomainName);
        annotations.put("serviceloadbalancer/lb.sslTerm", "true");

        // Labels
        Map<String, String> labels = new HashMap<>();
        labels.put("app", serviceName);
        labels.put("appType", Constants.BPG_APP_TYPE_LAUNCHER);
        labels.put("creator", EnvUtils.getEnvStringValue(Constants.ENV_CONTROLLER_ROLE));
        labels.put("reason", reason);

        // Port to be exposed
        List<ServicePort> ports = new ArrayList<>();
        ServicePort servicePort = new ServicePort();
        servicePort.setName("https-port");
        servicePort.setPort(443);
        servicePort.setTargetPort(new IntOrString(
                EnvUtils.getEnvIntValue(Constants.ENV_BPG_LAUNCHER_HTTPS_PORT, Constants.DEFAULT_LAUNCHER_HTTPS_PORT)));
        ports.add(servicePort);

        // Pod selector
        Map<String, String> selector = new HashMap<>();
        selector.put("app", serviceName);

        ObjectMeta serviceMetadata = new ObjectMetaBuilder()
                .withName(serviceName)
                .withAnnotations(annotations)
                .withLabels(labels)
                .build();

        ServiceSpec serviceSpec = new ServiceSpecBuilder()
                .withPorts(ports)
                .withSelector(selector)
                .build();

        Service service = new ServiceBuilder()
                .withKind("Service")
                .withMetadata(serviceMetadata)
                .withSpec(serviceSpec)
                .build();

        Service createdService = k8sClient.services().inNamespace(namespace).create(service);

        if (createdService != null) {
            // Wait until Service object is properly created
            while (!getServices().contains(serviceName)) {
                log.info("Waiting until the service is completed...");
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    log.error("Wait interrupted. Unlikely.");
                }
            }

            return true;
        }

        return false;
    }

    @Override
    public boolean deleteDeployment(String deploymentName) {
        return k8sClient.extensions().deployments().inNamespace(namespace).withName(deploymentName).delete();
    }

    @Override
    public boolean deleteService(String serviceName) {
        return k8sClient.services().inNamespace(namespace).withName(serviceName).delete();
    }

    @Override
    public List<String> getDeployments() {
        DeploymentList depList = k8sClient.extensions().deployments()
                .inNamespace(namespace)
                .withLabel("appType", Constants.BPG_APP_TYPE_LAUNCHER)
                .list();

        List<String> depNameList = new ArrayList<>();
        for (Deployment deployment : depList.getItems()) {
            depNameList.add(deployment.getMetadata().getName());
        }

        return depNameList;
    }

    @Override
    public List<String> getServices() {
        ServiceList serviceList = k8sClient.services().inNamespace(namespace).withLabel("appType", Constants.BPG_APP_TYPE_LAUNCHER).list();
        List<String> serviceNameList = new ArrayList<>();
        for (Service service : serviceList.getItems()) {
            serviceNameList.add(service.getMetadata().getName());
        }

        return serviceNameList;
    }

    @Override
    public boolean deploymentExists(String deploymentName) {
        return k8sClient.extensions().deployments().inNamespace(namespace).withName(deploymentName).get() != null;
    }

    @Override
    public boolean serviceExists(String serviceName) {
        return k8sClient.services().inNamespace(namespace).withName(serviceName).get() != null;
    }

    @Override
    public void watchWithWatcher(Watcher<Event> watcher) {
        k8sClient.events().inNamespace(namespace).watch(watcher);
    }

    /**
     * Create an Environment Variable entry to be added to a Deployment.
     *
     * @param key
     * @param value
     * @return
     */
    private EnvVar buildEnvVar(String key, String value) {
        return new EnvVarBuilder()
                .withName(key)
                .withValue(value)
                .build();
    }
}
