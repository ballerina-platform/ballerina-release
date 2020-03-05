import ballerina/http;

map<json> ordersMap = {};

@http:ServiceConfig { basePath: "/ordermgt" }
service orderMgt on new http:Listener(9090) {

   @http:ResourceConfig {
       methods: ["GET"],
       produces: ["application/json"],
       path: "/order/{orderId}"
   }
   resource function findOrder(http:Caller caller, http:Request req,
                               string orderId) returns error? {
       json? payload = ordersMap[orderId];

       http:Response response = new;
       response.setPayload(untaint payload);

       check caller->respond(response);
   }

   @http:ResourceConfig {
       methods: ["POST"],
       consumes: ["application/json"],
       produces: ["application/json"],
       path: "/order"
   }
   resource function addOrder(http:Caller caller, http:Request req) returns error? {
       json|error orderReq = req.getJsonPayload();
       if (orderReq is json) {
           string orderId = orderReq.Order.ID.toString();
           ordersMap[orderId] = orderReq;

           json payload = { status: "Order Created.", orderId: orderId };

           http:Response response = new;
           response.setPayload(untaint payload);
           response.statusCode = 201;
           response.setHeader("Location",
               "http://localhost:9090/ordermgt/order/" + orderId);

           check caller->respond(response);
       } else {
           http:Response response = new;
           response.statusCode = 400;
           check caller->respond(response);
       }
   }
}