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

import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.Charset;

/**
 * Utils to work with spawned processes
 */
public class ProcessUtils {

    private static final Logger logger = LoggerFactory.getLogger(ProcessUtils.class);

    /**
     * kill process found by given search command
     */
    public static void terminate(String[] findProcessCommand, Runnable next) {
        BufferedReader reader = null;
        try {
            Process findProcess = Runtime.getRuntime().exec(findProcessCommand);
            findProcess.waitFor();
            reader = new BufferedReader(new InputStreamReader(findProcess.getInputStream(), Charset.defaultCharset()));

            String line;
            while ((line = reader.readLine()) != null) {
                try {
                    int processID = Integer.parseInt(line);
                    killChildProcesses(processID);
                    kill(processID);
                    next.run();
                } catch (Throwable e) {
                    logger.error("Unable to kill process " + line + ".");
                }
            }
        } catch (Throwable e) {
            logger.error("Unable to find the process ID for " + findProcessCommand + ".");
        } finally {
            if (reader != null) {
                IOUtils.closeQuietly(reader);
            }
        }
    }

    /**
     * Kill process with given PID
     *
     * @param pid - process id
     */
    private static void kill(int pid) {
        if (pid < 0) {
            return;
        }
        String killCommand = String.format("kill -9 %d", pid);
        try {
            Process kill = Runtime.getRuntime().exec(killCommand);
            kill.waitFor();
        } catch (Throwable e) {
            logger.error("Unable to terminate process:" + pid + ".");
        }
    }

    /**
     * Terminate running all child processes for a given pid.
     *
     * @param pid - process id
     */
    private static void killChildProcesses(int pid) {
        BufferedReader reader = null;
        try {
            Process findChildProcess = Runtime.getRuntime().exec(String.format("pgrep -P %d", pid));
            findChildProcess.waitFor();
            reader = new BufferedReader(new InputStreamReader(findChildProcess.getInputStream(),
                    Charset.defaultCharset()));
            String line;
            int childProcessID;
            while ((line = reader.readLine()) != null) {
                childProcessID = Integer.parseInt(line);
                kill(childProcessID);
            }
        } catch (Throwable e) {
            logger.error("Unable to find parent for process:" + pid + ".");
        } finally {
            if (reader != null) {
                IOUtils.closeQuietly(reader);
            }
        }
    }
}
