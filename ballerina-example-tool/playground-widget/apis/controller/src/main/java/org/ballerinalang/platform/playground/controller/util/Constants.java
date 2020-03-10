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

package org.ballerinalang.platform.playground.controller.util;

/**
 * Constant values specific to the Controller roles.
 */
public class Constants {
    public static final String BPG_APP_TYPE_LAUNCHER = "bpg-launcher";
    public static final String LAUNCHER_URL_PREFIX = "launcher";

    // Controller roles
    public static final String CONTROLLER_ROLE_API_SERVER = "API_SERVER";
    public static final String CONTROLLER_ROLE_DESIRED_COUNT_CHECK = "DESIRED_CHECK";
    public static final String CONTROLLER_ROLE_MAX_COUNT_CHECK = "MAX_CHECK";
    public static final String CONTROLLER_ROLE_URL_VALIDATOR = "URL_VALIDATOR";
    public static final String CONTROLLER_ROLE_EVENT_WATCHER = "EVENT_WATCHER";

    // Environment variable keys
    public static final String ENV_CONTROLLER_ROLE = "BPG_CONTROLLER_ROLE";
    public static final String ENV_BPG_NAMESPACE = "BPG_NAMESPACE";
    public static final String ENV_LAUNCHER_IMAGE_NAME = "BPG_LAUNCHER_IMAGE_NAME";
    public static final String ENV_STEP_UP = "BPG_SCALING_STEP_UP";
    public static final String ENV_STEP_DOWN = "BPG_SCALING_STEP_DOWN";
    public static final String ENV_DESIRED_COUNT = "BPG_MIN_CONCURRENT_USERS";
    public static final String ENV_MAX_COUNT = "BPG_MAX_CONCURRENT_USERS";
    public static final String ENV_FREE_BUFFER = "BPG_SCALING_FREE_BUFFER";
    public static final String ENV_BGP_NFS_SERVER_IP = "BGP_NFS_SERVER_IP";
    public static final String ENV_ROOT_DOMAIN_NAME = "ROOT_DOMAIN_NAME";
    public static final String ENV_BPG_LAUNCHER_HTTPS_PORT = "BPG_LAUNCHER_HTTPS_PORT";

    // Default values
    public static final String DEFAULT_BALLERINA_PLAYGROUND_NAMESPACE = "ballerina-playground";
    public static final int DEFAULT_STEP_UP = 2;
    public static final int DEFAULT_STEP_DOWN = 1;
    public static final int DEFAULT_DESIRED_COUNT = 5;
    public static final int DEFAULT_MAX_COUNT = 10;
    public static final int DEFAULT_FREE_BUFFER = 2;
    public static final int DEFAULT_LAUNCHER_HTTPS_PORT = 8443;

    // API Path Parameters
    public static final String PATH_PARAM_LAUNCHER_URL = "launcher-url";
    public static final String CPU_RESOURCE = "cpu";
    public static final String DEFAULT_CPU_LIMIT = "4";
    public static final String DEFAULT_CPU_REQUEST = "0.5";
}
