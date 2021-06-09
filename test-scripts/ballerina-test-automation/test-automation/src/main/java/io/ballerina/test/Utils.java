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

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.sql.Timestamp;
import java.util.Locale;

public class Utils {
    private static final String OS = System.getProperty("os.name").toLowerCase(Locale.getDefault());
    public static final boolean BALLERINA_STAGING_UPDATE = Boolean.parseBoolean(
            System.getenv("BALLERINA_STAGING_UPDATE"));

    private static TrustManager[] trustAllCerts = new TrustManager[]{
            new X509TrustManager() {
                public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                    return null;
                }

                public void checkClientTrusted(java.security.cert.X509Certificate[] certs, String authType) {
                    //No need to implement.
                }

                public void checkServerTrusted(java.security.cert.X509Certificate[] certs, String authType) {
                    //No need to implement.
                }
            }
    };

    public static final String DISTRIBUTION_LOCATION ="http://dist-dev.ballerina.io/downloads/";

    public static void downloadFile(String version, String installerName) {
        try {
            String destination = getUserHome();
            File output = new File(destination + File.separator + installerName);
            if (!output.exists()) {
                SSLContext sc = SSLContext.getInstance("SSL");
                sc.init(null, trustAllCerts, new java.security.SecureRandom());
                HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());

                HttpURLConnection conn = (HttpURLConnection) new URL(
                        DISTRIBUTION_LOCATION + version + "/" + installerName).openConnection();
                conn.setRequestProperty("content-type", "binary/data");

                try (InputStream in = conn.getInputStream();
                     FileOutputStream out = new FileOutputStream(output)) {
                    byte[] b = new byte[1024];
                    int count;
                    while ((count = in.read(b)) > 0) {
                        out.write(b, 0, count);
                    }
                } catch (IOException e) {
                    System.out.print(e);
                }
            }
        } catch (Exception e) {
            System.out.print(e);
        }
    }

    public static String executeWindowsCommand(String command) {
        String output = "";
        try {
            ProcessBuilder pb = new ProcessBuilder("cmd.exe", "/c", command);
            if (BALLERINA_STAGING_UPDATE) {
                pb.environment().put("BALLERINA_STAGING_UPDATE", "true");
            }
            Process p = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                output += line + "\n";
            }
        } catch (Exception e) {
            System.out.print("Error occurred");
        }
        return output;
    }


    public static String executeCommand(String command) {
        String output = "";
        try {
            File file = new File(getUserHome() + File.separator
                    + "temp-" + new Timestamp(System.currentTimeMillis()).getTime() + ".sh");
            file.createNewFile();
            file.setExecutable(true);
            PrintWriter writer = new PrintWriter(file.getPath(), "UTF-8");
            writer.println(command);
            writer.close();

            ProcessBuilder pb = new ProcessBuilder(file.getPath());
            Process process = pb.start();
            InputStream inputStream = process.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
            String line;
            while ((line = reader.readLine()) != null) {
                output += line + "\n";
            }
            if (output.isEmpty()) {
                inputStream =  process.getErrorStream();
                reader = new BufferedReader(new InputStreamReader(inputStream));
                while ((line = reader.readLine()) != null) {
                    output += line + "\n";
                }
            }
            file.delete();
        } catch (Exception e) {
            System.out.print("Error occurred");
        }
        return output;
    }

    private static boolean isUnix() {
        return OS.contains("nix") || OS.contains("nux") || OS.contains("aix");
    }

    /**
     * Provide user home directory based on command.
     *
     * @return user home directory
     */
    public static String getUserHome() {
        String userHome = System.getenv("HOME");
        if (isUnix() && userHome.contains("root")) {
            userHome = "/home/" + System.getenv("SUDO_USER");
        }
        if (userHome == null) {
            userHome = System.getProperty("user.home");
        }
        return userHome;
    }

    /**
     * Get the command name(ballerina or bal)
     *
     * @param toolVersion
     * @return returns the command name
     */
    public static String getCommandName(String toolVersion) {
        String[] version = toolVersion.split("\\.");
        //command will be ballerina if update tool version is less than 0.8.10.
        return version[0].equals("0") && Integer.parseInt(version[2]) <= 10 ? "ballerina " : "bal ";
    }
}
