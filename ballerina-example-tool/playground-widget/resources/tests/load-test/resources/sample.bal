import ballerina/http;
import ballerina/io;

// Listener endpoint that a service binds to
endpoint http:Listener listener {
  port:9090
};

// Annotations decorate code.
// Change the service URL base to '/greeting'.
@http:ServiceConfig {
    basePath:"/greeting"
}
service<http:Service> greeting bind listener {

  // Decorate the 'greet' resource to accept POST requests.
  @http:ResourceConfig{
    path: "/",
    methods: ["POST"]
  }
  greet (endpoint caller, http:Request request) {
    http:Response response = new;

    // Check statement matches the output type of the
    // getStringPayload method to a string. If not it
    // throws an error.
    string reqPayload = check request.getTextPayload();
    response.setTextPayload("Hello, " + reqPayload + "!\n CACHE_CONTROL_PLACEHOLDER" );
    _ = caller -> respond(response);
  }
}
