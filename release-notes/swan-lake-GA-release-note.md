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

##### `http` Package

- Implemented typed `headers` for the HTTP response
- Added the `map<string>` data binding support for `application/www-x-form-urlencoded`
- Added support to provide an inline request/response body with `x-form-urlencoded` content
- Added compiler validation for the payload annotation usage

#### Improvements

##### `grpc` Package
- Changed the `--proto_path` option of the gRPC CLI to `--proto-path`

##### `websub` Package
- Added the support for `readonly` parameters of remote methods

#### `websubhub` Package
- Added the support for `readonly` parameters of remote methods

##### `kafka` Package
- Made the `kafka:Caller` optional in the `onConsumerRecord` method of the `kafka:Service`
- Allow the `readonly & kafka:ConsumerRecord[]` parameter type in the `onConsumerRecord` method

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

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.0.0 of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FLanguageServer+milestone%3A%22Ballerina+Swan+Lake+GA%22)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22)

#### Ballerina Packages Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.0.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+2201.0.0%22+label%3AType%2FBug).

### Breaking Changes

<style>.cGitButtonContainer, .cBallerinaTocContainer {display:none;}</style>