---
layout: ballerina-left-nav-release-notes
title: Swan Lake 2201.0.0
permalink: /downloads/swan-lake-release-notes/swan-lake-2201.0.0/
active: swan-lake-2201.0.0
redirect_from: 
    - /downloads/swan-lake-release-notes/swan-lake-2201.0.0
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---

### Overview of Ballerina Swan Lake 2201.0.0

<em>Swan Lake 2201.0.0 is the first major release of 2021 and it includes a new set of features and significant improvements to the compiler, runtime, standard library, and developer tooling. It is based on the 2021R1 version of the Language Specification.</em> 

### Updating Ballerina

If you are already using Ballerina, use the [Ballerina Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Swan Lake Beta6 by running the command below.

> `bal dist pull 2201.0.0`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.0.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.0.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.0.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+2201.0.0%22+label%3AType%2FBug).


### Code to Cloud Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.0.0 of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22)
- [Docker](https://github.com/ballerina-platform/module-ballerina-docker/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22)
- [AWS Lambda](https://github.com/ballerina-platform/module-ballerinax-aws.lambda/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22)
- [Azure Functions](https://github.com/ballerina-platform/module-ballerinax-azure.functions/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22) 

### Developer Tools Updates

#### New Features

##### Ballerina Shell

- Added the module auto-import feature to the Ballerina Shell
- Added the import statement for a module, which has a reference without an import statement based on the user’s input

```ballerina
For example, see below.

=$ io:println("HelloWorld")
|
| Found following undefined module(s).
| io
|
| Following undefined modules can be imported.
| 1. io
Do you want to import mentioned modules (yes/y) (no/n)? y
|
| Adding import: import ballerina/io
| Import added: import ballerina/io

HelloWorld
```

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.0.0 of the repositories below.

- [Language](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22+label%3AType%2FBug+label%3ATeam%2FDevTools)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22)

#### Ballerina Packages Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.0.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+2201.0.0%22+label%3AType%2FBug).

### Breaking Changes

<style>.cGitButtonContainer, .cBallerinaTocContainer {display:none;}</style>