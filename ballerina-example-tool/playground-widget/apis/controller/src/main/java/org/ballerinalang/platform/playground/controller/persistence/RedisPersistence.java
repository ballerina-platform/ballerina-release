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

package org.ballerinalang.platform.playground.controller.persistence;

import org.ballerinalang.platform.playground.utils.MemberConstants;
import org.ballerinalang.platform.playground.utils.RedisClient;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.ScanParams;
import redis.clients.jedis.ScanResult;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Redis Persistence
 */
public class RedisPersistence implements Persistence {

    // Redis keys
    private static final String CACHE_KEY_LAUNCHERS_LIST = "CACHE_KEY_FREE_LAUNCHERS_LIST";

    private RedisClient redisClient;

    public RedisPersistence() {
        redisClient = RedisClient.getInstance();
    }

    @Override
    public void addFreeLaunchers(List<String> launcherUrls) {
        Map<String, String> launchers = launcherUrls.stream()
                .collect(Collectors.toMap((url) -> url, (url) -> MemberConstants.MEMBER_STATUS_FREE));
        try (Jedis client = redisClient.getClient()) {
            client.hmset(CACHE_KEY_LAUNCHERS_LIST, launchers);
        }
    }

    @Override
    public void addFreeLauncher(String launcherUrl) {
        try (Jedis client = redisClient.getClient()) {
           client.hset(CACHE_KEY_LAUNCHERS_LIST, launcherUrl, MemberConstants.MEMBER_STATUS_FREE);
        }
    }

    @Override
    public void unregisterLauncher(String launcherUrl) {
        try (Jedis client = redisClient.getClient()) {
            if (client.hexists(CACHE_KEY_LAUNCHERS_LIST, launcherUrl)) {
                client.hdel(CACHE_KEY_LAUNCHERS_LIST, launcherUrl);
            }
        }
    }

    @Override
    public List<String> getFreeLauncherUrls() {
        return searchLaunchersByStatus(MemberConstants.MEMBER_STATUS_FREE);
    }

    @Override
    public List<String> getBusyLauncherUrls() {
        return searchLaunchersByStatus(MemberConstants.MEMBER_STATUS_BUSY);
    }

    @Override
    public List<String> getTotalLauncherUrls() {
        try (Jedis client = redisClient.getClient()) {
            return new ArrayList<>(client.hkeys(CACHE_KEY_LAUNCHERS_LIST));
        }
    }

    @Override
    public boolean markLauncherAsFree(String launcherUrl) {
        try (Jedis client = redisClient.getClient()) {
            client.hset(CACHE_KEY_LAUNCHERS_LIST, launcherUrl, MemberConstants.MEMBER_STATUS_FREE);
        }
        return true;
    }

    @Override
    public boolean markLauncherAsBusy(String launcherUrl) {
        try (Jedis client = redisClient.getClient()) {
            client.hset(CACHE_KEY_LAUNCHERS_LIST, launcherUrl, MemberConstants.MEMBER_STATUS_BUSY);
        }
        return true;
    }

    @Override
    public boolean launcherExists(String launcherUrl) {
        try (Jedis client = redisClient.getClient()) {
            return client.hexists(CACHE_KEY_LAUNCHERS_LIST, launcherUrl);
        }
    }

    private List<String> searchLaunchersByStatus(String status) {
        List<String> freeLaunchers = new ArrayList<>();
        String cursor = "";
        ScanParams params = new ScanParams();
        try (Jedis client = redisClient.getClient()) {
            while (!cursor.equals("0")) {
                ScanResult<Map.Entry<String, String>> result
                        = client.hscan(CACHE_KEY_LAUNCHERS_LIST,
                        cursor.isEmpty() ? "0" : cursor, params);
                cursor = result.getStringCursor();
                result.getResult()
                        .stream()
                        .filter(entry -> entry.getValue().equals(status))
                        .forEach(entry -> freeLaunchers.add(entry.getKey()));
            }
            return freeLaunchers;
        }
    }
}
