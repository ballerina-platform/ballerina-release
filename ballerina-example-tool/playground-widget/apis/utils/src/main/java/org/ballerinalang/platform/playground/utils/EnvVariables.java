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
package org.ballerinalang.platform.playground.utils;

/**
 * Contains various env vars available to apis
 */
public class EnvVariables {
    // environment variables
    public static final String ENV_BPG_REDIS_WRITE_HOST = "BPG_REDIS_WRITE_HOST";
    public static final String ENV_BPG_REDIS_WRITE_PORT = "BPG_REDIS_WRITE_PORT";
    public static final String ENV_BPG_REDIS_READ_HOST = "BPG_REDIS_READ_HOST";
    public static final String ENV_BPG_REDIS_READ_PORT = "BPG_REDIS_READ_PORT";
    public static final String ENV_BPG_USE_IN_MEMORY_CACHE = "BPG_USE_IN_MEMORY_CACHE";
    public static final String ENV_BPG_LAUNCHER_SELF_URL = "BPG_LAUNCHER_SELF_URL";
    public static final String ENV_BPG_CONTROLLER_INTERNAL_URL = "BPG_CONTROLLER_INTERNAL_URL";
    public static final String ENV_IS_LAUNCHER_CACHE = "BPG_LAUNCHER_CACHE_NODE";
    public static final String ENV_BPG_CACHE_MOUNT = "BPG_CACHE_MOUNT";
    public static final String ENV_BPG_LAUNCHER_CPU_LIMIT = "BPG_LAUNCHER_CPU_LIMIT";
    public static final String ENV_BPG_LAUNCHER_CPU_REQUEST = "BPG_LAUNCHER_CPU_REQUEST";
}
