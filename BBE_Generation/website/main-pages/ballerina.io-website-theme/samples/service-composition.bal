import ballerina/http;

http:Client airlineEP = new("http://localhost:9091/airline");

http:Client hotelEP = new("http://localhost:9092/hotel");

@http:ServiceConfig {basePath:"/travel"}
service travelAgencyService on new http:Listener(9090) {

   @http:ResourceConfig {
       methods:["POST"]
   }
   resource function arrangeTour(http:Caller caller,
                                   http:Request inRequest) returns error? {
       json|error inReqPayload = inRequest.getJsonPayload();

       if (inReqPayload is json) {
           json outReqPayload = {
                               "Name":inReqPayload.Name,
                               "ArrivalDate":inReqPayload.ArrivalDate,
                               "DepartureDate":inReqPayload.DepartureDate,
                               "Preference":""
                            };

           outReqPayload.Preference = inReqPayload.Preference.Airline;
           http:Response|error inResAirline = airlineEP->post(
               "/reserve", untaint outReqPayload);

           // Implement the business logic for the retrieved response
           outReqPayload.Preference =
                           inReqPayload.Preference.Accommodation;
           http:Response|error inResHotel = hotelEP->post(
               "/reserve", untaint outReqPayload);

           // Implement the business logic for the retrieved response
           if (inResAirline is http:Response
                           && inResHotel is http:Response) {
               http:Response outResponse = new;
               outResponse.setPayload({"Message":"Congratulations! " +
                   "Your journey is ready!!"});
               check caller->respond(outResponse);
               return;
           }

           json errMsg;
           if (inResAirline is error) {
               errMsg = {"Message":"Failed to reserve the air ticket"};
           } else {
               errMsg = {"Message":"Failed to reserve the hotel"};
           }

           http:Response errResponse = new;
           errResponse.setPayload(errMsg);
           check caller->respond(errResponse);
       } else {
           http:Response errResponse = new;
           errResponse.statusCode = 400;
           errResponse.setPayload("Invalid JSON payload");
           check caller->respond(errResponse);
       }
   }
}
