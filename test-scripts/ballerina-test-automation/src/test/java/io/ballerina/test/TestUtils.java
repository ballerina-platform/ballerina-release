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

import java.io.File;
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

    public static void testDistCommands(Executor executor, String version, String specVersion, String toolVersion,
                                        String previousVersion, String previousSpecVersion,
                                        String previousVersionsLatestPatch) {
        //Test installation
        TestUtils.testInstallation(executor, version, specVersion, toolVersion);

        //Test `ballerina dist list`
        String actualOutput = executor.executeCommand("ballerina dist list", false);
        System.out.println(actualOutput);
        Assert.assertTrue(actualOutput.contains("1.0.0"));
        Assert.assertTrue(actualOutput.contains("1.1.0"));
        Assert.assertTrue(actualOutput.contains("1.2.0"));
        Assert.assertTrue(actualOutput.contains("slp1"));

        //Test `ballerina dist pull`
        String s = executor.executeCommand("ballerina dist pull "
                + TestUtils.getSupportedVersion(toolVersion, previousVersion), true);
        System.out.println(s);
        TestUtils.testInstallation(executor, previousVersion, previousSpecVersion, toolVersion);

        //Test Update notification message
        if (isSupportedRelease(previousVersion)) {
            //TODO : This is a bug and have fixed in the update tool. Need to update here once new version is released.
            String expectedOutput = "A new version of Ballerina is available: jballerina-" + previousVersionsLatestPatch
                    + "\nUse 'ballerina dist pull jballerina-" + previousVersionsLatestPatch
                    + "' to download and use the distribution\n\n";
            //  Assert.assertEquals(executor.executeCommand("ballerina build help", false), expectedOutput);
        }

        //Test `ballerina dist use`
        executor.executeCommand("ballerina dist use " + TestUtils.getSupportedVersion(toolVersion, version), true);

        //Verify the the installation
        TestUtils.testInstallation(executor, version, specVersion, toolVersion);

        //Test `ballerina dist update`
        executor.executeCommand("ballerina dist use " + TestUtils.getSupportedVersion(toolVersion, previousVersion),
                true);
        executor.executeCommand("ballerina dist remove " + TestUtils.getSupportedVersion(toolVersion, version), true);


        //TODO: Temporary attempt
        executor.executeCommand("ballerina update", true);
        toolVersion = "0.8.10";

        executor.executeCommand("ballerina dist update", true);
        TestUtils.testInstallation(executor, previousVersionsLatestPatch, specVersion, toolVersion);

        //Try `ballerina dist remove`
        executor.executeCommand("ballerina dist remove " + TestUtils.getSupportedVersion(toolVersion, previousVersion),
                true);
    }

    /**
     * Execute smoke testing to verify fetching dependencies.
     *
     * @param executor    Executor for relevant operating system
     * @param version     Installed jBallerina version
     * @param specVersion Installed language specification
     * @param toolVersion Installed tool version
     */
    public static void testDependencyFetch(Executor executor, String version, String specVersion, String toolVersion) {
        //Test installation
        TestUtils.testInstallation(executor, version, specVersion, toolVersion);
        String actualOutput = executor.executeCommand("ballerina dist list", false);
        System.out.println(actualOutput);

        //Test `ballerina dist pull`
        String output = executor.executeCommand("ballerina dist pull 1.2.11", true);
        System.out.println(output);
        Assert.assertTrue(output.contains("Downloading 1.2.11"));
        Assert.assertTrue(output.contains("Fetching the dependencies for '1.2.11' from the remote server..."));
        Assert.assertTrue(output.contains("Downloading jdk8u265-b01-jre"));
        Assert.assertTrue(output.contains("'slp1' successfully set as the active distribution"));
        TestUtils.testInstallation(executor, "1.2.11", "2020R1", toolVersion);


        Path userDir = Paths.get(System.getProperty("user.dir"));
        System.out.println(executor.executeCommand("ballerina new project1 && cd project1 && ballerina add module1 && ballerina build module1", false));
        Path projectPath = userDir.resolve("project1");
        System.out.println(Files.exists(projectPath));
        Assert.assertTrue(Files.isDirectory(projectPath));
        System.out.println(Paths.get(System.getProperty("user.dir")).toString());
        Path modulepath = projectPath.resolve("src").resolve("module1");
        System.out.println(modulepath.toString());
        System.out.println(Files.isDirectory(modulepath));
        Assert.assertTrue(Files.isDirectory(modulepath));
        Assert.assertTrue(Files.exists(projectPath.resolve("target/bin/module1.jar")));

        output = executor.executeCommand("ballerina dist pull " + version, true);
        System.out.println(output);
        Assert.assertTrue(output.contains("Downloading slp7"));
        Assert.assertTrue(output.contains("Fetching the dependencies for 'slp7' from the remote server..."));
        Assert.assertTrue(output.contains("Downloading jdk-11.0.8+10-jre"));
        Assert.assertTrue(output.contains("'slp7' successfully set as the active distribution"));
        TestUtils.testInstallation(executor, version, specVersion, toolVersion);
        System.out.println(executor.executeCommand("ballerina new project2 && cd project2 && ballerina add module1 && ballerina build", false));
        projectPath = userDir.resolve("project2");
        System.out.println(Files.exists(projectPath));
        Assert.assertTrue(Files.exists(projectPath));
        modulepath = projectPath.resolve("modules").resolve("module1");
        System.out.println(Files.exists(modulepath));
        Assert.assertTrue(Files.isDirectory(modulepath));
        System.out.println(executor.executeCommand("ballerina build", false));
        Assert.assertTrue(Files.exists(projectPath.resolve("target/bin/project2.jar")));
        //Test `ballerina dist list`
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
        Assert.assertEquals(executor.executeCommand("ballerina -v", true),
                TestUtils.getVersionOutput(version, specVersion, toolVersion));
    }

    /**
     * Execute smoke testing to verify installation.
     *
     * @param executor    Executor for relevant operating system
     */
    public static void verifyDistList(Executor executor) {
        String actualOutput = executor.executeCommand("ballerina dist list", false);
        System.out.println(actualOutput);
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
    public static void testProject(Executor executor) {
        executor.executeCommand("ballerina new project1 && cd project1 && ballerina add module1", false);
        Path userDir = Paths.get(System.getProperty("user.dir"));
        Path projectPath = userDir.resolve("project2");
        System.out.println(Files.exists(projectPath));
        Assert.assertTrue(Files.exists(projectPath));
        System.out.println(Files.exists(projectPath.resolve("modules").resolve("module1")));
        Assert.assertTrue(Files.isDirectory(projectPath.resolve("modules").resolve("module1")));
        Assert.assertTrue(Files.exists(projectPath.resolve("target/bin/project2.jar")));
    }

    private static String getSupportedVersion(String toolVersion, String version) {
        if (TestUtils.isOldToolVersion(toolVersion)) {
            return "jballerina-" + version;
        }
        if (version.contains(TestUtils.SWAN_LAKE_KEYWORD)) {
            return "slp" + version.replace("swan-lake-preview", "");
        }
        return version;
    }
}
