import ballerina/grpc;
import ballerina/http;

listener grpc:Listener grpcListener = new(9090);

http:Client backendEP = new("https://ballerina.io/samples");

service UserProfile on grpcListener {

   int nextUserNo = 1;

   resource function addUser(grpc:Caller caller, UserInfo userInfo)
                               returns error? {
       User user = {id:string.convert(self.nextUserNo), info: userInfo};
       json|error userJSON = json.convert(user);

       if (userJSON is json) {
           self.nextUserNo += 1;

           http:Response|error backendRes = backendEP->post(
               "/test/add", untaint userJSON);

           if (backendRes is http:Response) {
               check caller->send(check backendRes.getTextPayload());
           } else {
               check caller->send(backendRes.reason());
           }

       } else {
           check caller->send("Invalid JSON received");
       }
   }

   resource function getUser(grpc:Caller caller, string id)
                               returns error? {
       http:Response backendRes = check backendEP->get(
           "/test/get?id=" + untaint id);

       json|error userJson = backendRes.getJsonPayload();
       User|error user = userJson is json ? User.convert(userJson)
                                           : userJson;

       if (user is User) {
           check caller->send(user);
       } else {
           check caller->send("Invalid user received "
                               + "from the upstream server");
       }
   }
}

type UserInfo record {
   string name;
   int age;
   string email;
};

type User record {
   string id;
   UserInfo info;
};
