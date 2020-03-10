package org.ballerinalang.platform.playground.utils.model;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class LauncherResponse implements Serializable {

    @SerializedName("launcher-url")
    private String launcherUrl;

    @SerializedName("cache-id")
    private String cacheId;

    public LauncherResponse(String launcherUrl, String cacheId) {
        this.launcherUrl = launcherUrl;
        this.cacheId = cacheId;
    }

    public LauncherResponse(String launcherUrl) {
        this.launcherUrl = launcherUrl;
        this.cacheId = "";
    }

    public LauncherResponse() {
        this.launcherUrl = "";
        this.cacheId = "";
    }

    public String getLauncherUrl() {
        return launcherUrl;
    }

    public void setLauncherUrl(String launcherUrl) {
        this.launcherUrl = launcherUrl;
    }

    public String getCacheId() {
        return cacheId;
    }

    public void setCacheId(String cacheId) {
        this.cacheId = cacheId;
    }
}
