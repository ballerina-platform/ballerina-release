import ballerina/io;

public function main () {
    // Create a JSON object out of other primitives
    int i = 4;
    json[] codes = [i, 8];
    json addr = {
        "street":"Main",
        "city":"94"
    };
    json j = {
        "Store":{
            "@id":"AST",
            "name":"Anne",
            "address":addr,
            "codes":codes
        }
    };

    j.Store.name = "Jane";

    io:println("Constructed JSON:");
    io:println(j);

    // Convert the JSON object to XML using the default 
    // `attributePrefix` and the default `arrayEntryTag`.
    xml|error x1 = j.toXML({});

    if (x1 is xml) {
        xml x2 = xml `<!--I am a comment-->`;
        xml x3 = x1 + x2;

        io:println("Produced XML:");
        io:println(x3);
        io:println("Value of an individual element:");
        io:println(x3.selectDescendants("name").getTextValue());
    } else {
        io:println("Failed to convert to XML");
    }
}