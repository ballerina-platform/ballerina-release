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
package org.ballerinalang.platform.playground.launcher.core.util;

import com.google.gson.Gson;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHeaders;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClients;
import org.ballerinalang.platform.playground.utils.EnvUtils;
import org.ballerinalang.platform.playground.utils.EnvVariables;
import org.ballerinalang.platform.playground.utils.MemberConstants;
import org.ballerinalang.platform.playground.utils.model.StatusUpdateRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Launcher Utils
 */
public class LauncherUtils {

    private static final Logger logger = LoggerFactory.getLogger(LauncherUtils.class);

    private static Gson gson = new Gson();

    public static void markNodeAsFree() {
        StatusUpdateRequest statusUpdateRequest = new StatusUpdateRequest();
        statusUpdateRequest.setStatus(MemberConstants.MEMBER_STATUS_FREE);
        String request = gson.toJson(statusUpdateRequest);

        try {
            HttpClient client = HttpClients.createDefault();
            HttpPost post = new HttpPost(getControllerURL());
            HttpEntity reqEntity = new StringEntity(request, ContentType.APPLICATION_JSON);
            logger.info("Using request: "+ request);
            post.setEntity(reqEntity);
            HttpResponse response = client.execute(post);
            if (response.getStatusLine().getStatusCode() != HttpStatus.SC_OK) {
                logger.error("Error while marking launcher node as free. "
                        + response.getStatusLine().getReasonPhrase());
                logger.error("Error code: "
                        + response.getStatusLine().getStatusCode());
                logger.error("Error response: "
                        + response.getEntity().toString());
            }
        } catch (Exception e) {
            logger.error("Error while marking launcher node as free. ", e);
        }
    }

    private static String getControllerURL() {
        String launcherSubDomain = EnvUtils.getRequiredEnvStringValue(EnvVariables.ENV_BPG_LAUNCHER_SELF_URL)
                .split("\\.")[0];
        String url = "http://"
                + EnvUtils.getRequiredEnvStringValue(EnvVariables.ENV_BPG_CONTROLLER_INTERNAL_URL)
                + "/api/launcher/"
                + launcherSubDomain;
        logger.info("Using " + url + " to mark node as free");
        return url;
    }
}
