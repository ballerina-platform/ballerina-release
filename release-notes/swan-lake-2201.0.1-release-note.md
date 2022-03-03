---
layout: ballerina-left-nav-release-notes
title: 2201.0.1 (Swan Lake) 
permalink: /downloads/swan-lake-release-notes/2201-0-1-swan-lake/
active: 2201-0-1-swan-lake
redirect_from: 
    - /downloads/swan-lake-release-notes/2201-0-1-swan-lake
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---

## Overview of Ballerina Swan Lake 2201.0.1

<em>Swan Lake 2201.0.1 is the first patch release of Ballerina 2201.0.0 (Swan Lake) and it includes a new set of bug fixes to the compiler, runtime, standard library, and developer tooling.</em> 

## Updating Ballerina

**If you are already using Ballerina 2201.0.0 (Swan Lake)**, run either of the commands below to directly update to 2201.0.1 using the [Ballerina Update Tool](/learn/cli-documentation/update-tool/) to directly update to 2201.0.1 (Swan Lake).

`bal dist update (or bal dist pull 2201.0.1)`

**If you are using a version below 2201.0.0 (Swan Lake)**, run the commands below to update to 2201.0.1 (Swan Lake).

1. Run `bal update` to get the latest version of the Update Tool.

2. Run `bal dist update` (or `bal dist pull 2201.0.1`) to update your Ballerina version to 2201.0.1 (Swan Lake).

However, **if you are using a version below 2201.0.0 (Swan Lake) and if you already ran `bal dist update` (or `bal dist pull 2201.0.1`) before `bal update`, see [Updating Ballerina](/downloads/swan-lake-release-notes/2201-0-1-swan-lake/#troubleshooting) to recover your installation.

### Troubleshooting 

If you already ran the `bal dist update` (or `bal dist pull 2201.0.0`) before the `bal update` command, follow the instructions below to recover your installation.

#### For macOS Users (`.pkg` installations)

1. Run the `rm ~/.ballerina/ballerina-version` command to delete the version configuration.
2. Run the `chmod 755 /Library/Ballerina/distributions/ballerina-2201.0.0/bin/bal` command to provide execute permissions for the `bal` command.
3. Run the `bal dist use 2201.0.0` command to switch to the 2201.0.0 version. 

#### For Ubuntu Users (`.deb` installations)

1. Run the `rm ~/.ballerina/ballerina-version` command to delete the version configuration.
2. Run the `chmod 755 /usr/lib/ballerina/distributions/ballerina-2201.0.0/bin/bal` command to provide execute permissions for the `bal` command.
3. Run the `bal dist use 2201.0.0` command to switch to the 2201.0.0 version.

#### For CentOS Users (`.rpm` installations)

1. Run the `rm ~/.ballerina/ballerina-version` command to delete the version configuration.
2. Run the `chmod 755 /usr/lib64/ballerina/distributions/ballerina-2201.0.0/bin/bal` command to provide execute permissions for the `bal` command.
3. Run the `bal dist use 2201.0.0` command to switch to the 2201.0.0 version.

#### For Windows Users (`.msi` installations)

1. Run the `del %userprofile%\.ballerina\ballerina-version` command to delete the version configuration.
2. Run the `bal dist use 2201.0.0` command to switch to the 2201.0.0 version.

## Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

## Migrating from Swan Lake Beta Releases

>**Info:** If you have been using Swan Lake Beta releases, delete the `Dependencies.toml` files in your Ballerina packages when migrating to Balelrina 2201.0.0 (Swan Lake). 

A few backward-incompatible changes have been introduced during the Swan Lake Beta program, and thereby, some of your existing packages may not compile with Ballerina 2201.0.0 (Swan Lake). Therefore, you need to delete the `Dependencies.toml` file to force the dependency resolver to use the latest versions of your dependencies. 

## Language Updates

### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.0.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

## Runtime Updates

### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.0.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

## Standard Library Updates

### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.0.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+2201.0.0%22+label%3AType%2FBug).

## Code to Cloud Updates

### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.0.0 of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22)

## Developer Tools Updates

### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.0.0 of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FLanguageServer+milestone%3A%22Ballerina+Swan+Lake+GA%22)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22)

### Ballerina Packages Updates

### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.0.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+2201.0.0%22+label%3AType%2FBug).

## Breaking Changes

<style>.cGitButtonContainer, .cBallerinaTocContainer {display:none;}</style>
