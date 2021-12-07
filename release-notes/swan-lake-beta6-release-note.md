---
layout: ballerina-left-nav-release-notes
title: Swan Lake Beta6
permalink: /downloads/swan-lake-release-notes/swan-lake-beta6/
active: swan-lake-beta5
redirect_from: 
    - /downloads/swan-lake-release-notes/swan-lake-beta6
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---

### Overview of Ballerina Swan Lake Beta6

<em>This is the sixth Beta release in a series of planned Alpha and Beta releases leading up to the Ballerina Swan Lake GA release.</em> 

The Ballerina Swan Lake Beta6 release improves upon the Beta5 release by addressing a few [Language issues](https://github.com/ballerina-platform/ballerina-lang/milestone/119).

### Updating Ballerina

If you are already using Ballerina, you can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Ballerina Swan Lake Beta6 as follows. 

To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake Beta5.

> `bal dist pull slbeta6`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

#### Improvements

#### Bug Fixes and Breaking Changes

- The resulting type of the `unary` plus expression has been changed to the same static type of the operand.
```ballerina
// the following are now allowed

public function main() {
    int:Unsigned8 a = 32;
    a = +a;

    int:Unsigned16 b = 43;
    b = +b;

    int:Unsigned32 c = 54;
    c = +c;

    byte d = 127;
    d = +d;

    int:Signed8 e = 32;
    e = +e;

    int:Signed16 f = 65;
    f = +f;

    int:Signed32 g = 64;
    g = +g;
}
```


### Standard Library Updates

#### New Features

##### GraphQL Package
- added support for GraphQL list type inputs

##### HTTP Package
- Introduced request and request error interceptors at service level

#### Improvements

##### HTTP Package
- Changed `RequestContext:add` function to `RequestContext:set`
- Allowed listener level interceptors to have only the default path
- Improved `parseHeader()` function to support multiple header values

<style>.cGitButtonContainer, .cBallerinaTocContainer {display:none;}</style>

#### Improvements
##### Ballerina OpenAPI Tools
###### Ballerina OpenAPI client generation improvements for the OpenAPI to Ballerina command
- Add the flag `--with-tests` for openAPI client generation command to generate test boiler plates file to relevant
  remote functions.
  > `bal openapi -i <openapi contract> --mode client --with-test`

###### The Ballerina to OpenAPI command improvements
- Add support to generate openAPI contract files for all the services in the current package by introducing 
  new flag `--export-openapi` to `bal build` command.
  > `bal build --export-openapi`
