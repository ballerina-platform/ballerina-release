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

#### Improvements

- Worker deadlock detection has been improved to include the `wait` action.
- `self` of an isolated object no longer needs to be accessed within a `lock` statement unless it is used to access a field that is either not `final` or is not a subtype of `readonly` or `isolated object`.
- `xml:strip()` does not mutate the XML value, thus using `xml:strip()` on immutable XML values is allowed.

#### Breaking Changes

- An included record parameter of a function can only be specified after any required and/or defaultable parameters of the function.
- Additive expressions and multiplicative expressions are no longer supported with numeric values when the static types of the operands belong to different numeric basic types.
- Configurable variables are implicitly `final` now. Moreover, the type of such a variable is now effectively the intersection of the specified type and `readonly`. Therefore configurable variables no longer support the `final` and `isolated` qualifiers.
- Type narrowing will no longer take place for captured variables of an anonymous function, since the narrowed type cannot be guaranteed during the execution of the function.
- Type narrowing will now be reset after a compound assignment.
- Worker message passing after waiting for the same worker has been disallowed.
- When a named worker is used in a `wait` action, it can no longer be used in a variable reference anywhere else.
- When the `type-descriptor` is ambiguous, it is considered according to the following table, in which the type precedence is presented in the decreasing order.
  
  For example, `A & B | C` is considered to be `(A & B) | C`.
  
  | Operator                  | Associativity |
  |---------------------------|---------------|
  | distinct T                |               |
  | T[ ]                      |               |
  | T1 & T2                   | left          |
  | T1 &#124; T2              | left          |
  | function (args) returns T | right         |

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta1](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta1%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

#### Breaking Changes

- `io.ballerina.runtime.api.types.Type#getName` and `io.ballerina.runtime.api.types.Type#getQualifiedName` now returns an empty string if no name was associated with the type. The `io.ballerina.runtime.api.types.Type#toString` method can be used to get the string representation of a type if required.
- Wait actions that wait for expressions that are not named workers can return errors now. The eventual type of such wait future expressions is now `T|error`, `T` being the type of the original return value.


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

##### `graphql` Package
- Improved introspection validation and execution
- Added missing fields in the GraphQL types
- Compiler plugin improvements to validate inputs and return types
- Use included record parameters instead of the record type in the listener initialization

##### `http` Package
- Improve the `http:Client` remote methods to support the contextually-expected type inference
- Change the configuration parameters of the listeners and clients to include the record parameters

##### `websubhub` Package
- Include the auth configuration to the WebSubHub publisher client configuration

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta1](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Beta1%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features

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

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake Beta1 of the repositories below.

- [Language](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta1%22+label%3AType%2FBug+label%3ATeam%2FDevTools)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta%22) 

#### Ballerina Packages Updates

### Breaking Changes
