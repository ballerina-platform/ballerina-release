---
layout: ballerina-left-nav-release-notes
title: 2201.x.0 (Swan Lake) 
permalink: /downloads/swan-lake-release-notes/2201-x-0/
active: 2201-x-0
redirect_from: 
    - /downloads/swan-lake-release-notes/2201-x-0
    - /downloads/swan-lake-release-notes/2201.x.0/
    - /downloads/swan-lake-release-notes/2201-x-0-swan-lake/
    - /downloads/swan-lake-release-notes/2201-x-0-swan-lake
---

### Overview of Ballerina 2201.x.0 (Swan Lake)

<em>2201.x.0 (Swan Lake) is the <first> major release of <2022>, and it includes a new set of features and significant improvements to the compiler, runtime, standard library, and developer tooling. It is based on the <2022R1> version of the Language Specification.</em> 

### Update Ballerina

>**Info:** The version format has been revised. `2201.x.0 (Swan Lake)` represents the format of `$YYMM.$UPDATE.$PATCH ($CODE_NAME)`. For further information, see [Ballerina Swan Lake is on the Horizon](https://blog.ballerina.io/posts/ballerina-swan-lake-is-on-the-horizon/).

If you are already using Ballerina, use the [Ballerina update tool](/learn/cli-documentation/update-tool/#using-the-update-tool) to directly update to 2201.x.0 (Swan Lake). To do this: 

1. Run the command below to get the latest version of the update tool.

   `bal update`

2. Run the command below to update your Ballerina version to 2201.x.0 (Swan Lake).

   `bal dist update`

#### Troubleshoot 

If you already ran the `bal dist update` (or `bal dist pull 2201.x.0`) before the `bal update` command, follow the instructions below to recover your installation.

##### For macOS Users (`.pkg` installations)

1. Run the `rm ~/.ballerina/ballerina-version` command to delete the version configuration.
2. Run the `chmod 755 /Library/Ballerina/distributions/ballerina-2201.x.0/bin/bal` command to provide execute permissions for the `bal` command.
3. Run the `bal dist use 2201.x.0` command to switch to the 2201.0.0 version. 

##### For Ubuntu Users (`.deb` installations)

1. Run the `rm ~/.ballerina/ballerina-version` command to delete the version configuration.
2. Run the `chmod 755 /usr/lib/ballerina/distributions/ballerina-2201.x.0/bin/bal` command to provide execute permissions for the `bal` command.
3. Run the `bal dist use 2201.x.0` command to switch to the 2201.0.0 version.

##### For CentOS Users (`.rpm` installations)

1. Run the `rm ~/.ballerina/ballerina-version` command to delete the version configuration.
2. Run the `chmod 755 /usr/lib64/ballerina/distributions/ballerina-2201.x.0/bin/bal` command to provide execute permissions for the `bal` command.
3. Run the `bal dist use 2201.x.0` command to switch to the 2201.0.0 version.

##### For Windows Users (`.msi` installations)

1. Run the `del %userprofile%\.ballerina\ballerina-version` command to delete the version configuration.
2. Run the `bal dist use 2201.x.0` command to switch to the 2201.0.0 version.

### Install Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Migrate from Swan Lake Beta releases
>**Info:** If you have been using Swan Lake Beta releases, delete the `Dependencies.toml` files in your Ballerina packages when migrating to Balelrina 2201.0.0 (Swan Lake). 

A few backward-incompatible changes have been introduced during the Swan Lake Beta program, and thereby, some of your existing packages may not compile with Ballerina 2201.0.0 (Swan Lake). Therefore, you need to delete the `Dependencies.toml` file to force the dependency resolver to use the latest versions of your dependencies. 

### Language Updates

#### New features

#### Improvements

#### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.x.0 (Swan Lake)](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FCompilerFE+milestone%3A%22Ballerina+2201.x.0%22).

### Runtime updates

#### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.0.0 (Swan Lake)](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FjBallerina+milestone%3A%22Ballerina+2201.x.0%22).

### Standard library updates

#### New features

##### `graphql` package

#### Improvements

##### `graphql` package


### Code to Cloud updates

#### Improvements

#### Bug fixes

To view bug fixes, see the [GitHub milestone for 2201.x.0 (Swan Lake)](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+2201.0.0%22+label%3AType%2FBug).

### Developer tools updates

#### New features

##### Ballerina Shell

##### Ballerina Update Tool

#### Improvements

##### Ballerina shell

##### Ballerina update Tool

#### Bug fixes

### Breaking changes

To view bug fixes, see the GitHub milestone for 2201.x.0 (Swan Lake) of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+milestone%3A%22Ballerina+2201.x.0%22+is%3Aclosed+label%3ATeam%2FLanguageServer)
- [update tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+milestone%3A%22Ballerina+2201.x.0%22+is%3Aclosed+label%3AType%2FBug)
- [OpenAPI](https://github.com/ballerina-platform/openapi-tools/issues?q=is%3Aissue+label%3AType%2FBug+milestone%3A%22Ballerina+2201.x.0%22+is%3Aclosed)

<!-- <style>.cGitButtonContainer, .cBallerinaTocContainer {display:none;}</style> -->