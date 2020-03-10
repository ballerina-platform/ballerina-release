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

import io.netty.handler.codec.http.HttpHeaderNames;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.ballerinalang.platform.playground.controller.util.Constants;
import org.ballerinalang.platform.playground.utils.MemberConstants;
import org.ballerinalang.platform.playground.utils.cache.CacheUtils;
import org.ballerinalang.platform.playground.utils.model.LauncherRequest;
import org.ballerinalang.platform.playground.utils.model.LauncherResponse;
import org.ballerinalang.platform.playground.utils.model.StatusUpdateRequest;

import javax.ws.rs.Consumes;
import javax.ws.rs.OPTIONS;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

/**
 * The API for the Controller Service.
 */
@Path(value = "/api")
public class ControllerService {

    private static final Log log = LogFactory.getLog(ControllerService.class);

    private ControllerServiceManager serviceManager;

    public ControllerService(ControllerServiceManager serviceManager) {
        this.serviceManager = serviceManager;
    }

    @OPTIONS
    @Path("/launcher")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response validateAndParseOptions() {
        return Response
                .ok()
                .header(HttpHeaderNames.ACCESS_CONTROL_MAX_AGE.toString(), "600 ")
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN.toString(), "*")
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_CREDENTIALS.toString(), "true")
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_METHODS.toString(),
                        "POST, GET, PUT, UPDATE, DELETE, OPTIONS, HEAD")
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_HEADERS.toString(),
                        HttpHeaderNames.CONTENT_TYPE.toString() + ", " + HttpHeaderNames.ACCEPT.toString()
                                + ", X-Requested-With")
                .build();
    }

    /**
     * Provide a launcher URL.
     * <p>
     * A Launcher URL can be a free launcher instance or the URL to the Cache Responder, based on the
     * availability of the Cached responses.
     *
     * @param request The {@link LauncherRequest} object
     * @return A {@link LauncherResponse}
     */
    @POST
    @Path("/launcher")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response allocateLauncher(LauncherRequest request) {
        String outputCacheId = CacheUtils.getOutputCacheID(request.getSource(), request.getCurl());
        LauncherResponse response;
        if (CacheUtils.cacheExists(outputCacheId)) {
            String cacheResponderUrl = serviceManager.getCacheResponderUrl();
            response = new LauncherResponse(cacheResponderUrl, outputCacheId);
        } else {
            // Get a free launcher URL
            String launcherUrl = serviceManager.allocateFreeLauncher();
            if (launcherUrl != null) {
                response = new LauncherResponse(launcherUrl);
            } else {
                return buildNotFoundResponse();
            }
        }
        return Response.status(Response.Status.OK)
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN.toString(), '*')
                .type(MediaType.APPLICATION_JSON)
                .entity(response)
                .build();
    }

    /**
     * Mark a particular launcher as busy or free
     *
     * @param launcherSubdomain The String launcher subdomain, ex: launcher-1, to be set status for
     * @param request           The {@link StatusUpdateRequest}
     * @return The success or failure of the operation.
     */
    @POST
    @Path("/launcher/{" + Constants.PATH_PARAM_LAUNCHER_URL + "}")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response setLauncherStatus(
            @PathParam(Constants.PATH_PARAM_LAUNCHER_URL) String launcherSubdomain,
            StatusUpdateRequest request) {

        // Check if sent status is valid
        switch (request.getStatus()) {
            case MemberConstants.MEMBER_STATUS_FREE:
                if (serviceManager.markLauncherFree(launcherSubdomain)) {
                    log.info("Marking launcher [URL] " + launcherSubdomain + " as free...");
                    return Response.status(Response.Status.OK)
                            .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN.toString(), '*')
                            .build();
                } else {
                    log.warn("Launcher [URL] " + launcherSubdomain + " not found.");
                    return buildNotFoundResponse();
                }
            case MemberConstants.MEMBER_STATUS_BUSY:
                if (serviceManager.markLauncherBusy(launcherSubdomain)) {
                    log.info("Marking launcher [URL] " + launcherSubdomain + " as busy...");
                    return Response.status(Response.Status.OK)
                            .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN.toString(), '*')
                            .build();
                } else {
                    log.warn("Launcher [URL] " + launcherSubdomain + " not found.");
                    return buildNotFoundResponse();
                }
            default:
                log.warn("Invalid launcher status: " + launcherSubdomain);
                return Response.status(Response.Status.BAD_REQUEST)
                        .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN.toString(), '*')
                        .build();
        }
    }

    /**
     * Build a 404 Not Found HTTP Response.
     *
     * @return
     */
    private Response buildNotFoundResponse() {
        return Response.status(Response.Status.NOT_FOUND)
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN.toString(), '*')
                .build();
    }
}
