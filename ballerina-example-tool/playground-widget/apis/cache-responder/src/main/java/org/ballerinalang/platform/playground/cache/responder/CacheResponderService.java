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
package org.ballerinalang.platform.playground.cache.responder;

import com.google.gson.Gson;
import org.ballerinalang.platform.playground.launcher.core.RunSession;
import org.ballerinalang.platform.playground.utils.cache.CacheUtils;
import org.ballerinalang.platform.playground.utils.cmd.CommandUtils;
import org.ballerinalang.platform.playground.utils.cmd.dto.Command;
import org.ballerinalang.platform.playground.utils.cmd.dto.RunCommand;
import org.ballerinalang.platform.playground.utils.exception.mapper.ErrorResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.websocket.CloseReason;
import javax.websocket.OnClose;
import javax.websocket.OnError;
import javax.websocket.OnMessage;
import javax.websocket.OnOpen;
import javax.websocket.Session;
import javax.websocket.server.ServerEndpoint;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * Ballerina Cache Responder Service for playground
 */
@ServerEndpoint(value = "/api/run")
public class CacheResponderService {

    private static final Logger logger = LoggerFactory.getLogger(CacheResponderService.class);

    private Map<String, RunSession> runSessionMap = new HashMap<String, RunSession>();

    private Gson gson = new Gson();

    @OnOpen
    public void onOpen (Session session) {
        runSessionMap.put(session.getId(), new RunSession(session));
    }

    @OnMessage
    public void onTextMessage(String message, Session session) throws IOException {
        Command command = CommandUtils.fromJson(message);
        if (command instanceof RunCommand) {
            RunCommand runCommand = (RunCommand) command;
            String outputCacheID = runCommand.getCacheId();
            if (outputCacheID != null && CacheUtils.cacheExists(outputCacheID)) {
                runSessionMap.get(session.getId()).processCommand(runCommand);
            } else {
                session.getBasicRemote().sendText(gson.toJson(new ErrorResponse("No cache found for the request.")));
            }
        } else if (command.getCommand().equals("stop")) {
            runSessionMap.get(session.getId()).processCommand(command);
        } else {
            session.getBasicRemote().sendText(gson.toJson(new ErrorResponse("Unsupported command")));
        }
    }

    @OnClose
    public void onClose(CloseReason closeReason, Session session) {
        runSessionMap.get(session.getId()).terminate();
        runSessionMap.remove(session.getId());
    }

    @OnError
    public void onError(Throwable throwable, Session session) {
        logger.error("Error occurred in launcher socket." , throwable);
        ErrorResponse errorResponse = new ErrorResponse("Error occurred in remote server. Error: "
                + throwable.getMessage());
        try {
            session.getBasicRemote().sendText(gson.toJson(errorResponse));
        } catch (IOException e) {
            logger.error("Error while sending back error details" , e);
        }
    }
}
