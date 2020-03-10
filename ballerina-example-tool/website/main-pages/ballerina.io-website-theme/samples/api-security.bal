import ballerina/http;

http:AuthProvider jwtAuthProvider = {
   scheme: http:JWT_AUTH,
   config: {
       issuer:"ballerina",
       audience: ["ballerina.io"],
       certificateAlias: "ballerina",
       trustStore: {
           path: "${ballerina.home}/bre/security/ballerinaTruststore.p12",
           password: "ballerina"
       }
   }
};

http:Client httpEndpoint = new("https://localhost:9090", config = {
   auth: {
       scheme: http:BASIC_AUTH,
       config: {
           username: "tom",
           password: "1234"
       }
   }
});

listener http:Listener secureListener = new http:Listener(9090, config = {
   authProviders:[jwtAuthProvider],
   secureSocket: {
       keyStore: {
           path: "${ballerina.home}/bre/security/ballerinaKeystore.p12",
           password: "ballerina"
       },
       trustStore: {
           path: "${ballerina.home}/bre/security/ballerinaTruststore.p12",
           password: "ballerina"
       }
   }
});

@http:ServiceConfig {
   authConfig: {
       authentication: { enabled: true }
   }
}
service echo on secureListener {

   @http:ResourceConfig {
       authConfig: {
           scopes: ["hello"]
       }
   }
   resource function hello(http:Caller caller, http:Request req)
                               returns error? {
       http:Response res = check httpEndpoint->get("/secured/endpoint");
       check caller->respond(res);
   }
}
