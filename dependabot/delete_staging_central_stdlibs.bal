import ballerina/io;
import ballerina/log;

const EXTENSIONS_FILE_PATH = "dependabot/resources/extensions.json";
const GRADLE_PROPERTIES_FILE_PATH = "dependabot/resources/gradle.properties";
const MODULE_DETAILS_JSON_PATH = "ModuleDetails.json";

const BAL_PREFIX = "ballerina-";

map<string> versionProperties = {};

type Module record {
    string level;
    string packageName;
    string packageVersion;
};

public function main() returns error? {
    error? retrieveModuleVersionsResult = retrieveModuleVersions();
    if retrieveModuleVersionsResult is error {
        log:printError("Could not retrieve module versions due to " + retrieveModuleVersionsResult.message());
        return ;
    } 

    json|error gatherModuleDetailsResult = gatherModuleDetails();
    if gatherModuleDetailsResult is error {
        log:printError("Could not gather details due to " + gatherModuleDetailsResult.message());
        return ;
    } 

    // Create response JSON object to be passed
    json responseObject = {
        standard_library: gatherModuleDetailsResult
    };

    check io:fileWriteJson(MODULE_DETAILS_JSON_PATH, responseObject);
}

// Retrieves and maps the respective X.X.X versions corresponding to the stdlib version keys
function retrieveModuleVersions() returns error? {
    string[] propertiesContent = check io:fileReadLines(GRADLE_PROPERTIES_FILE_PATH);

    foreach string property in propertiesContent {
        if property.includes("Version") {
            int splitVersionKeyIndex = <int>property.indexOf("=");
            int splitVersionIndex = property.includes("-") ? <int>property.indexOf("-") : property.length();
            string versionKey = property.substring(0, splitVersionKeyIndex);
            versionProperties[versionKey] = property.substring(splitVersionKeyIndex + 1, splitVersionIndex);
        }
    }
}

// Maps each stdlib module name to its corresponding X.X.X version using the map created in retrieveModuleVersions()
function gatherModuleDetails() returns json|error {
    Module[] moduleDetails = [];
    json extensionJson = check io:fileReadJson(EXTENSIONS_FILE_PATH);
    json[] modules = <json[]> check extensionJson.standard_library;
    
    foreach json module in modules {
        boolean pushToCentral = check module.push_to_central;

        if pushToCentral {
            string moduleName =  check module.name;

            // Extracts the core module name
            // eg: "module-ballerina-jballerina.java.arrays" is identified as "jballerina.java.arrays"
            if moduleName.includes(BAL_PREFIX) {
                int splitNameIndex = <int>moduleName.lastIndexOf(BAL_PREFIX);
                moduleName = moduleName == "module-ballerina-c2c" ? "cloud" :
                    moduleName.substring(splitNameIndex + BAL_PREFIX.length(), moduleName.length());
            } else if moduleName == "openapi-tools" {
                moduleName = "openapi";
            }

            moduleDetails.push({
                level: (check module.level).toString(),
                packageName: moduleName,
                packageVersion: <string>versionProperties[check module.version_key]
            });
        }
    }

    // Sort modules based on their levels
    moduleDetails = from Module module in moduleDetails
                        order by module.level descending
                    select module;

    return moduleDetails.toJsonString();
}
