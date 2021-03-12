---
layout: ballerina-blank-page
title: Release Note
---
### Overview of Ballerina Swan Lake <VERSION>

This <VERSION> release includes the language features planned for the Ballerina Swan Lake release. Moreover, this release includes improvements and bug fixes to the language, runtime, standard library, code to cloud, and developer tooling. This release note lists only the features and updates added after the <VERSION> release of Ballerina Swan Lake.

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

##### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Alpha3%22+label%3AType%2FBug).

#### Code to Cloud

##### Bug Fixes

To view bug fixes, see the Github issues on [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F76+), [Docker](https://github.com/ballerina-platform/module-ballerina-docker/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F76), [AWS Lambda](https://github.com/ballerina-platform/module-ballerinax-aws.lambda/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F76), and [Azure Functions](https://github.com/ballerina-platform/module-ballerinax-azure.functions/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F76) repos.

#### Developer Tools

##### Bug Fixes

To view bug fixes, see the Github milestone issues on the [Lang](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha3%22+label%3AType%2FBug+label%3ATeam%2FDevTools), [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32), [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha%22) repos.

#### Breaking Changes
