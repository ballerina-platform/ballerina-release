package org.ballerinalang.platform.playground.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class EnvUtils {

    private static final Logger log = LoggerFactory.getLogger(EnvUtils.class);

    /**
     * Read environment variable. If no value is found, null is returned.
     *
     * @param key
     * @return
     */
    public static String getEnvStringValue(String key) {
        return getEnvStringValue(key, false);
    }

    /**
     * Read environment variable. If no value is found, the provided default value is returned.
     *
     * @param key
     * @param defaultValue
     * @return
     */
    public static String getEnvStringValue(String key, String defaultValue) {
        try {
            return getEnvStringValue(key, true);
        } catch (IllegalArgumentException ex) {
            log.debug("Environment variable " + key + " not found. Using default value " + defaultValue);
            return defaultValue;
        }
    }

    /**
     * Read environment variable. If no value is found, the provided default value is returned.
     *
     * @param key
     * @param defaultValue
     * @return
     */
    public static boolean getEnvBooleanValue(String key, boolean defaultValue) {
        try {
            return getEnvBoolean(key, true);
        } catch (IllegalArgumentException ex) {
            log.debug("Environment variable " + key + " not found. Using default value " + defaultValue);
            return defaultValue;
        }
    }

    /**
     * Read environment variable. If no value is found an {@link IllegalArgumentException} is thrown.
     *
     * @param key
     * @return
     */
    public static String getRequiredEnvStringValue(String key) {
        return getEnvStringValue(key, true);
    }

    /**
     * Read environment variable and return the parsed integer value. If no value is found, 0 is returned.
     *
     * @param key
     * @return
     */
    public static int getEnvIntValue(String key) {
        return getEnvIntValue(key, false);
    }

    /**
     * Read environment variable and return the parsed integer value. If no value is found, the provided default
     * value is returned.
     *
     * @param key
     * @param defaultValue
     * @return
     */
    public static int getEnvIntValue(String key, int defaultValue) {
        try {
            return getEnvIntValue(key, true);
        } catch (IllegalArgumentException ex) {
            log.debug("Environment variable " + key + " not found or invalid value passed. Using default value " + defaultValue);
            return defaultValue;
        }
    }

    /**
     * Read environment variable and return the parse integer value. If no value is found or the read value cannot be
     * parse as a valid integer value, an {@link IllegalArgumentException} is thrown.
     *
     * @param key
     * @return
     */
    public static int getRequiredEnvIntValue(String key) {
        return getEnvIntValue(key, true);
    }

    /**
     * Read environment variable. If no value is found and if {@param required} is true,
     * an {@link IllegalArgumentException} is thrown.
     *
     * @param key
     * @param required
     * @return
     */
    private static String getEnvStringValue(String key, boolean required) {
        if (key != null) {
            String readValue = System.getenv(key);

            if (readValue == null && required) {
                throw new IllegalArgumentException("Missing required environment variable: " + key);
            } else if (readValue == null) {
                log.debug("No value found for environment variable " + key);
            }

            return readValue;

        } else {
            throw new IllegalStateException("Null key provided to lookup environment variable");
        }
    }

    /**
     * Read environment variable and return the parsed integer value. If {@param required} is true, when no value is
     * found, or the read value cannot be properly parsed as an integer, an {@link IllegalArgumentException} is thrown.
     * If {@param required} is false 0 returned for no value or invalid value scenarios.
     *
     * @param key
     * @param required
     * @return
     */
    private static int getEnvIntValue(String key, boolean required) {
        String rawValue = getEnvStringValue(key, required);
        if (rawValue != null) {
            try {
                return Integer.parseInt(rawValue);
            } catch (NumberFormatException e) {
                if (required) {
                    throw new IllegalArgumentException("Couldn't parse value set for environment variable " + key, e);
                }

                log.warn("Couldn't parse value set for environment variable " + key);
                return 0;
            }
        } else {
            log.warn("No value found for environment variable " + key);
            return 0;
        }
    }

    /**
     * Read environment variable and return the parsed boolean value. If {@param required} is true, when no value is
     * found, or the read value cannot be properly parsed as an boolean, an {@link IllegalArgumentException} is thrown.
     * If {@param required} is false, false is returned for no value or invalid value scenarios.
     *
     * @param key
     * @param required
     * @return
     */
    private static boolean getEnvBoolean(String key, boolean required) {
        String rawValue = getEnvStringValue(key, required);
        if (rawValue != null) {
            try {
                return Boolean.parseBoolean(rawValue);
            } catch (Exception e) {
                if (required) {
                    throw new IllegalArgumentException("Couldn't parse value set for environment variable " + key, e);
                }

                log.warn("Couldn't parse value set for environment variable " + key);
                return false;
            }
        } else {
            log.warn("No value found for environment variable " + key);
            return false;
        }
    }
}
