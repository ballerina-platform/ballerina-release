import ballerina/http;
import ballerina/log;

http:Client backendEP = new("http://localhost:8080", config = {
   circuitBreaker: {
       failureThreshold: 0.2,
       statusCodes: [400, 404, 500]
   },
   timeoutMillis: 2000,
   retryConfig: {
       backOffFactor: 2,
       count: 3,
       interval: 1000
   }
});

service legacyEndpoint on new http:Listener(9090) {

   @http:ResourceConfig {
       path: "/"
   }
   resource function invokeEndpoint(http:Caller caller,
                           http:Request request) returns error? {
       http:Response backendRes = check backendEP->forward("/hello",
                                                           request);
       check caller->respond(backendRes);
   }
}
