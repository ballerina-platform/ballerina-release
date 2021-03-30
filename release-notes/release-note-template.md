---
layout: ballerina-blank-page
title: Release Note
---
### Overview of Ballerina Swan Lake <VERSION>

The <VERSION> release includes the language features planned for the Ballerina Swan Lake release. Moreover, this release includes improvements and bug fixes to the language, runtime, standard library, code to cloud, and developer tooling. This release note lists only the features and updates added after the <PREVIOUS_VERSION> release of Ballerina Swan Lake.

- [Updating Ballerina](#updating-ballerina)
    - [For Existing Users](#for-existing-users)
    - [For New Users](#for-new-users)
- [Highlights](#highlights)
- [What is new in Ballerina Swan Lake <VERSION>](#what-is-new-in-ballerina-swan-lake-<VERSION>)
    - [Language](#language)
        - [Bug Fixes](#bug-fixes)
    - [Runtime](#runtime)
        - [Bug Fixes](#bug-fixes)
    - [Standard Library](#standard-library)
        - [Bug Fixes](#bug-fixes)
    - [Code to Cloud](#code-to-cloud)
        - [Bug Fixes](#bug-fixes)
    - [Developer Tools](#developer-tools)
        - [Bug Fixes](#bug-fixes)
    - [Ballerina Packages](ballerina-packages)
    - [Breaking Changes](#breaking-changes)

### Updating Ballerina

You can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to update to Ballerina Swan Lake <VERSION> as follows.

#### For Existing Users

If you are already using Ballerina, you can directly update your distribution to the Swan Lake channel using the [Ballerina Update Tool](/learn/tooling-guide/cli-tools/update-tool/). To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake <VERSION>.

> `bal dist pull slalpha3`

#### For New Users

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Highlights

### What is new in Ballerina Swan Lake <VERSION>

#### Language

##### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha3%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

#### Runtime

##### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha3%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

#### Standard Library

##### New Features

###### Time Package

- Introduced the following APIs to support email typed string conversions:
    - Converts a given UTC to an email string.
        ```ballerina
        import ballerina/time; 
             
        string emailFormattedString = time:utcToEmailString(time:utcNow());
        ```
    - Converts a given Civil to an email string.
        ```ballerina
        import ballerina/time; 
       
        time:Civil civil = check time:civilFromString("2021-04-12T23:20:50.520+05:30[Asia/Colombo]");
        string|time:Error emailDateTime = time:civilToEmailString(civil, "GMT");
        ```
    - Converts a given email string to Civil.
        ```ballerina
        import ballerina/time; 
       
        time:Civil|time:Error emailDateTime = time:civilFromEmailString("Wed, 10 Mar 2021 19:51:55 -0820");
        ```
    
##### Improvements

###### I/O Package

- Improved the print APIs to support string templates.
```ballerina
import ballerina/io;

string val = "John";
io:println(`Hello ${val}!!!`);
io:print(`Hello ${val}!!!`);
```
- Changed streaming APIs to be completed from `nil` return. 

###### MySQL Package

- Changed the previous SSLConfig Record to SecureSocket Record.
```ballerina
public type SecureSocket record {|
    SSLMode mode = SSL_PREFERRED;
    crypto:KeyStore key?;
    crypto:TrustStore cert?;
|};
```

- Changed the SSLMode value from `SSL_VERIFY_CERT` to `SSL_VERIFY_CA`.

###### Xmldata Package

- API for converts a JSON to an XML has been supported the `nil` return value.
```ballerina
import ballerina/xmldata;

json data = {
    name: "John"
};
xml?|Error x = xmldata:fromJson(data);
```

##### Bug Fixes

##### Renamed `java.arrays` Package

The `java.arrays` package’s org and package names were renamed as `ballerina` and `jballerina.java.arrays`. 
```ballerina
import ballerina/jballerina.java.arrays;

handle secondWord = arrays:get(input, 1);
```

##### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Alpha3%22+label%3AType%2FBug).

#### Code to Cloud

##### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake <VERSION> of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha3%22)
- [Docker](https://github.com/ballerina-platform/module-ballerina-docker/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha3%22)
- [AWS Lambda](https://github.com/ballerina-platform/module-ballerinax-aws.lambda/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha3%22)
- [Azure Functions](https://github.com/ballerina-platform/module-ballerinax-azure.functions/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha3%22) 

#### Developer Tools

##### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake <VERSION> of the repositories below.

- [Language](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha3%22+label%3AType%2FBug+label%3ATeam%2FDevTools)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha%22) 

##### Language Server

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha3%22+label%3AType%2FBug+label%3ATeam%2FLanguageServer).


#### Ballerina Packages

### Breaking Changes
