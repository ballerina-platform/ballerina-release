---
layout: ballerina-left-nav-release-notes
title: 2201.3.0 (Swan Lake) 
permalink: /downloads/swan-lake-release-notes/2201-3-0/
active: 2201-3-0
redirect_from: 
    - /downloads/swan-lake-release-notes/2201-3-0
    - /downloads/swan-lake-release-notes/2201.3.0/
    - /downloads/swan-lake-release-notes/2201-3-0-swan-lake/
    - /downloads/swan-lake-release-notes/2201-3-0-swan-lake
---

## Overview of Ballerina Swan Lake 2201-3-0

<em>2201.3.0 (Swan Lake) is the third major release of 2022, and it includes a new set of features and significant improvements to the compiler, runtime, standard library, and developer tooling. It is based on the 2022R3 version of the Language Specification.</em> 

## Update Ballerina

**If you are already using Ballerina 2201.0.0 (Swan Lake)**, run either of the commands below to directly update to 2201-3-0 using the [Ballerina Update Tool](/learn/cli-documentation/update-tool/).

`bal dist update` (or `bal dist pull 2201-3-0`)

**If you are using a version below 2201.0.0 (Swan Lake)**, run the commands below to update to 2201-3-0.

1. Run `bal update` to get the latest version of the Update Tool.

2. Run `bal dist update` ( or `bal dist pull 2201-3-0`) to update your Ballerina version to 2201-3-0.

However, if you are using a version below 2201.0.0 (Swan Lake) and if you already ran `bal dist update` (or `bal dist pull 2201-3-0`) before `bal update`, see [Troubleshooting](/downloads/swan-lake-release-notes/2201-0-0-swan-lake/#troubleshooting) to recover your installation.

## Install Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

## Language updates

### New features


#### Added a new field to the `display` annotation

A new field named `kind` has been introduced to the `display` annotation to indicate the kind of the data. Allowed values are "text", "password", and "file".

```ballerina
public type RefreshTokenGrantConfig record {|
    @display {
        iconPath: "Field.icon",
        label: "clientSecret field",
        kind: "password"
    }
    string clientSecret;
|};
```

#### Added support for function pointers with defaultable parameters

Function pointers are now allowed with default values for parameters. Any expression can be used as the default value of a function pointer parameter.

```ballerina
import ballerina/io;

public function main() {
    int num1 = 100;
    int num2 = 50;
    int num3 = 25;
    function (int a = 0, int b = 0, int c = 0) returns int total = getSum;

    io:println(total()); // Prints `0`.
    io:println(total(num1, num2)); // Prints `150`.
    io:println(total(num1, num2, num3)); // Prints `175`.
}

function getSum(int num1, int num2, int num3) returns int {
    return num1 + num2 + num3;
}
```

### Improvements

#### More improvements on working with optional fields

If there is an optional field `T x?;` in a record, the absence of `x` is represented by nil where `T` does not allow nil.

```ballerina
import ballerina/io;

type Employee record {
    int id?;
    string department?;
};

public function main() {
    Employee e = {id: 2, department: "HR"};
    e.id = ();
    e = {id: 3};
    var {id: _, department} = e;
    io:println(department is ()); // true

    int? idOrNil = ();
    e = {id: idOrNil, department: "Engineering"};
    io:println(e.id is ()); // true
}

```

#### Allow an optional terminating semicolon for module-level declarations
Previously, a closing semicolon was not allowed after the module-level declarations below.
- block function body
- service declaration
- module class definition
- module enumeration declaration 

Now, you can optionally end these declarations with a semicolon.


### Backward-incompatible changes

#### Disallow using the `-9223372036854775808` unary expression as an integer

Previously, `-9223372036854775808` was allowed to be assigned to an integer in Ballerina. However, according to the language specification, `-9223372036854775808` is considered as a unary expression, which requires the expression  after `-` to be a valid value for `int`. Therefore, `-9223372036854775808` now results in a compilation error since `9223372036854775808` is out of range for `int`.

```
int result = -9223372036854775808; // error: '9223372036854775808' is out of range for 'int'
```

## Compiler API updates

### New features

#### Semantic API
- Added a new `annotAttachments()` API to get the annotation attachments and their constant values from the annotatable symbols
- Introduced a new `ClientDeclSymbol` symbol to represent the semantic information of the client-declaration statement

### Improvements

#### Semantic API
- Improved the `constValue()` method to retrieve the constant value as an object from the constant symbol

#### Syntax API
- Added a few methods to the `NodeParser` API. The following methods have been introduced for the `NodeParser` class.
  - `Node parseObjectMember(String text)`
  - `ModulePartNode parseModulePart(String text)`
  - `IntermediateClauseNode parseIntermediateClause(String text, boolean allowActions)`

### Backward-incompatible changes
- Updated NodeFactory methods to allow optional terminating semicolon for module-level declarations. The methods below in the `NodeFactory` have been updated with an extra parameter for the optional semicolon token.
  - `createServiceDeclarationNode`
  - `createFunctionBodyBlockNode`
  - `createEnumDeclarationNode`
  - `createClassDefinitionNode`

### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.3.0 (Swan Lake)](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+milestone%3A2201.3.0+label%3ATeam%2FCompilerFETools+label%3AType%2FBug+).

## Runtime updates

### New features

### Improvements

### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.0.0 (Swan Lake)](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FjBallerina+milestone%3A%22Ballerina+2201.3.0%22).

## Standard library updates

### New features

#### `graphql` package

#### `gRPC` package
- Added server reflection support for gRPC services

### Improvements

#### `graphql` package

#### `gRPC` package
- Updated Protocol Buffers version to 3.21.7

## Code to Cloud updates

### New features

### Improvements

### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.x.0 (Swan Lake)](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+2201.3.0%22+label%3AType%2FBug).

## Developer tools updates

### New features

#### Ballerina Shell

#### Ballerina Update Tool

### Improvements

#### Ballerina shell

#### Ballerina update Tool

### Bug fixes

## Package updates

### New features

### Improvements

### Bug fixes

## Breaking changes

To view bug fixes, see the GitHub milestone for 2201.3.0 (Swan Lake) of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+milestone%3A%22Ballerina+2201.3.0%22+is%3Aclosed+label%3ATeam%2FLanguageServer)
- [update tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+milestone%3A%22Ballerina+2201.3.0%22+is%3Aclosed+label%3AType%2FBug)
- [OpenAPI](https://github.com/ballerina-platform/openapi-tools/issues?q=is%3Aissue+label%3AType%2FBug+milestone%3A%22Ballerina+2201.3.0%22+is%3Aclosed)
