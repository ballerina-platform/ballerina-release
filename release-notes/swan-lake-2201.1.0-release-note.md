---
layout: ballerina-left-nav-release-notes
title: Swan Lake 2201.1.0
permalink: /downloads/swan-lake-release-notes/2201.1.0/
active: swan-lake-2201.1.0
redirect_from: 
    - /downloads/swan-lake-release-notes/2201-1-0
    - /downloads/swan-lake-release-notes/2201-1-0-swan-lake/
    - /downloads/swan-lake-release-notes/2201-1-0-swan-lake
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---

### Overview of Ballerina Swan Lake 2201.1.0 (Swan Lake)

<em>2201.1.0 (Swan Lake) is the first update of 2201.1.0 (Swan Lake), and it includes a new set of features and significant improvements to the compiler, runtime, standard library, and developer tooling. It is based on the 2022R2 version of the Language Specification.</em> 


### Updating Ballerina

If you are already using Ballerina, use the [Ballerina Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Swan Lake Beta6 by running the command below.

> `bal dist pull 2201.1.0`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.0.0%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.1.0%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

##### `http` Package

- Introduced `ResponseInterceptor` and `ResponseErrorInterceptor`
- Introduced `DefaultErrorInterceptor`
- Added code-actions to generate the interceptor method template
- Allowed records to be annotated with `@http:Header`
- Added basic type support for header parameters in addition to `string` and `string[]`
- Added `anydata` support for service and client data binding
- Added common constants for HTTP status-code responses

##### `websocket` Package

- Introduced the `writeMessage` client and caller APIs
- Introduced the `onMessage` remote function for services
- Added `anydata` data binding support for the `writeMessage` API and `onMessage` remote function

##### `graphql` Package

- Added the support for GraphQL `subscriptions`
- Added the support for GraphQL `interfaces`
- Added the support for GraphQL `documentation`
- Added the `GraphiQL client` support for GraphQL services

##### `websub` Package

- Add code-actions to generate a `websub:SubscriberService` template

#### Improvements

##### `http` Package

- Allowed `Caller` to respond an `error` or a `StatusCodeResponse`
- Appended the HTTPS scheme (`https://`) to the client URL if security is enabled
- Refactored the auth-desugar response with a `DefaultErrorInterceptor`
- Hid the subtypes of the `http:Client`

##### `jwt` Package

- Appended the HTTPS scheme (`https://`) to the client URL (of JWKs endpoint) if security is enabled

##### `oauth2` Package

- Appended the HTTPS scheme (`https://`) to the client URL (of token endpoint or introspection endpoint) if security is enabled

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%222201.1.0%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.1.0 of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.1.0%22)

### Developer Tools Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.1.0 of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FLanguageServer+milestone%3A%22Ballerina+Swan+Lake+2201.1.0%22)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.1.0%22)

#### Ballerina Packages Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+2201.1.0%22+label%3AType%2FBug).

### Breaking Changes

<style>.cGitButtonContainer, .cBallerinaTocContainer {display:none;}</style>
