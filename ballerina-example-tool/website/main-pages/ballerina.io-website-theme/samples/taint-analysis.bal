import ballerina/mysql;

function secureOperation(@sensitive string secureParameter) { }

public function main(string... args) returns error? {
    // Pass input argument to security sensitive parameter
    secureOperation(args[0]);

    if (isInteger(args[0])) {
        // After sanitizing the content untaint can be used
        secureOperation(untaint args[0]);
    } else {
        error err = error("Error: ID should be an integer");
        panic err;
    }

    // Tainted return value cannot be passed into sensitive parameter
    json taintedJson = generateTaintedData();
    secureOperation(check string.convert(taintedJson.name));

    // Untainted return value can be passed into sensitive parameter
    string sanitizedData = sanitize(check string.convert(
                                        taintedJson.firstname));
    secureOperation(sanitizedData);

    return;
}

function generateTaintedData() returns @tainted json {
    json j = [{"id":"1001","ccnum":1111,"name":"John@"}];
    return j;
}

function sanitize(string input) returns @untainted string {
    string regEx = "[^a-zA-Z]";
    return input.replace(regEx, "");
}

function isInteger(string input) returns boolean {
    string regEx = "\\d+";
    boolean|error isInt = input.matches(regEx);
    return isInt is boolean ? isInt : false;
}