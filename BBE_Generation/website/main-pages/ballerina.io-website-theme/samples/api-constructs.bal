import ballerina/http;

// Create a simple hello world service that accepts name
// as a POST payload
@http:ServiceConfig {
   basePath: "/"
}
service hello on new http:Listener(9090) {

   // Define a REST resource within the API
   @http:ResourceConfig {
       path: "/",
       methods: ["POST"]
   }
   // Parameters include a reference to the caller
   // and the request data
   resource function hi(http:Caller caller, http:Request request) returns error? {
       // Create an empty response
       http:Response res = new;
       // Try to retrieve parameters
       var payload = request.getTextPayload();

       // Different handling depending on if we got proper string
       // or error
       if (payload is string) {
           res.setPayload("Hello " + untaint payload + "!\n");
       } else {
           res.setPayload(untaint <string>payload.detail().message);
       }

       // Return response, '->' signifies remote call
       check caller->respond(res);
   }
}
