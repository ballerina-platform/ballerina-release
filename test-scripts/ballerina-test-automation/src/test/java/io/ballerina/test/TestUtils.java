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


import org.testng.Assert;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Locale;

public class TestUtils {
    private static final String OS = System.getProperty("os.name").toLowerCase(Locale.getDefault());
    private static final String SWAN_LAKE_KEYWORD = "swan-lake";


    public static String getVersionOutput(String jBallerinaVersion, String specVersion, String toolVersion) {
        String toolText = TestUtils.isOldToolVersion(toolVersion) ? "Ballerina tool" : "Update Tool";
        if (jBallerinaVersion.contains(TestUtils.SWAN_LAKE_KEYWORD)) {
            String[] versionParts = jBallerinaVersion.split("-");
            return "Ballerina Swan Lake Preview " + versionParts[versionParts.length - 1].replace("preview", "") + "\n"
                    + "Language specification " + specVersion + "\n" + toolText + " " + toolVersion + "\n";
        }

        String ballerinaReference = isSupportedRelease(jBallerinaVersion) ? "jBallerina" : "Ballerina";
        return ballerinaReference + " " + jBallerinaVersion + "\n" +
                "Language specification " + specVersion + "\n" +
                toolText + " " + toolVersion + "\n";
    }

    public static Executor getExecutor(String version) {
        Executor executor;
        if (OS.contains("win")) {
            executor = new Windows(version);
        } else if (OS.contains("mac")) {
            executor = new MacOS(version);
        } else {
            String provider = System.getenv("OS_TYPE");
            if (provider != null && provider.equalsIgnoreCase("centos")) {
                executor = new CentOS(version);
            } else {
                executor = new Ubuntu(version);
            }
        }
        return executor;
    }

    public static void testDistCommands(Executor executor, String latestVersion, String latestSpecVersion,
                                        String latestToolVersion, String previousVersion, String previousSpecVersion,
                                        String previousVersionsLatestPatch) {

        //Test `ballerina dist list`
        String actualOutput = executor.executeCommand("ballerina dist list", false);
        System.out.println(actualOutput);
        Assert.assertTrue(actualOutput.contains("1.0.0"));
        Assert.assertTrue(actualOutput.contains("1.1.0"));
        Assert.assertTrue(actualOutput.contains("1.2.0"));
        Assert.assertTrue(actualOutput.contains("slp1"));

        //Test `ballerina dist update for swan-lake-release`
        executor.executeCommand("ballerina dist update", true);
        TestUtils.testInstallation(executor, latestVersion, latestSpecVersion, latestToolVersion);

        //Test `ballerina dist pull` 1.2.0
        executor.executeCommand("ballerina dist pull "
                + TestUtils.getSupportedVersion(previousVersion), true);
        TestUtils.testInstallation(executor, previousVersion, previousSpecVersion, latestToolVersion);

        //Test `ballerina dist update for jballerina-release`
        executor.executeCommand("ballerina dist update", true);
        TestUtils.testInstallation(executor, previousVersionsLatestPatch, previousSpecVersion, latestToolVersion);
        //Test Update notification message
        if (isSupportedRelease(previousVersion)) {
            //TODO : This is a bug and have fixed in the update tool. Need to update here once new version is released.
            String expectedOutput = "A new version of Ballerina is available: jballerina-" + previousVersionsLatestPatch
                    + "\nUse 'ballerina dist pull jballerina-" + previousVersionsLatestPatch
                    + "' to download and use the distribution\n\n";
            //  Assert.assertEquals(executor.executeCommand("ballerina build help", false), expectedOutput);
        }

        //Test `ballerina dist use`
        executor.executeCommand("ballerina dist use " + TestUtils.getSupportedVersion(previousVersion), true);

        //Verify the the installation
        TestUtils.testInstallation(executor, previousVersion, previousSpecVersion, latestToolVersion);

        executor.executeCommand("ballerina dist remove " + TestUtils.getSupportedVersion(previousVersionsLatestPatch), true);

        executor.executeCommand("ballerina dist update", true);
        TestUtils.testInstallation(executor, previousVersionsLatestPatch, previousSpecVersion, latestToolVersion);

        //Try `ballerina dist remove`
        executor.executeCommand("ballerina dist remove " + TestUtils.getSupportedVersion(previousVersion),
                true);
    }

    /**
     * Execute smoke testing to verify installation.
     *
     * @param executor    Executor for relevant operating system
     * @param version     Installed jBallerina version
     * @param specVersion Installed language specification
     * @param toolVersion Installed tool version
     */
    public static void testInstallation(Executor executor, String version, String specVersion, String toolVersion) {
        System.out.println(executor.executeCommand("ballerina -v", false));
        Assert.assertEquals(executor.executeCommand("ballerina -v", false),
                TestUtils.getVersionOutput(version, specVersion, toolVersion));
    }

    /**
     * Execute smoke testing to verify fetching dependencies.
     *
     * @param executor    Executor for relevant operating system
     * @param toolVersion Installed tool version
     */
    public static void testDependencyFetch(Executor executor, String toolVersion) {
        executor.executeCommand("ballerina dist list", false);
        //Test `Fetching compatible JRE dependency`
        String output = executor.executeCommand("ballerina dist pull 1.2.10", true);
        System.out.println(output);
        Assert.assertTrue(output.contains("Downloading 1.2.10"));
        Assert.assertTrue(output.contains("Fetching the dependencies for '1.2.10' from the remote server..."));
        Assert.assertTrue(output.contains("Downloading jdk8u202-b08-jre"));
        Assert.assertTrue(output.contains("'slp1' successfully set as the active distribution"));
        TestUtils.testInstallation(executor, "1.2.10", "2020R1", toolVersion);

        Path userDir = Paths.get(System.getProperty("user.dir"));
        executor.executeCommand("ballerina new project1 && cd project1 && ballerina add module1 && " +
                "ballerina build module1", false);
        Path projectPath = userDir.resolve("project1");
        Assert.assertTrue(Files.isDirectory(projectPath));
        Assert.assertTrue(Files.isDirectory(projectPath.resolve("src").resolve("module1")));
        Assert.assertTrue(Files.exists(projectPath.resolve("target/bin/module1.jar")));

        output = executor.executeCommand("ballerina dist pull slp7", true);
        System.out.println(output);
        Assert.assertTrue(output.contains("Downloading slp7"));
        Assert.assertTrue(output.contains("Fetching the dependencies for 'slp7' from the remote server..."));
        Assert.assertTrue(output.contains("Downloading jdk-11.0.8+10-jre"));
        Assert.assertTrue(output.contains("'slp7' successfully set as the active distribution"));
        TestUtils.testInstallation(executor, "swan-lake-preview7", "v2020-09-22", toolVersion);

        executor.executeCommand("ballerina new project2 && cd project2 && ballerina add module1 && " +
                "ballerina build", false);
        projectPath = userDir.resolve("project2");
        Assert.assertTrue(Files.isDirectory(projectPath));
        Assert.assertTrue(Files.isDirectory(projectPath.resolve("modules").resolve("module1")));
        Assert.assertTrue(Files.exists(projectPath.resolve("target/bin/project2.jar")));
    }

    /**
     * Execute smoke testing to verify dist list.
     *
     * @param executor    Executor for relevant operating system
     */
    public static void verifyDistList(Executor executor) {
        String actualOutput = executor.executeCommand("ballerina dist list", false);
        Assert.assertTrue(actualOutput.contains("1.0.0"));
        Assert.assertTrue(actualOutput.contains("1.1.0"));
        Assert.assertTrue(actualOutput.contains("1.2.0"));
    }

    /**
     * To check whether installation is a 1.0.x release.
     *
     * @return returns is a 1.0.x release
     */
    public static boolean isSupportedRelease(String version) {
        if (version.contains(TestUtils.SWAN_LAKE_KEYWORD)) {
            return true;
        }

        String[] versions = version.split("\\.");
        return !(versions[0].equals("1") && versions[1].equals("0"));
    }

    /**
     * To check whether older tool version before swan lake support
     *
     * @param toolVersion
     * @return returns is a older version
     */
    public static boolean isOldToolVersion(String toolVersion) {
        return toolVersion.equals("0.8.5") || toolVersion.equals("0.8.0");
    }

    /**
     * Test project and module creation.
     *
     * @param executor Executor for relevant operating system
     */
    public void testProject(Executor executor) {
        String expectedOutput = "Created new Ballerina project at project1\n" +
                "\n" +
                "Next:\n" +
                "    Move into the project directory and use `ballerina add <module-name>` to\n" +
                "    add a new Ballerina module.\n";
        Assert.assertEquals(executor.executeCommand("ballerina new project1", false), expectedOutput);

        executor.executeCommand("cd project1", false);
        expectedOutput = "Added new ballerina module at 'src/module1'\n";
        Assert.assertEquals(executor.executeCommand("ballerina add module1'", false), expectedOutput);
    }

    private static String getSupportedVersion(String version) {
        if (version.contains("1.")) {
            return "jballerina-" + version;
        }
        if (version.contains(TestUtils.SWAN_LAKE_KEYWORD)) {
            return "slp" + version.replace("swan-lake-preview", "");
        }
        return version;
    }
}
