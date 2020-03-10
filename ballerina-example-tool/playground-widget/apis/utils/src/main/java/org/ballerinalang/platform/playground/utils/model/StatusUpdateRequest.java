package org.ballerinalang.platform.playground.utils.model;

import com.google.gson.annotations.SerializedName;

public class StatusUpdateRequest {

    @SerializedName("status")
    private String status;

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
