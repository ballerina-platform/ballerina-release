---
layout: ballerina-left-nav-release-notes
title: Swan Lake 2201.1.0
permalink: /downloads/swan-lake-release-notes/2201.1.0/
active: swan-lake-2201.1.0
redirect_from: 
    - /downloads/swan-lake-release-notes/2201-1-0
    - /downloads/swan-lake-release-notes/2201-1-0-swan-lake/
    - /downloads/swan-lake-release-notes/2201-1-0-swan-lake
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---

### Overview of Ballerina Swan Lake 2201.1.0 (Swan Lake)

<em>2201.1.0 (Swan Lake) is the first update of 2201.1.0 (Swan Lake), and it includes a new set of features and significant improvements to the compiler, runtime, standard library, and developer tooling. It is based on the 2022R2 version of the Language Specification.</em> 


### Updating Ballerina

If you are already using Ballerina, use the [Ballerina Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Swan Lake Beta6 by running the command below.

> `bal dist pull 2201.1.0`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### Improvements

##### Support to Provide Values for Configurable Variables through TOML In-line Tables

The configurable feature is improved to support TOML in-line tables through the TOML syntax.
The values for configurable variables of types `map` and `record` can be now provided using TOML in-line tables.
Similarly, the values for configurable variables of types array of `map`, array of `record`, and `table` can be now provided using the TOML array of TOML in-line tables.

For example, if the configurable variables are defined in the following way,

```ballerina
configurable map<anydata> mapVar = ?;
configurable Person recordVar = ?;
configurable table<map<int>> tableVar = ?;
configurable Person[] recordArrayVar = ?;

```

the values can be provided in the `Config.toml` file as follows.

```
mapVar = {a = "a", b = 2, c = 3.4, d = [1, 2, 3]}

recordVar = {name = "Jane"}

tableVar = [{a = 1, b = 2}, {c = 3}, {d = 4, e = 5, f = 6}]

recordArrayVar = [{name = "Tom"}, {name = "Harry"}]

```

##### Improved Configurable Variables to Support Tuple Types Through TOML Syntax

The configurable feature is improved to support variables of tuple types through the TOML syntax.

For example, if the tuple-typed configurable variables are defined in the following way,

```ballerina
configurable [int, string, float, decimal, byte, boolean] simpleTuple = ?;
configurable [int[], [string, int], map<anydata>, table<map<string>>] complexTuple = ?;
configurable [int, string, int...] restTuple = ?;
```

the values can be provided in the `Config.toml` file as follows.

```
simpleTuple = [278, "string", 2.3, 4.5, 2, true]

complexTuple = [[1, 3, 5, 7, 9], ["apple", 2], {name = "Baz Qux", age = 22}, [{a = "a"}, {b = "b", c = "c"}]]

restTuple = [1, "foo", 2, 3, 4, 5]
```

##### Improved Configurable Variables to Support Union Types Through CLI Arguments

The configurable feature is improved to support variables of union types with simple basic typed members through the CLI arguments.

For example, if the configurable variables are defined in the following way,

```ballerina
configurable float|int|string unionVar = ?; 
```

the values can be provided via CLI arguments in the following way.

```
bal run -- -Cval=5.0
```

##### Improved Runtime Error Creator and Value Creator API input validations

In order to handle Java Exceptions due to the invalid use of Ballerina runtime error creator and value 
creator APIs, input validations has been improved to provide proper ballerina runtime errors.
For example, the following invalid use of `ValueCreator.createRecordValue` API to create a record value with Java ArrayList as a field of it will result in panic.

```java
 public class App {

    private static Module module = new Module("org", "interop_project.records", "1");

    public static BMap<BString, Object> getRecord(BString recordName) {
        ArrayList<Integer> arrayList = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5));
        Map<String, Object> map = Map.ofEntries(
                Map.entry("arrList", arrayList)
        );
        return ValueCreator.createRecordValue(module, recordName.getValue(), map);
    }
}
```

in modules/records
```ballerina
import ballerina/jballerina.java;

public type Foo record {
    int[] x;    
};

public function getRecord(string recordName) returns record{} = @java:Method {
    'class: "javalibs.app.App"
} external;
```
main.bal
```ballerina
import interop_project.records;

public function main() {
    records:Foo foo =  <records:Foo> records:getRecord("Foo");
}
```
Runtime Error:
```
'class java.util.ArrayList' is not from a valid java runtime class. " +
        "It should be a subclass of one of the following: java.lang.Number, java.lang.Boolean or " +
        "from the package 'io.ballerina.runtime.api.values'
```

#### New Runtime Java APIs
##### Runtime API to create an enum type
New runtime Java API can be used to create enum types from native code.


```java
public static UnionType createUnionType(List<Type> memberTypes, String name, Module pkg, int typeFlags, boolean isCyclic, long flags)
```

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.1.0%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

#### `ftp` Package

- Introduced the `ftp:Caller` API and added it as an optional parameter in the `onFileChange` method
- Added compiler plugin validation support for the `ftp:Service`
- Added code-actions to generate a `ftp:Service` template

##### `http` Package

- Introduced `ResponseInterceptor` and `ResponseErrorInterceptor`
- Introduced `DefaultErrorInterceptor`
- Added code-actions to generate the interceptor method template
- Allowed records to be annotated with `@http:Header`
- Added basic type support for header parameters in addition to `string` and `string[]`
- Added `anydata` support for service and client data binding
- Added common constants for HTTP status-code responses
- Added union type support for service and client data binding
- Added OpenAPI definition field in the service config

##### `websocket` Package

- Introduced the `writeMessage` client and caller APIs
- Introduced the `onMessage` remote function for services
- Added `anydata` data binding support for the `writeMessage` API and `onMessage` remote function

##### `graphql` Package

- Added the support for GraphQL `subscriptions`
- Added the support for GraphQL `interfaces`
- Added the support for GraphQL `documentation`
- Added the `GraphiQL client` support for GraphQL services

##### `websub` Package

- Add code-actions to generate a `websub:SubscriberService` template

##### `kafka` Package

- Added data binding support for `kafka` producer and consumer

##### `rabbitmq` Package

- Added data binding support for `rabbitmq` clients and services
- Added code-actions to generate a `rabbitmq:Service` template

##### `nats` Package

- Added data binding support for `nats` clients and services
- Added code-actions to generate a `nats:Service` template

##### `regex` Package

- Introduced the API to extract the first substring from the start index in the given string that matches the regex
- Introduced the API to extract all substrings in the given string that match the given regex
- Introduced the API to replace the first substring from the start index in the given string that matches the given regex with the provided replacement string or the string returned by the provided function. The `replaceFirst()` API is being deprecated by introducing this API
- Allowed passing a replacer function to `replace` and `replaceAll` APIs. Now the regex matches can be replaced with a new string value or the value returned by the specified replacer function

##### `file` Package

- Introduced the constants for path and path list separators
  - `file:pathSeparator`: It is a character used to separate the parent directories, which make up the path to a specific location. For windows, it’s `\` and for UNIX it’s `/`
  - `file:pathListSeparator`: It is a character commonly used by the operating system to separate paths in the path list. For windows, it’s `;` and for UNIX it’s `:`

##### `os` Package
- Introduced the `setEnv()` function to set an environment variable
- Introduced the `unsetEnv()` function to remove an environment variable from the system
- Introduced the `listEnv()` function to list the existing environment variables of the system

#### Improvements

##### `http` Package

- Allowed `Caller` to respond an `error` or a `StatusCodeResponse`
- Appended the HTTPS scheme (`https://`) to the client URL if security is enabled
- Refactored the auth-desugar response with a `DefaultErrorInterceptor`
- Hid the subtypes of the `http:Client`

##### `jwt` Package

- Appended the HTTPS scheme (`https://`) to the client URL (of JWKs endpoint) if security is enabled

##### `oauth2` Package

- Appended the HTTPS scheme (`https://`) to the client URL (of token endpoint or introspection endpoint) if security is enabled

#### Bug Fixes

##### `grpc` Package

- Fix incorrect stub generation for repeated values of any, struct, timestamp, and duration messages
- Fix incorrect caller type name validation in the gRPC compiler plugin
- Fix passing protobuf predefined types as repeated values and values in messages

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%222201.1.0%22+label%3AType%2FBug).

### Deployment updates

#### Improvements
- Reduced the package size of `ballerina/cloud`
- Docker image generation now relies on the user's docker client
- The `ballerinax/awslambda` package is now available in [Ballerina Central](https://central.ballerina.io/ballerinax/awslambda)
- The `ballerinax/azure_functions` package is now available in [Ballerina Central](https://central.ballerina.io/ballerinax/azure.functions)

#### Breaking Changes
- For existing `ballerinax/awslambda` and `ballerinax/azure_functions` projects, change the version to `2.1.0` in the `Dependencies.toml` file.

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.1.0 of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.1.0%22)

### Developer Tools Updates

#### New Features

##### AsyncAPI Tool

- Ballerina AsyncAPI tooling will make it easy for you to start the development of an event API documented in an AsyncAPI contract in Ballerina by generating Ballerina service and listener skeletons. Ballerina Swan Lake supports the AsyncAPI Specification version 2.x. For more information, see [Ballerina AsyncAPI support](http://ballerina.io/learn/ballerina-asyncapi-support) and [AsyncAPI CLI documentation](http://ballerina.io/learn/cli-documentation/asyncapi/#asyncapi-to-ballerina).

##### GraphQL Tool

- Introduced the Ballerina GraphQL tool, which will make it easy for you to generate a client in Ballerina given the GraphQL schema (SDL) and GraphQL queries. Ballerina Swan Lake supports the GraphQL specification [October 2021 edition](https://spec.graphql.org/October2021/). For more information, see [Ballerina GraphQL support](http://ballerina.io/learn/ballerina-graphql-support/) and [Graphql CLI documentation](http://ballerina.io/learn/cli-documentation/graphql/#graphql-to-ballerina).

##### Language Server

- Added completion and code action support for already-imported modules in the Ballerina user home
- Implemented file operation events in the Language Server

#### Improvements

##### Debugger
- Added rutime breakpoint verification support. With this improvement, the debugger is expected to verify all the valid breakpoint locations in the current debug source. All the breakpoints that are set on non-executable lines of code (i.e., Ballerina line comments, documentation , blank lines, declarations, etc.) will be marked as `unverified` in the editor.

##### Language Server

- Improve the `Document this code` action to support module-level variables
- Added signature help for included record params
- Revamp the code action utilities introducing a new API to find the top-level node for a given code action context
- Improved completion item sorting in several contexts
- Improved the `Create function` code action to handle named arguments
- Improved the `Create function` code action to add an isolated qualifier
- Added signature help for union-typed expressions

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.1.0 of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FLanguageServer+milestone%3A%22Ballerina+Swan+Lake+2201.1.0%22)
- [Debugger](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AArea%2FDebugger+milestone%3A%22Ballerina+2201.1.0%22)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.1.0%22)

#### Ballerina Packages Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+2201.1.0%22+label%3AType%2FBug).

### Breaking Changes

<style>.cGitButtonContainer, .cBallerinaTocContainer {display:none;}</style>
