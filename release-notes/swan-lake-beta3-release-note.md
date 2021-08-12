---
layout: ballerina-left-nav-release-notes
title: Swan Lake Beta3
permalink: /downloads/swan-lake-release-notes/swan-lake-beta3/
active: swan-lake-beta3
redirect_from: 
    - /downloads/swan-lake-release-notes/swan-lake-beta3
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---
### Overview of Ballerina Swan Lake Beta3

<em>This is the third beta release leading up to the Ballerina Swan Lake GA release.</em> 

It introduces the new language features planned for the Swan Lake GA release and includes improvements and bug fixes done to the compiler, runtime, standard library, and developer tooling after the Swan Lake Beta2 release.

### Updating Ballerina

If you are already using Ballerina, you can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Ballerina Swan Lake Beta3 as follows. 

To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake <VERSION>.

> `bal dist pull slbeta3`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### Improvements

##### Improved configurable variables to support xml types through TOML syntax

The `configurable` feature is improved to support variables with xml types through the TOML syntax.

For example, if the xml typed configurable variables are defined in the following way,

``` ballerina
configurable xml xmlVar = ?;
```
The values can be provided in `Config.toml` as follows,


```toml
xmlVar = "<book><name>Sherlock Holmes</name></book>"
```

##### Improved configurable variables to support additional fields and rest fields for records

The `configurable` feature is improved to support additional fields and rest fields in record variables through the TOML syntax.

For example, if a configurable variable with open record type is defined in the following way,

```ballerina
type Person record {
};

configurable Person person = ?;
```

The values can be provided in `Config.toml` as follows,


```toml
[person]
intVal = 22
floatVal = 22.33
stringVal = "abc"
arrVal = [1,2,3]
mapVal.a = "a"
mapVal.b = 123
```

The additional fields that are created from the TOML values will have the following types.

TOML Integer - `int`
TOML Float - `float`
TOML String - `string`
TOML Boolean - `boolean`
TOML Table - `map<anydata>`
TOML Table array - `map<anydata>[]`

Similarly, if a configurable variable with a record type that contains a rest field is defined in the following way

```ballerina
public type Numbers record {|
   int ...;
|};

configurable Numbers numbers = ?;
```

The values can be provided in `Config.toml` as follows,


```toml
num1 = 11
num2 = 26
```

##### Improved print error stacktrace with cause

Error stack trace has been improved to have the error cause locations. Stack frames of the wrapped error causes are also added to the stack trace.

e.g:
For the following example,
```ballerina
public function main() {
    panic bar();
}
function bar() returns error {
    return error("a", y());
}
function y() returns error {
    return x();
}
function x() returns error {
    return error("b");
}
```

The expected stack trace is

```
error: a
at cause_location.0:bar(main.bal:6)
cause_location.0:main(main.bal:2)
cause: b
at cause_location.0:x(main.bal:14)
cause_location.0:y(main.bal:10)
... 2 more
```

##### New Runtime Java APIs

###### Invoke ballerina object method asynchronously
New JAVA Runtime API is introduced for execute ballerina object method from Java. Object method caller can decide weather to execute the object method sequentially or concurrently using isIsolated parameter.

```java
invokeMethodAsync(BObject, String, String, StrandMetadata, boolean, Callback, Map, Type, Object...)}
```

Previous invokeMethodAsync methods are deprecated.

######  API to retrieve ballerina object or object method is isolated

Following two new APIs are introduced to ObjectType.
```java
    boolean isIsolated();

    boolean isIsolated(String methodName);
```

##### Removed package version from runtime

Full qualified package version has been removed from runtime and will only have major version. So when we provide 
the version to ballerina runtime java api like create runtime values, we need to provide only package runtime version. Stacktraces will contain only major package versions.


#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

##### Crypto Package
- Improved the hash APIs for cryptographic salt

##### GraphQL Package
- Added field alias support for GraphQL documents
- Added variable support in GraphQL requests
- Added mutation support for GraphQL services
- Added typename introspection

##### gRPC Package
- Added declarative auth configurations
- Added timestamp, duration, and struct type support

##### HTTP Package
- Enabled HTTP trace and access log support
- Added HATEOAS link support
- Introduced the `http:CacheConfig` annotation to the resource signature
- Introduced support for the service-specific media-type subtype prefix
- Introduced the introspection resource method to get the generated OpenAPI document of the service

##### JWT Package
- Added HMAC signature support for JWT
  
##### Log Package
- Added observability span context values to the log messages when observability is enabled.

##### SQL Package
- Added support for `queryRow()` in the database connectors. This method allows retrieving a single row as a record, or a single value from the database.
```ballerina
record{} queryResult = sqlClient->queryRow(`SELECT * FROM ExTable where row_id = 1`)
int count = sqlClient->queryRow(“SELECT COUNT(*) FROM ExTable”)
```

#### Improvements

##### GraphQL Package
- Validate the `maxQueryDepth` at runtime as opposed to validating it at compile time

##### HTTP Package
- Added support for the `map<json>` as query parameter type
- Added support for nilable client data binding types

##### WebSocket Package
- Made the WebSocket caller isolated
- Introduced a write timeout for the WebSocket client

##### SQL Package
- Improved the throughput performance with asynchronous database queries
- Introduced new array out parameter types in call procedures.
- Changed the return type of the SQL query API to include the completion type as nil in the stream. The SQL query code below demonstrates this change.
    
    **Previous Syntax**
    ```ballerina
    stream<RowType, error> resultStream = sqlClient->query(“”);
    ```
    **New Syntax**
    ```ballerina
    stream<RowType, error?> resultStream = sqlClient->query(“”);
    ```

##### IO Package
- Changed the `io:readin` function input parameter to optional. In the previous API, it was required to pass a value to be printed before reading the user input as a string. Remove it due to the breaking change and made it optional. It is not recommended to pass a value to print it in the console.

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Beta3%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22).

### Developer Tools Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake Beta2 of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug+label%3ATeam%2FLanguageServer)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta%22)
- [Debugger](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+label%3AType%2FBug+label%3AArea%2FDebugger+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta2%22)
- [Test Framework](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+label%3ATeam%2FTestFramework+milestone%3A%22Ballerina+Swan+Lake+-+Beta2%22+label%3AType%2FBug+)

#### Ballerina Packages Updates

### Breaking Changes
