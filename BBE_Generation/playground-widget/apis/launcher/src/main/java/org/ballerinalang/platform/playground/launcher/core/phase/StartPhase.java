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
package org.ballerinalang.platform.playground.launcher.core.phase;

import org.apache.commons.io.IOUtils;
import org.apache.commons.lang.StringUtils;
import org.ballerinalang.platform.playground.launcher.core.Constants;
import org.ballerinalang.platform.playground.launcher.core.util.ProcessUtils;
import org.ballerinalang.platform.playground.launcher.core.RunSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import java.util.stream.Stream;

/**
 * Start Phase of Run
 */
public class StartPhase implements Phase {

    private static final String BPG_ENV_PREFIX = "BPG_ENV_";

    private static final String JAVA_HOME = "JAVA_HOME";

    public static final String SERVICE_STARTED_MSG_PREFIX = "[ballerina/http] started HTTP/WS endpoint";

    private static final Logger logger = LoggerFactory.getLogger(StartPhase.class);

    /**
     * Construct the command array to be executed.
     * @return String[] command array
     */
    private String[] getRunCommandArray(RunSession session) throws IOException {
        List<String> commandList = new ArrayList<>();
        // path to ballerina
        commandList.add("ballerina");
        commandList.add("run");
        commandList.add(session.getBuildFile().toAbsolutePath().toString());
        return commandList.toArray(new String[0]);
    }
    
    @Override
    public void execute(RunSession runSession, Runnable next) throws Exception{
        String[] cmdArray = getRunCommandArray(runSession);
        Process launchProcess = Runtime.getRuntime().exec(cmdArray, getEnvVars(),
                runSession.getBuildFile().getParent().toFile());

        // kill the program process after specified timeout
        new Timer().schedule(new TimerTask() {
            @Override
            public void run() {
                if (launchProcess != null && launchProcess.isAlive()) {
                    terminate(runSession);
                    runSession.pushMessageToClient(Constants.CONTROL_MSG, Constants.OUTPUT
                            , "program timed-out in " + Constants.PROGRAM_TIMEOUT + "ms");
                }
            }
        }, Constants.PROGRAM_TIMEOUT);

        runSession.pushMessageToClient(Constants.CONTROL_MSG, Constants.EXECUTION_STARTED,
                "running program");

        new Thread(() -> {
            BufferedReader reader = null;
            try {
                reader = new BufferedReader(new InputStreamReader(launchProcess.getInputStream(), Charset
                        .defaultCharset()));
                String line = "";
                while ((line = reader.readLine()) != null) {
                    if (line.startsWith("ballerina: initiating service(s) in")
                            || line.startsWith("ballerina: deploying service(s) in")
                            || line.startsWith("Initiating service(s)")) {
                        continue;
                    } else if (line.startsWith(SERVICE_STARTED_MSG_PREFIX)) {
                        updateHostAndPort(runSession, line);
                        String serviceURL = "http://playground.localhost/";
                        runSession.pushMessageToClient(Constants.DATA_MSG, Constants.OUTPUT,
                                "started service at " + serviceURL);
                        next.run();
                    } else {
                        runSession.pushMessageToClient(Constants.DATA_MSG, Constants.OUTPUT,
                                "BVM-OUTPUT:" + line);
                    }
                }
                runSession.pushMessageToClient(Constants.CONTROL_MSG, Constants.EXECUTION_STOPPED,
                        "running program completed");
            } catch (IOException e) {
                logger.error("Error while sending run output stream.");
            } finally {
                if (reader != null) {
                    IOUtils.closeQuietly(reader);
                }
            }
        }).start();

        new Thread(() -> {
            BufferedReader reader = null;
            try {
                reader = new BufferedReader(new InputStreamReader(
                        launchProcess.getErrorStream(), Charset.defaultCharset()));
                String line = "";
                while ((line = reader.readLine()) != null) {
                    runSession.pushMessageToClient(Constants.DATA_MSG, Constants.ERROR, "BVM-OUTPUT:" + line);
                }
            } catch (IOException e) {
                logger.error("Error while sending build error stream.", e);
            } finally {
                if (reader != null) {
                    IOUtils.closeQuietly(reader);
                }
            }
        }).start();
    }

    /**
     * Terminate running ballerina program.
     */
    public void terminate(RunSession runSession) {
        String balFile = runSession.useBuildCache()
                ? runSession.getBuildFileFromCache().toString()
                : runSession.getBuildFile().toString();
        String[] searchCmd = {
                "/bin/sh",
                "-c",
                "ps -ef -o pid,args | grep " +
                        balFile + " | grep run | grep ballerina | grep -v 'grep " +
                        balFile + "' | awk '{print $1}'"
        };
        ProcessUtils.terminate(searchCmd, () -> {
            runSession.pushMessageToClient(Constants.CONTROL_MSG, Constants.PROGRAM_TERMINATED,
                    "program terminated");
        });
    }

    /**
     * Gets the host and port of the from console log
     *
     * @param line The log line.
     */
    private void updateHostAndPort(RunSession runSession, String line) {
        String hostPort = StringUtils.substringAfterLast(line,
                SERVICE_STARTED_MSG_PREFIX).trim();
        String host = StringUtils.substringBeforeLast(hostPort, ":");
        String port = StringUtils.substringAfterLast(hostPort, ":");
        if (StringUtils.isNotBlank(host)) {
            runSession.setServiceHost(host);
        }
        if (StringUtils.isNotBlank(port)) {
            runSession.setServicePort(port);
        }
    }

    private String[] getEnvVars() {
        return System.getenv()
                .entrySet()
                .stream()
                .filter(envEntry -> envEntry.getKey().startsWith(BPG_ENV_PREFIX)
                        || envEntry.getKey().equals(JAVA_HOME))
                .map(envEntry -> envEntry.getKey().replaceAll(BPG_ENV_PREFIX, "") +
                        "=" + envEntry.getValue())
                .toArray(String[]::new);
    }
}
