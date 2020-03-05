import ballerina/http;
import ballerina/openapi;
import ballerinax/kubernetes;

// Generate Docker image and Kubernetes deployment artifacts
// for that service to be started with kubectl apply -f
@kubernetes:Deployment {
   image: "demo/ballerina-demo",
   name: "ballerina-demo"
}

// Generate openapi definition with: ballerina openapi export demo.bal
@openapi:ServiceInfo {
   title: "Hello World Service",
   serviceVersion: "2.0.0",
   description: "Simple hello world service"
}

// Change the service context
@http:ServiceConfig {
   basePath: "/"
}
service hello on new http:Listener(9090) {

   // Change the resource path and accepted verbs
   @http:ResourceConfig {
       path: "/",
       methods: ["GET"]
   }
   resource function hi(http:Caller caller, http:Request request) returns error? {
       http:Response res = new;
       res.setPayload("Hello World!\n");

       check caller->respond(res);
   }

}
