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
import org.ballerinalang.platform.playground.launcher.core.Constants;
import org.ballerinalang.platform.playground.launcher.core.RunSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.time.Duration;
import java.time.Instant;

/**
 * TryIt Phase of Run
 */
public class TryItPhase implements Phase {

    private static final Logger logger = LoggerFactory.getLogger(StartPhase.class);

    private volatile int currentCurlExec = 0;

    private volatile boolean terminate = false;

    private Instant curlStart;

    public synchronized void incrementCurlExecCount() {
        currentCurlExec++;
    }

    public synchronized int getCurrentCurlExec() {
        return currentCurlExec;
    }

    @Override
    public void execute(RunSession session, Runnable next) {
        (new Thread(() -> {
            curlStart = Instant.now();
            session.pushMessageToClient(Constants.CONTROL_MSG, Constants.CURL_EXEC_STARTED,
                    "executing curl...");
            for (int i = 0; i < session.getRunCommand().getNoOfCurlExecutions(); i++) {
                if (terminate) {
                    break;
                }
                try {
                    executeCURL(session, next);
                    Thread.sleep(Constants.CURL_RETRY_DELAY);
                } catch (InterruptedException | IOException e) {
                    logger.error("Error while executing the curl.");
                }

            }
        })).start();
    }

    private void executeCURL(RunSession session, Runnable next) throws IOException {
        String curl = session.getRunCommand().getCurl() != null
                ? session.getRunCommand().getCurl()
                    .replace("playground.localhost",
                        session.getServiceHost() + ":" + session.getServicePort())
                : null;
        String[] cmdArray = curl.split("(\\s)+");
        if (cmdArray.length > 0 && !cmdArray[0].equals("curl")) {
            session.pushMessageToClient(Constants.DATA_MSG, Constants.OUTPUT,
                    "only curl cmd is supported");
            return;
        }
        Process curlProcess = Runtime.getRuntime().exec(cmdArray, new String[0]);

        new Thread(() -> {
            BufferedReader reader = null;
            try {
                reader = new BufferedReader(new InputStreamReader(curlProcess.getInputStream(), Charset
                        .defaultCharset()));
                String line = "";
                while ((line = reader.readLine()) != null) {
                    session.pushMessageToClient(Constants.DATA_MSG, Constants.OUTPUT,
                            "CURL-OUTPUT:" + line);
                }
                incrementCurlExecCount();
                if (getCurrentCurlExec() == session.getRunCommand().getNoOfCurlExecutions()) {
                    Instant curlStop = Instant.now();
                    Duration executionTime = Duration.between(curlStart, curlStop);
                    session.pushMessageToClient(Constants.CONTROL_MSG, Constants.CURL_EXEC_STOPPED,
                            "executing curl completed in " + executionTime.toMillis() + "ms");

                    if (session.getRunCommand().getPostCurlDelay() > 0) {
                        Thread.sleep(session.getRunCommand().getPostCurlDelay());
                    }
                    next.run();
                }

            } catch (Exception e) {
                logger.error("Error while sending curl output stream.", e);
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
                        curlProcess.getErrorStream(), Charset.defaultCharset()));
                String line = "";
                while ((line = reader.readLine()) != null) {
                    session.pushMessageToClient(Constants.ERROR_MSG, Constants.OUTPUT, line);
                }
            } catch (IOException e) {
                logger.error("Error while sending curl error stream.", e);
            } finally {
                if (reader != null) {
                    IOUtils.closeQuietly(reader);
                }
            }
        }).start();
    }


    /**
     * Terminate curl process
     */
    public void terminate(RunSession runSession) {
        terminate = true;
    }

}
