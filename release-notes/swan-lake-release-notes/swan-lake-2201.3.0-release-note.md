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

### Improvements

### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.x.0 (Swan Lake)](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FCompilerFE+milestone%3A%22Ballerina+2201.3.0%22).

## Runtime updates

### New features

### Improvements

### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.0.0 (Swan Lake)](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FjBallerina+milestone%3A%22Ballerina+2201.3.0%22).

## Standard library updates

### New features

#### `graphql` package

- Added support for disabling introspection queries
- Added support for GraphQL interfaces
- Added support for interfaces implementing interfaces
- Introduced GraphQL client configurations

### Improvements

#### `graphql` package

- Added service-level interceptor execution for records fields, maps, and tables
- Added service-level interceptor execution for subscriptions
- Enabled returning all the errors related to a GraphQL document in a single response

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
