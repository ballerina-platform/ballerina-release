---
layout: ballerina-left-nav-release-notes
title: 2201.2.0 (Swan Lake) 
permalink: /downloads/swan-lake-release-notes/2201-2-0/
active: 2201-2-0
redirect_from: 
    - /downloads/swan-lake-release-notes/2201-2-0
    - /downloads/swan-lake-release-notes/2201.2.0/
    - /downloads/swan-lake-release-notes/2201-2-0-swan-lake/
    - /downloads/swan-lake-release-notes/2201-2-0-swan-lake
---

### Overview of Ballerina 2201.2.0 (Swan Lake)

<em>2201.2.0 (Swan Lake) is the second major release of 2022, and it includes a new set of features and significant improvements to the compiler, runtime, standard library, and developer tooling. It is based on the 2022R2 version of the Language Specification.</em> 

### Update Ballerina

>**Info:** The version format has been revised. `2201.2.0 (Swan Lake)` represents the format of `$YYMM.$UPDATE.$PATCH ($CODE_NAME)`. For further information, see [Ballerina Swan Lake is on the Horizon](https://blog.ballerina.io/posts/ballerina-swan-lake-is-on-the-horizon/).

If you are already using Ballerina, use the [Ballerina update tool](/learn/cli-documentation/update-tool/#using-the-update-tool) to directly update to 2201.2.0 (Swan Lake). To do this: 

1. Run the command below to get the latest version of the update tool.

   `bal update`

2. Run the command below to update your Ballerina version to 2201.2.0 (Swan Lake).

   `bal dist update`

#### Troubleshoot 

If you already ran the `bal dist update` (or `bal dist pull 2201.2.0`) before the `bal update` command, follow the instructions below to recover your installation.

##### For macOS Users (`.pkg` installations)

1. Run the `rm ~/.ballerina/ballerina-version` command to delete the version configuration.
2. Run the `chmod 755 /Library/Ballerina/distributions/ballerina-2201.2.0/bin/bal` command to provide execute permissions for the `bal` command.
3. Run the `bal dist use 2201.2.0` command to switch to the 2201.2.0 version. 

##### For Ubuntu Users (`.deb` installations)

1. Run the `rm ~/.ballerina/ballerina-version` command to delete the version configuration.
2. Run the `chmod 755 /usr/lib/ballerina/distributions/ballerina-2201.2.0/bin/bal` command to provide execute permissions for the `bal` command.
3. Run the `bal dist use 2201.2.0` command to switch to the 2201.2.0 version.

##### For CentOS Users (`.rpm` installations)

1. Run the `rm ~/.ballerina/ballerina-version` command to delete the version configuration.
2. Run the `chmod 755 /usr/lib64/ballerina/distributions/ballerina-2201.2.0/bin/bal` command to provide execute permissions for the `bal` command.
3. Run the `bal dist use 2201.2.0` command to switch to the 2201.2.0 version.

##### For Windows Users (`.msi` installations)

1. Run the `del %userprofile%\.ballerina\ballerina-version` command to delete the version configuration.
2. Run the `bal dist use 2201.2.0` command to switch to the 2201.2.0 version.

### Install Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Migrate from Swan Lake Beta releases
>**Info:** If you have been using Swan Lake Beta releases, delete the `Dependencies.toml` files in your Ballerina packages when migrating to Balelrina 2201.2.0 (Swan Lake). 

A few backward-incompatible changes have been introduced during the Swan Lake Beta program, and thereby, some of your existing packages may not compile with Ballerina 2201.2.0 (Swan Lake). Therefore, you need to delete the `Dependencies.toml` file to force the dependency resolver to use the latest versions of your dependencies. 

### Language Updates

#### New features

#### Improvements

#### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.2.0 (Swan Lake)](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FCompilerFE+milestone%3A%22Ballerina+2201.2.0%22).

### Runtime updates

#### New features

##### Strand dump

Allows getting the status of strands and strand groups during the execution of a Ballerina program.

This can be used to troubleshoot runtime errors. The Ballerina runtime will emit the strand dump to the standard output stream in the text format, if it receives a `SIGTRAP` signal (`SIGTRAP` is not available on Windows).

E.g., if the PID of the running Ballerina program is `$PID`, you can get the strand dump by executing either `kill -SIGTRAP $PID` or `kill -5 $PID` command.

##### `StopHandler` Object

Allows registering a function that will be called during graceful shutdown.

A call to `onGracefulStop` will result in one call to the handler function that was passed as an argument; the handler functions will be called after calling `gracefulStop` on all registered listeners, in the reverse order of the corresponding calls to `onGracefulStop`.

E.g., a `foo` function can be called during the graceful shutdown by registering it as follows.

`runtime:onGracefulStop(foo);`

#### Improvements

#### New runtime Java APIs

##### Type-reference type support at runtime

###### Modified existing runtime APIs

When a type is defined referring to another type, it will now be passed to the runtime as a `BTypeReferenceType` instance.

For example, the following code contains the `Integer` and `Student` type reference types.

```ballerina
type Integer int;

type Person record {|
    string name;
    Integer age;
|};

type Student Person;

```

The following runtime Java APIs are now supported to return the `BTypeReferenceType` instances.

```java
// from the `ArrayType`.
Type getElementType();

// from the `FunctionType`.
Parameter[] getParameters();
Type[] getParameterTypes();

// from the `Field`.
Type getFieldType();

// from the `BTypedesc`.
Type getDescribingType();
```

###### New runtime Java API

The follwing new runtime APIs are added to provide the referred type of a type reference type.  

- `TypeUtils.getReferredType()`
- `getReferredType()` in `ReferenceType`  

```ballerina
type Integer int;

type Quantity Integer;
```  

In the above example of the `Quantity` type,  
the `TypeUtils.getReferredType()` call will return the `int` type instance.  
The `getReferredType()` call on the `ReferenceType` will return another `BTypeReferenceType` instance with the `Integer` name.

#### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.2.0 (Swan Lake)](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+milestone%3A2201.2.0+label%3ATeam%2FjBallerina+label%3AType%2FBug+is%3Aclosed).

### Standard library updates

#### New features

##### `constraint` package

- Introduced the `constraint` standard library package, which provides features to validate the values that have been assigned to Ballerina types

##### `graphql` package

- Added the support for deprecation of fields and enum values
- Added the support for GraphQL interceptors

##### `serdes` package

- Introduced the `serdes` standard library package for serializing and deserializing Ballerina `anydata` subtypes
- Proto3 is the underlying technology used by this package to achieve serialization and deserialization

##### `os` Package
- Introduced the `exec()` function to support OS command execution in Ballerina

#### Improvements

##### `graphql` package

##### `random` Package
- Updated the `createDecimal()` function to be cryptographically secure

### Code to Cloud updates

#### Improvements
The base image was updated to `ballerina/jvm-runtime:1.0` based on Alpine 3.15 with the necessary libraries.

#### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.2.0 (Swan Lake)](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+2201.2.0%22+label%3AType%2FBug).

### Developer tools updates

#### New features

##### SemVer validator CLI tool (Experimental)
Introduced the `bal semver` CLI command, which attempts to validate <a href="https://semver.org/">Semantic Versioning</a> compatibility of the local package changes against any previously published version(s) in Ballerina Central. Currently, the tool can be used to: 
- list down the source code differences (along with its compatibility impact) between the local and any published versions in Ballerina central
- suggest the new package version based on the compatibility impact of source code changes

Refer to the examples below which demonstrate few key functionalities of the semver CLI tool.

- version suggestions
```
$bal semver             
checking for the latest compatible release version available in central...

current version: 1.2.2-SNAPSHOT
compatibility impact (compared with the release version '1.2.1'): backward-incompatible changes detected
suggested version: 2.0.0
```

- version suggestions with the list of source code changes
```
$bal semver --show-diff
checking for the latest compatible release version available in central...

=========================================================================
 Comparing version '1.2.2-SNAPSHOT'(local) with version '1.2.1'(central) 
=========================================================================
[+-] package 'io' is modified [version impact: MAJOR]
  [+-] module 'io' is modified [version impact: MAJOR]
    [++] function 'printlnNew' is added [version impact: MINOR]
    [+-] function 'println' is modified [version impact: MAJOR]
      [+-] documentation is modified [version impact: PATCH]
      [--] 'isolated' qualifier is removed [version impact: AMBIGUOUS]
      [++] 'transactional' qualifier is added [version impact: AMBIGUOUS]
      [++] new required parameter 'a' is added [version impact: MAJOR]
      [++] new defaultable parameter 'b' is added [version impact: MINOR]
      [+-] parameter type changed from 'Printable' to 'string' [version impact: AMBIGUOUS]
      [+-] function body is modified [version impact: PATCH]

current version: 1.2.2-SNAPSHOT
compatibility impact (compared with the release version '1.2.1'): backward-incompatible changes detected
suggested version: 2.0.0
```
##### CLI

Introduced the `bal graph` CLI command, which resolves the dependencies of the current package and prints the dependency graph in the console. This produces the textual representation of the dependency graph using the DOT graph description language.

```ballerina
$ bal graph
digraph "org/package:0.1.0" {
        node [shape=record]
        "org/package" [label="<0.1.0> org/package:0.1.0"];
        "ballerina/io" [label="<1.2.2> ballerina/io:1.2.2"];

        // Edges
        "org/package":"0.1.0" -> "ballerina/io":"1.2.2";
}
```

##### Ballerina Shell

##### Ballerina Update Tool

#### Improvements

##### Ballerina shell

##### Ballerina update Tool

#### Bug fixes

### Breaking changes

### Developer tools updates

#### New features

##### OpenAPI Tool
Added support for generating client resource methods in the client generation command. The preferred client method type can be chosen using the `--client-methods=<remote(default)|resource>` option.
  - `$ bal openapi -i <OpenAPI contract> --client-methods=resource`
  - `$ bal openapi -i <OpenAPI contract> --mode client --client-methods=resource`

#### Improvements

##### OpenAPI Tool
Added support for OpenAPI schema constraint properties in client/service generation. With this improvement, the OpenAPI constraints will be applied as `ballerina/constraint` standard library package annotations when generating Ballerina clients and services from the OpenAPI definition.
The following OpenAPI properties are currently supported in the Ballerina OpenAPI generation tool. 
- `minimum`, `maximum`, `exclusiveMinimum`, and `exclusiveMaximum` for `integer` and `number` types
- `minLength` and `maxLength` for `string` type
- `minItems` and `maxItems` for `array` type

To view bug fixes, see the GitHub milestone for 2201.2.0 (Swan Lake) of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+milestone%3A%22Ballerina+2201.2.0%22+is%3Aclosed+label%3ATeam%2FLanguageServer)
- [update tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+milestone%3A%22Ballerina+2201.2.0%22+is%3Aclosed+label%3AType%2FBug)


### Ballerina packages updates

#### New features

Introduced an `include` field under the `[package]` table in `Ballerina.toml`. It accepts a string array of paths to any additional files and directories, which need to be packed in the BALA file. The path should be relative to the package root directory.

```ballerina
[package]
org = "samjs"
name = "winery"
version = "0.1.0"
include = [documents/”, "images/sample.png"]
```

<!-- <style>.cGitButtonContainer, .cBallerinaTocContainer {display:none;}</style> -->
