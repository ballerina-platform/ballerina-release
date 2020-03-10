import ballerina/config;
import ballerina/http;
import wso2/twitter;

listener http:Listener tweeter = new(9090, config = {
    keepAlive: http:KEEPALIVE_ALWAYS,
    timeoutMillis: 12000
});

twitter:Client twitterClient = new({
    clientId: config:getAsString("consumer_id"),
    clientSecret: config:getAsString("consumer_secret"),
    accessToken: config:getAsString("access_token"),
    accessTokenSecret: config:getAsString("access_token_secret")
});

service passthrough on tweeter {

    @http:ResourceConfig {
        path: "/"
    }
    resource function passthrough(http:Caller caller, http:Request req)
                                    returns error? {
        twitter:Status twitterStatus = check twitterClient->tweet(
                                            "Hello", "", "");
        _ = caller->respond("Tweet ID: " + <string> twitterStatus.id 
                 + ", Tweet: " + twitterStatus.text);
        return;
    }
}