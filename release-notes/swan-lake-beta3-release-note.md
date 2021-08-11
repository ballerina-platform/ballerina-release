---
layout: ballerina-left-nav-release-notes
title: Swan Lake Beta3
permalink: /downloads/swan-lake-release-notes/swan-lake-beta3/
active: swan-lake-beta3
redirect_from: 
    - /downloads/swan-lake-release-notes/swan-lake-beta3
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---
### Overview of Ballerina Swan Lake Beta3

<em>This is the third beta release leading up to the Ballerina Swan Lake GA release.</em> 

It introduces the new language features planned for the Swan Lake GA release and includes improvements and bug fixes done to the compiler, runtime, standard library, and developer tooling after the Swan Lake Beta2 release.

### Updating Ballerina

If you are already using Ballerina, you can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Ballerina Swan Lake Beta3 as follows. 

To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake <VERSION>.

> `bal dist pull slbeta3`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Beta3%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22).

### Developer Tools Updates

#### New Features

##### Ballerina OpenAPI Tool
- Introduced a new command-line option to generate all the record fields that are not specifically mentioned as 
  `nullable:false` in the OpenAPI schema property as nullable to reduce the type conversion errors in the OpenAPI to
  Ballerina command
  >`bal openapi -i <openapi-contract-file>  --nullable`
- Introduced a new command-line option to add user-required license or copyright headers for the generated Ballerina
  files via OpenAPI to Ballerina command
  >`bal openapi -i <openapi-contract-file> --license <license-file> `
- Introduced a new command-line option to generate the JSON file via the Ballerina to OpenAPI command
  >`bal openapi -i <service-file> --json`
- Added support to generate a boilerplate of test functions for each remote function implemented within a
  client connector  
  
#### Improvements
##### Ballerina OpenAPI Tool
###### Ballerina OpenAPI client and schema generation improvements for the OpenAPI to Ballerina command
- Added support to generate suitable client connector authentication mechanisms by mapping the security schemes
  given in the OpenAPI specification (OAS)
- Added support to generate API documentation for the client init method, remote functions and records
- Added support to facilitate users to set common client configurations when initializing the connector 
- Added support to generate records for nested referenced schemas in the OpenAPI specification 
- Improved the OpenAPI tool to select `https` server URL when multiple URLs are given in the OpenAPI specification
 
###### The Ballerina to OpenAPI command improvements
- Added support for language server extension 
- Improved the response status code map to `202` when the resource function does not have `return` type
- Improved mapping different status code response in the resource function
- Enhanced generating openAPI schema with Ballerina `typeInclusion` scenarios
- Added resource function API documentation mapping to the OAS description and summary
- Improved resource function request payload mapping with OAS requestBody   
 
#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake Beta2 of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug+label%3ATeam%2FLanguageServer)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug)
- [Debugger](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+label%3AType%2FBug+label%3AArea%2FDebugger+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta2%22)
- [Test Framework](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+label%3ATeam%2FTestFramework+milestone%3A%22Ballerina+Swan+Lake+-+Beta2%22+label%3AType%2FBug+)

#### Ballerina Packages Updates

### Breaking Changes
