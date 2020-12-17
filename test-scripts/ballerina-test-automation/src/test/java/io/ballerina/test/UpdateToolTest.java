/*
 * Copyright (c) 2020, WSO2 Inc. (http://wso2.com) All Rights Reserved.
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

package io.ballerina.test;

import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class UpdateToolTest {
    String version = System.getProperty("BALLERINA_VERSION");
    String specVersion = System.getProperty("SPEC_VERSION");
    String toolVersion = System.getProperty("TOOL_VERSION");
    String latestVersion = System.getProperty("LATEST_BALLERINA_VERSION");
    String latestSpecVersion = System.getProperty("LATEST_SPEC_VERSION");
    String latestToolVersion = System.getProperty("LATEST_TOOL_VERSION");

    String previousVersion = System.getProperty("PREVIOUS_BALLERINA_VERSION");
    String previousSpecVersion = System.getProperty("PREVIOUS_SPEC_VERSION");
    String previousVersionsLatestPatch = System.getProperty("PREVIOUS_VERSIONS_LATEST_PATCH");
    String previousVersionsLatestSpec = System.getProperty("PREVIOUS_VERSIONS_LATEST_ SPEC");

    @DataProvider(name = "getExecutors")
    public Object[][] dataProviderMethod() {
        Executor[][] result = new Executor[1][1];
        result[0][0] = TestUtils.getExecutor(version);
        return result;
    }

    @Test(dataProvider = "getExecutors")
    public void testUpdateTool(Executor executor) {
        executor.transferArtifacts();
        executor.install();

        //Test dist list
        TestUtils.verifyDistList(executor);
        //Test installation
        TestUtils.testInstallation(executor, version, specVersion, toolVersion);

        //Test `ballerina update`
        executor.executeCommand("ballerina update", true);
        TestUtils.testInstallation(executor, version, specVersion, latestToolVersion);

        //Execute all ballerina dist commands once updated
        TestUtils.testDistCommands(executor, latestVersion, latestSpecVersion, latestToolVersion, previousVersion,
                previousSpecVersion, previousVersionsLatestPatch);

        executor.uninstall();
        executor.cleanArtifacts();
    }
}
