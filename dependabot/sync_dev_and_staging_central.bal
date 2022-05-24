import ballerina/file;
import ballerina/io;
import ballerina/log;
import ballerina/os;

const BAL_PREFIX = "ballerina-";
const BALA_ARCHIVE_PATH = "bala/";
const EXTENSIONS_FILE_PATH = "dependabot/resources/extensions.json";

string VERSION = os:getEnv("BAL_VERSION_ID");
string DIST_VERSION = string `${BAL_PREFIX}${VERSION}-${os:getEnv("BAL_VERSION_CODE_NAME")}`;
string DIST_BALA_PATH = string `${DIST_VERSION}/distributions/${BAL_PREFIX}${VERSION}/repo/bala/ballerina/`;

public function main() returns error? {
    error? gatherModuleBalasResult = gatherModuleBalas();
    if gatherModuleBalasResult is error {
        log:printError("Could not gather the module Balas due to " + gatherModuleBalasResult.message());
        return ;
    }
}

// Identifies the stdlibs using the extensions.json resource and gathers their respective balas from the distribution
function gatherModuleBalas() returns error? {
    check file:createDir(BALA_ARCHIVE_PATH);

    json extensionsJson = check io:fileReadJson(EXTENSIONS_FILE_PATH);
    json[] stdlibModules = <json[]> check extensionsJson.standard_library;

    foreach json module in stdlibModules {
        boolean pushToCentral = check module.push_to_central;
        string moduleName =  check module.name;

        if pushToCentral {
            // Extracts the core module name
            // eg: "module-ballerina-jballerina.java.arrays" is identified as "jballerina.java.arrays"
            if moduleName.includes(BAL_PREFIX) {
                int splitIndex = <int>moduleName.lastIndexOf(BAL_PREFIX);
                moduleName = moduleName == "module-ballerina-c2c" ? "cloud" :
                    moduleName.substring(splitIndex + BAL_PREFIX.length(), moduleName.length());
            }
            
            // Verifies the existence of the particular module bala in the distribution
            if check file:test(DIST_BALA_PATH + moduleName, file:EXISTS) {
                string moduleRootDist = string `${DIST_BALA_PATH}${moduleName}`;
                string moduleLevel = (check  module.level).toString();

                // Iterate the sub directories (named version and platform) to arrive at module root
                foreach var i in 0...1 {
                    file:MetaData[] readDirResults = check file:readDir(moduleRootDist);
                    int slashSplitIndex = <int>readDirResults[0].absPath.lastIndexOf("/");
                    moduleRootDist = moduleRootDist + readDirResults[0].absPath.substring(slashSplitIndex,
                                        readDirResults[0].absPath.length());
                }
                
                // Copies the respective stdlib bala to the archive of balas to be pushed
                check file:copy(moduleRootDist,
                                string `${BALA_ARCHIVE_PATH}${moduleLevel}${moduleName}`,
                                file:REPLACE_EXISTING);
            } else {
                log:printWarn("Module " + moduleName + " was not found.");
            }
        } else {
            log:printInfo("Module " + moduleName + " is not pushed to central.");
        }
    }
}
