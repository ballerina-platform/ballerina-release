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
package org.ballerinalang.platform.playground.launcher.core;

/**
 * Run API Constants
 */
public class Constants {

    public static final String BALLERINA_HOME = "ballerina.home";

    // message types
    public static final String INFO_MSG = "INFO_MSG";
    public static final String ERROR_MSG  = "ERROR_MSG";
    public static final String DATA_MSG  = "DATA_MSG";
    public static final String CONTROL_MSG  = "CONTROL_MSG";

    // control msg codes
    public static final String BUILD_STARTED = "BUILD_STARTED";
    public static final String CURL_EXEC_STARTED = "CURL_EXEC_STARTED";
    public static final String CURL_EXEC_STOPPED = "CURL_EXEC_STOPPED";
    public static final String BUILD_ERROR = "BUILD_ERROR";
    public static final String BUILD_STOPPED = "BUILD_STOPPED";
    public static final String BUILD_STOPPED_WITH_ERRORS = "BUILD_STOPPED_WITH_ERRORS";
    public static final String EXECUTION_STARTED = "EXECUTION_STARTED";
    public static final String EXECUTION_STOPPED = "EXECUTION_STOPPED";
    public static final String DEP_SERVICE_EXECUTION_STARTED = "DEP_SERVICE_EXECUTION_STARTED";
    public static final String DEP_SERVICE_EXECUTION_ERROR = "DEP_SERVICE_EXECUTION_ERROR";
    public static final String DEP_SERVICE_EXECUTION_STOPPED = "DEP_SERVICE_EXECUTION_STOPPED";
    public static final String PROGRAM_TERMINATED = "PROGRAM_TERMINATED";
    public static final String RUN_ABORTED = "RUN_ABORTED";

    // other msg codes
    public static final String INFO = "INFO";
    public static final String ERROR  = "ERROR";
    public static final String OUTPUT = "OUTPUT";

    // run timeout
    public static final int PROGRAM_TIMEOUT = 15000;

    // curl retry delay
    public static final int CURL_RETRY_DELAY = 1000;
}
