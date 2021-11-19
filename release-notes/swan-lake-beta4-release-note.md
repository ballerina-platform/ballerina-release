---
layout: ballerina-left-nav-release-notes
title: Swan Lake Beta4
permalink: /downloads/swan-lake-release-notes/swan-lake-beta4/
active: swan-lake-beta4
redirect_from: 
    - /downloads/swan-lake-release-notes/swan-lake-beta4
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---
### Overview of Ballerina Swan Lake Beta4

<em>This is the fourth Alpha release in a series of planned Alpha and Beta releases leading up to the Ballerina Swan Lake GA release.</em> 

It introduces the new language features planned for the Swan Lake GA release and includes improvements and bug fixes done to the compiler, runtime, standard library, and developer tooling after the Swan Lake Beta3 release.

### Updating Ballerina

If you are already using Ballerina, you can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Ballerina Swan Lake Beta4 as follows. 

To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake Beta4.

> `bal dist pull slbeta4`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

##### Improved Error Messages on a Type Conversion Failure

Detailed error messages are now given on a type conversion failure narrowing down the specific location of errors in the structural types. A maximum number of 20 errors are shown at a time.

E.g.,
```ballerina
type Journey record {|
    map<int> destinations;
    boolean[] enjoyable;
    [string, decimal] rating;
|};

type tupleType [Journey, [Journey, map<Journey>], ()[], int...];

public function main() {
    json j = [
        {"destinations": {"Bali": "2", "Hawaii": 3}, "enjoyable": true},
        [
            12,
            {
                "first": {
                    "destinations": {"Bali": true, "Hawaii": "3"},
                    "enjoyable": [1],
                    "rating": [10, 8.5]
                }
            }
        ],
        [null, 0],
        "12345678901234567890123"
    ];
    tupleType val = checkpanic j.cloneWithType();
}
``` 
now gives
```
error: {ballerina/lang.value}ConversionError {"message":"'json[]' value cannot be converted to '[Journey,[Journey,map<Journey>],()[],int...]': 
                missing required field '[0].rating' of type '[string,decimal]' in record 'Journey'
                map field '[0].destinations.Bali' should be of type 'int', found '"2"'
                field '[0].enjoyable' in record 'Journey' should be of type 'boolean[]', found 'true'
                tuple element '[1][0]' should be of type 'Journey', found '12'
                map field '[1][1].first.destinations.Bali' should be of type 'int', found 'true'
                map field '[1][1].first.destinations.Hawaii' should be of type 'int', found '"3"'
                array element '[1][1].first.enjoyable[0]' should be of type 'boolean', found '1'
                tuple element '[1][1].first.rating[0]' should be of type 'string', found '10'
                array element '[2][1]' should be of type '()', found '0'
                tuple element '[3]' should be of type 'int', found '"1234567890123456789...'"}
        at ballerina.lang.value.0:cloneWithType(value.bal:86)
           errmsg:main(errmsg.bal:18)
```

##### Improvement in the Runtime Error Creator API 

The runtime Java error creator API has been improved to get a `BMap` as the `details` parameter. 

```Java
BError createError(Module module, String errorTypeName, BString message, BError cause, BMap<BString, Object> details)
```

#### New Runtime Java APIs

##### API to Access Information of Type Inclusions at the Runtime

A new API is introduced to retrieve the type IDs of the given `io.ballerina.runtime.api.types.ObjectType`.

```Java
TypeIdSet getTypeIdSet();
``` 

##### API to Retrieve the Constituent Types of an Intersection Type

A new API is introduced to provide the list of constituent types of a given `io.ballerina.runtime.api.types.IntersectionType`.

```Java
List<Type> getConstituentTypes();
``` 

#### Bug Fixes

##### Removed Supporting the Single-Quote to Mark the Boundary of a JSON String Value 

To comply with the JSON [specification](https://www.json.org/), the JSON parser is no longer supporting single quotes to mark the boundaries of a string. Only double quotes are supported.

```ballerina
public function main() {
    string s = "{ 'foo': 'bar' }";
    json j = checkpanic s.fromJsonString();
    // this will now result in a runtime error
}
```

##### Throw Unused Configurable Value Warnings as Errors

When there is a configuration value provided in the `Config.toml` file or a command line argument that does not match
with the existing configurable variables, it will fail at runtime with an error instead of a warning.

For example, if you have the following in the `main.bal` file,

```ballerina
configurable int a = ?;
```

and the following in the `Config.toml` file,

```toml
a = 2
b = "invalid"

[c]
d = 45
```

then, it will fail with the following errors.

```
error: [Config.toml:(2:1,2:14)] unused configuration value 'b'
error: [Config.toml:(4:1,5:7)] unused configuration value 'c'
error: [Config.toml:(5:1,5:7)] unused configuration value 'c.d'
```

To view bug fixes, see the [GitHub milestone for Swan Lake Beta4](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

##### MySQL Package
- Introduced failover and retries support
- Added `noAccessToProcedureBodies` options

##### Log Package
- Introduced the `setOutputFile` function to write the log output to a file

##### HTTP Package
- Introduced request and request error interceptors
- Added `noAccessToProcedureBodies` options

##### gRPC Package
- Introduced Protobuf `Any` type support

#### Improvements

##### SQL Package
- Improved the `queryRow()` function to support union return types
- Improved the parameterized query to support the escaped backtick as insertions

##### Log Package
- Added `error:StackFrame[]` as a key-value pair type
    
##### HTTP Package
- Marked the HTTP service type as distinct
- Relaxed the data-binding restriction for status codes without content
- Changed the `Listener.getConfig()` API to return an `InferredListenerConfiguration`

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Beta4%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake <VERSION> of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22)
- [Docker](https://github.com/ballerina-platform/module-ballerina-docker/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22)
- [AWS Lambda](https://github.com/ballerina-platform/module-ballerinax-aws.lambda/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22)
- [Azure Functions](https://github.com/ballerina-platform/module-ballerinax-azure.functions/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22) 

### Developer Tools Updates

#### Language Server 
- Added document symbol support

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22+label%3AType%2FBug+label%3ATeam%2FLanguageServer).

#### New Features

##### Debugger
- Added support for debug pause instructions. With this support, any running Ballerina programs can be suspended immediately at the current execution line of the program.
- [Preview Feature] Introduced Ballerina code completion support in the VSCode debug console. Now, a context-aware completion list will be suggested automatically for Ballerina expressions in the VSCode evaluation window.
- Added string template support for debug logpoints. Now, you can interpolate expressions within debug logpoint messages by using the `${}` syntax so that the debug logpoints can be used to log state variable information without suspending the program. 

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake <VERSION> of the repositories below.

- [Language](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22+label%3AType%2FBug+label%3ATeam%2FDevTools)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22) 

#### Ballerina Packages Updates

### Breaking Changes
