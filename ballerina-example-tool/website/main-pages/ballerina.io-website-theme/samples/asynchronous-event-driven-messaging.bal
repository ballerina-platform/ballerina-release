// Consumer Example
// --------------------------------------------------------

import ballerina/io;
import wso2/kafka;

listener kafka:SimpleConsumer consumer = new({
    bootstrapServers: "localhost:9092, localhost:9093",
    groupId: "inventorySystem",
    topics: ["product-price"],
    pollingInterval:1000
});

service kafkaService on consumer {
    resource function onMessage(kafka:SimpleConsumer simpleConsumer,
                        kafka:ConsumerRecord[] records) returns error? {
        foreach var entry in records {
            byte[] serializedMsg = entry.value;
            io:WritableByteChannel byteChannel =
                        io:openWritableFile("/some/Path", append = true);
            int writtenBytes = check byteChannel.write(serializedMsg, 0);
        }
        return;
    }
}

// Producer Example
// --------------------------------------------------------

import ballerina/http;
import wso2/kafka;

kafka:SimpleProducer kafkaProducer = new({
    bootstrapServers: "localhost:9092",
    clientID:"basic-producer",
    acks:"all",
    noRetries:3
});

service productAdminService on new http:Listener(9090) {

    resource function updatePrice(http:Caller caller, http:Request request)
                                    returns error? {
        json|error reqPayload = request.getJsonPayload();

        if (reqPayload is json) {
            byte[] serializedMsg = reqPayload.toString().toByteArray("UTF-8");
            var result = check kafkaProducer->send(serializedMsg,
                                    "product-price", partition = 0);

            http:Response response = new;
            response.setJsonPayload({"Status":"Success"});
            _ = caller->respond(response);
        } else {
            http:Response errResp = new;
            errResp.statusCode = 400;
            errResp.setPayload("Invalid JSON payload received");
            _ = caller->respond(errResp);
        }
        return;
    }
}