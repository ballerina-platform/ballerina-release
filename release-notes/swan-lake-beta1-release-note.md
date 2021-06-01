---
layout: ballerina-left-nav-release-notes
title: Swan Lake Beta1
permalink: /downloads/swan-lake-release-notes/swan-lake-beta1/
active: swan-lake-alpha5
redirect_from: 
    - /downloads/swan-lake-release-notes/swan-lake-beta1
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---
### Overview of Ballerina Swan Lake Beta1

<em>This is the Beta1 release in a series of planned Alpha and Beta releases leading up to the Ballerina Swan Lake GA release.</em> 

It introduces the new language features planned for the Swan Lake GA release and includes improvements and bug fixes done to the compiler, runtime, standard library, and developer tooling after the Swan Lake Alpha5 release.

- [Updating Ballerina](#updating-ballerina)
- [Installing Ballerina](#installing-ballerina)
- [Language Updates](#language-updates)
- [Runtime Updates](#runtime-updates)
- [Standard Library Updates](#standard-library-updates)
- [Code to Cloud Updates](#code-to-cloud-updates)
- [Developer Tools Updates](#developer-tools-updates)
- [Ballerina Packages Updates](ballerina-packages-updates)

### Updating Ballerina

If you are already using Ballerina, you can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Ballerina Swan Lake Beta1 as follows. 

To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake Beta1.

> `bal dist pull beta1`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta1](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta1%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

##### Improved configurable variables to support for enum types

Configurable variables with enum types are supported to provide values through command-line arguments and a TOML file.
For example, see the configurable variable with enum type.

```ballerina
public enum HttpVersion {
    HTTP_1_1,
    HTTP_2
}

configurable configLib:HttpVersion & readonly httpVersion = ?;
```

The value for  'httpVersion' can be provided via the 'Config.toml' file or as a command-line argument as below.

TOML

```toml
[configUnionTypes]
httpVersion = "HTTP_1_1"
```

Command-line argument:

```
-ChttpVersion=HTTP_1_1
```

##### Improved configurable variables to support for map types

The `configurable` feature is improved to support variables with map types through the TOML syntax. 
For example, if the map-typed configurable variables are defined in the following way, 

``` ballerina
configurable map<string> admin = ?;

type HttpResponse record {|
    string method;
    string httpVersion = "HTTP_1_0";
    map<string> headers;
|};

configurable HttpResponse response = ?;
configurable map<string>[] users = ?;
```
The values can be provided in `Config.toml` as follows.


```toml
[admin]
username = "John Doe"
mail = "John@hotmail.com"
location = "LK"

[response]
method = "POST"
httpVersion = "HTTP_2_0"
headers.Status = "200 OK"
headers.Content-Type = "text/html"

[[users]]
username = "Jack"
location = "UK"

[[users]]
username = "Jane"
location = "US"
```

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta1](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta1%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

##### `graphql` Package
- Add declarative auth configurations
- Support optional types as inputs
- Support returning distinct service object unions
- Support inline fragments
- Support enums as input values

#### Improvements

##### `cache` Package
- Marked the `cache:Cache` class as an isolated class.

##### `file` Package
- Marked the `file:Listener` class as an isolated class.

##### `graphql` Package
- Improved introspection validation and execution
- Added missing fields in the GraphQL types
- Compiler plugin improvements to validate inputs and return types
- Use included record parameters instead of the record type in the listener initialization

##### `http` Package
- Improved the `http:Client` remote methods to support the contextually-expected type inference
- Changed the configuration parameters of the listeners and clients to include the record parameters

##### `sql` Package
- Added the SQL Array Value type support and introduced the new distinct array value types for identified SQL types
- Marked the `sql:Client` class as an isolated class

##### `websubhub` Package
- Include the auth configuration to the WebSubHub publisher client configuration

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta1](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Beta1%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features
- Add `@cloud:Expose` annotation to support custom listeners

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake Beta1 of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta1%22)
- [Docker](https://github.com/ballerina-platform/module-ballerina-docker/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta1%22)
- [AWS Lambda](https://github.com/ballerina-platform/module-ballerinax-aws.lambda/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta1%22)
- [Azure Functions](https://github.com/ballerina-platform/module-ballerinax-azure.functions/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta1%22) 

### Developer Tools Updates

#### Language Server 

To view bug fixes, see the [GitHub milestone for Swan Lake Beta1](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+BetaRC1%22+label%3AType%2FBug+label%3ATeam%2FLanguageServer).

#### New Features

##### Debugger
- Added remote debugging support for the command, which runs the Ballerina executable JAR.
- Added support for debugging single Ballerina tests in Visual Studio Code.

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake Beta1 of the repositories below.

- [Language](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta1%22+label%3AType%2FBug+label%3ATeam%2FDevTools)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta%22) 

#### Ballerina Packages Updates

### Breaking Changes
