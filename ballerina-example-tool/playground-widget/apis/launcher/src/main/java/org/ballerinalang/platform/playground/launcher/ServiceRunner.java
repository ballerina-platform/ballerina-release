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
package org.ballerinalang.platform.playground.launcher;

import org.ballerinalang.platform.playground.launcher.core.cache.adaptor.CacheStorageAdaptor;
import org.ballerinalang.platform.playground.launcher.core.cache.adaptor.InMemoryCacheStorageAdaptor;
import org.ballerinalang.platform.playground.utils.EnvUtils;
import org.ballerinalang.platform.playground.utils.EnvVariables;
import org.ballerinalang.platform.playground.utils.exception.mapper.CatchAllExceptionMapper;
import org.wso2.msf4j.MicroservicesRunner;

/**
 * Entry point for micro services server
 */
public class ServiceRunner {

    private static CacheStorageAdaptor inMemoryCache;

    public static void main(String[] args) {
        if (EnvUtils.getEnvStringValue(EnvVariables.ENV_BPG_USE_IN_MEMORY_CACHE) !=  null) {
            inMemoryCache = new InMemoryCacheStorageAdaptor();
        }
        MicroservicesRunner microservicesRunner = new MicroservicesRunner();
        microservicesRunner.deployWebSocketEndpoint(new LauncherService());
        microservicesRunner.addExceptionMapper(new CatchAllExceptionMapper());
        microservicesRunner.start();
    }

    public static CacheStorageAdaptor getInMemoryCache() {
        return inMemoryCache;
    }
}
