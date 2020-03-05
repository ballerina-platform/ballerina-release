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
package org.ballerinalang.platform.playground.utils.cache;

import org.ballerinalang.platform.playground.utils.RedisClient;
import org.ballerinalang.platform.playground.utils.cmd.dto.RunCommand;
import org.ballerinalang.platform.playground.utils.model.LauncherRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;

import java.security.MessageDigest;
import java.util.Base64;

/**
 * Playground Cache Utils
 */
public class CacheUtils {

    private static final String UTF_8 = "UTF-8";

    private static final String MD_5 = "MD5";

    private static final Logger logger = LoggerFactory.getLogger(CacheUtils.class);

    public static String getOutputCacheID(RunCommand runCommand) {
        return getOutputCacheID(runCommand.getSource(), runCommand.getCurl());
    }

    public static String getOutputCacheID(String source, String curl) {
        try {
            byte[] bytesOfSource = source.getBytes(UTF_8);
            byte[] bytesOfCurl = curl.getBytes(UTF_8);
            MessageDigest md5 = MessageDigest.getInstance(MD_5);
            String sourceMd5 = new String(md5.digest(bytesOfSource));
            String curlMd5 = new String(md5.digest(bytesOfCurl));
            return new String(Base64.getEncoder().encode((curlMd5 + "." + sourceMd5).getBytes()));
        } catch (Exception e) {
            logger.error("Error while generating cache ID", e);
        }
        return null;
    }

    public static String getBuildCacheID(RunCommand runCommand) {
        return getBuildCacheID(runCommand.getSource());
    }

    public static String getBuildCacheID(String source) {
        try {
            byte[] bytesOfSource = source.getBytes(UTF_8);
            MessageDigest md5 = MessageDigest.getInstance(MD_5);
            return new String(md5.digest(bytesOfSource));
        } catch (Exception e) {
            logger.error("Error while generating cache ID", e);
        }
        return null;
    }

    public static boolean cacheExists(String cacheId) {
        RedisClient redisClient = RedisClient.getInstance();
        try (Jedis client = redisClient.getClient()) {
            return client.exists(cacheId);
        }
    }
}
