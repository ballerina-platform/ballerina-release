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

##### Spread operator support for list constructor expressions

Spread operator support for the list constructor expression has been introduced.

If the spread operator in a list constructor expression is `...x`, then `x` is expected to be a list (i.e., an array or a tuple). All the member values of the list that result from evaluating `x` are included in the list value being constructed.

```ballerina
import ballerina/io;

public function fn() {
    int[] a1 = [3, 4];
    int[] v1 = [1, 2, ... a1];
    io:println(v1); // [1, 2, 3, 4]

    int[2] a2 = [6, 7];
    int[] v2 = [1, 2, ... a1, 5, ... a2];
    io:println(v2); // [1, 2, 3, 4, 5, 6, 7]

    [int, string] t1 = [5, "s"];
    any[] v3 = [ ... t1, "x"];
    io:println(v3); // [5, "s", "x"]

    [boolean, int...] t2 = [false, 4, 7];
    [string, int, string, boolean, int...] v4 = ["x", ... t1, ... t2];
    io:println(v4); // ["x", 5, "s", false, 4, 7];

    var v5 = [4, ... t1, ... a2];
    io:println(v5); // [4, 5, "s", 6, 7];
}
```

The spread operator is not allowed with a varying-length list if the inherent type of the list being constructed has required members that are not guaranteed to have been provided a value.

```ballerina
public function fn() {
    [int, string...] t1 = [5, "s"];
    [int, string, string...] v1 = [ ... t1]; // results in an error since a value is not guaranteed to have been provided for the second tuple member

    [int, boolean, string, int...] t2 = [5, false, "w"];
    [int, boolean, anydata...] v2 = [ ... t2, "x", "y"]; // works as all fixed tuple members are guaranteed to have been provided values
}
```

##### Allow int*float, float*int, int* decimal, decimal*int, float/int, decimal/int, float%int and decimal%int.

Multiplicative expressions are now allowed with `int` and `float` or `int` and `decimal` operands.  The type of the result will be the fractional type.

The following have been allowed.
- for multiplication we support both `int*float` and `float*int` and similarly `int*decimal` and `decimal*int`.
- for division and modulo, only the floating-point operand as the dividend is supported i.e., `float/int`, `decimal/int`, `float%int`, and `decimal%int` are supported.

```ballerina
import ballerina/io;

public function main() {
    int a = 5;
    float b = 2.5;
    decimal c = 1.25;

    float e = a * b;
    io:println(e); // 12.5
    float f = b * a;
    io:println(f); // 12.5

    decimal g = a * c;
    io:println(g); // 6.250
    decimal h = c * a;
    io:println(h); // 6.250

    float j = b / a;
    io:println(j); // 0.5
    decimal k = c / a;
    io:println(k); // 0.25

    float m = b % a;
    io:println(m); // 2.5
    decimal n = c % a;
    io:println(n); // 1.25
}
```

##### New lang library functions

###### New `lang.array:some()` and `lang.array:every()` functions

The `lang.array:some()` function tests whether a function returns `true` for some member of an array. The function `lang.array:every` function tests whether a function returns `true` for every member of an array. 

```ballerina
import ballerina/io;

function func1(int i) returns boolean {
    return i > 2;
}

public function fn() {
    io:println([1, 3].some(func1)); // true
    io:println([1, -3].some(func1)); // false
    io:println([5, 3].every(func1)); // true
    io:println([1, 3].every(func1)); // false
}
```
###### New `lang.decimal:quantize()` function

The `lang.decimal:quantize()` function has been introduced to control the precision of decimal values. This results in a value equal to the first operand after rounding it to have the exponent of the second operand.

```ballerina
import ballerina/io;

public function main() {
    io:println(decimal:quantize(123.123, 1.0)); // 123.1
    io:println(decimal:quantize(123.123, 1.00)); // 123.12
    io:println(decimal:quantize(123.123, 1.000)); // 123.123
}
```
If the length of the coefficient after the quantize operation would be greater than the precision, the function results in a panic.

```ballerina
public function main() {
    decimal _ = decimal:quantize(123.1233, 1E-36); // results in a panic
}
```

###### New `lang.float:toFixedString()` and `lang.float:toExpString()` functions

Two new functions namely `lang.float:toFixedString()` and `lang.float:toExpString()` have been introduced to get the string representation of a `float` value in fixed-point notation and scientific notation respectively. Both the functions allow you to specify the number of digits required after the decimal point.

```ballerina
import ballerina/io;

public function main() {
    string a = float:toFixedString(5.7, 16); 
    io:println(a); // 5.7000000000000002
    string b = float:toFixedString(5.7, 2); 
    io:println(b); // 5.70
    
    float f1 = -45362.12334;
    string c = float:toExpString(f1, 16); 
    io:println(c); // -4.5362123339999998e+4
    string d = float:toExpString(f1, 2); 
    io:println(d); // -4.54e+4
}
```

###### New `lang.string:padStart()`, `lang.string:padEnd()`, and `lang.string:padZero()` functions

The `lang.string:padStart()`, `lang.string:padEnd()`, and `lang.string:padZero()` functions have been introduced to add padding in strings. `lang.string:padStart()` adds padding to the start of a string. `lang.string:padEnd()` adds padding to the end of a string. `lang.string:padZero()` pads a string with zeros.

```ballerina
public function main() {
    io:println("abc".padStart(5, "#")); // "##abc"
    io:println("abc".padStart(5)); // "  abc"

    io:println("abc".padEnd(5, "#")); // "abc##"
    io:println("abc".padEnd(5)); // "abc  "

    io:println("123".padZero(5)); // "00123"
    io:println("123".padZero(5, "#")); // "##123"
}
```

#### Improvements

##### Disallow inferring array length in contexts that are not permitted

Inferring array length has been restricted to list constructors in variable and constant declarations. Moreover, only the first dimension can be inferred in multidimensional arrays.

```ballerina
int[*] x1 = [1, 2]; // Supported.

int[2] y = [1, 2];
int[*] x2 = y; // Not supported. Requires a list constructor to infer the array length.

int[*][2] x3 = [[1, 2], [1, 2]]; // Supported.
int[*][*] x4 = [[1, 2], [1, 2]]; // Not supported. Only the first dimension can be inferred.
```

##### Add annotation attachments to the BIR



##### Revamped `lang.float:round` langlib function

The function signature has been changed to have an extra argument `fractionDigits`, where the user can choose the number of fraction digits of the rounded result. When `fractionDigits` is zero, the function rounds to an integer.

```ballerina
import ballerina/io;
import ballerina/lang.'float as floats;

public function main() {
    float x = 555.545;
    float y = 5.5565;
    int fractionDigits = 3;

    io:println(555.545.round(1));                     // 555.5
    io:println(555.545.round(2));                     // 555.54
    io:println(floats:round(x));                      // 556.0
    io:println(floats:round(x, fractionDigits = 0));  // 556.0
    io:println(floats:round(x, 1));                   // 555.5
    io:println(y.round(2));                           // 5.56
    io:println(y.round(fractionDigits));              // 5.556
}
```

##### `lang.decimal:round` method signature is improved

The function signature has been changed to have an extra argument `fractionDigits`, where the user can choose the number of fraction digits of the rounded result. When `fractionDigits` is zero, the function rounds to an integer.

```ballerina
import ballerina/io;
import ballerina/lang.'decimal as decimals;

public function main() {
    decimal x = 555.545;
    decimal y = 5.5565;
    int fractionDigits = 3;

    io:println(555.545.round(1));                      // 555.6
    io:println(decimals:round(x));                     // 556
    io:println(decimals:round(x, fractionDigits = 0)); // 556
    io:println(decimals:round(x, 1));                  // 555.6
    io:println(y.round(2));                            // 5.56
    io:println(y.round(fractionDigits));               // 5.556
}
```

##### An unreachable panic statement no longer results in a compilation error

```ballerina
function fn() returns string {
    int|string a = 10;

    if a is int {
        return "INT";
    } else {
        return "STRING";
    }

    panic error("Not Reached!"); // unreachable, but not an error.
}
```

#### Bug Fixes

- An invalid sub-typing relationship between `table` and `anydata` has been fixed.

```ballerina
public function main() {
    table<map<any>> tany = table [{"a": 2}];
    anydata ad = tany; // Results in a compilation error.
}
```

- A union containing the `null` literal allowing `"null"` as a valid value has been fixed.

```ballerina
type Foo boolean|null;

public function main() {
    Foo a = "null"; // compilation error
    "string"|null b = "null"; // compilation error
}
```

- An issue that caused the value of enum members defined with quoted identifiers to include the quote has been fixed.

```ballerina
import ballerina/io;

public enum Status {
    'new,
    old
}
public function main() {
    io:println('new); // Previously printed `'new`, now prints `new`.
}
```


- A compilation error is now logged when there is an extra comma inside a mapping match pattern.

```ballerina
type MyRecord record {
    int field1;
    int field2;
};

function fn(MyRecord r1) {
    match r1 {
        {field1: 0,} => { // A syntax error is now given for the comma.

        }
    }
}
```

- An issue in the parser that disallowed qualified identifiers with a pre-declared prefix as a const match pattern has been fixed.

```ballerina
function fn(any x) {
    match x {
        int:MAX_VALUE => { // Match pattern is now allowed
        }

        [int:MAX_VALUE, int:MIN_VALUE] => { // Match pattern is now allowed
        }
    }
}
```

- Qualified identifiers not being allowed in error match patterns has been fixed.

```ballerina
function fn(error e) {
    match e {
        error(errors:MESSAGE) => { // Match pattern is now allowed

        }
    }
}
```

##### Fix compiler crashing when a query expression that throws an error is enclosed within a statement with on-fail. 

```ballerina
function verifyCheck() returns error? {
    return error("custom error");
}

public function main() {
    do {
        _ = from int v in 1 ... 3
            select check verifyCheck();
    } on fail error err {
        io:println("error caught", err);
    }
}
```

- The inherent type of a list constructed using a list constructor with `any` as the contextually-expected type has been fixed to be `(any|error)[]` instead of `any[]`.

```ballerina
public function main() {
    any x = [1, 3, 4];
    if x is (any|error)[] {
        x.push(error("invalid!")); // Now allowed, previously failed at runtime.
    }
}
```

- A bug that allowed additive expressions with operands of types that are union types of different basic types has been fixed.

```ballerina
public function main() {
    int|float a = 4;
    int|float b = 4.5;

    int _ = a + b; // Now result in a compilation error.
}
```

##### Allow additive expression with operands of a union type containing builtin subtypes of `string` and `XML`

Fixed a spec deviation that disallowed the operands of additive expression with a union type containing builtin subtypes of `string` and `XML`

```ballerina
import ballerina/io;

type Strings "A"|"B";

public function main() {
    string:Char|Strings a = "A";
    string b = "B";
    // This, which was disallowed previously results `AB` now.
    io:println(a + b);
}
```

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FCompilerFE+milestone%3A%22Ballerina+2201.1.0%22).

### Runtime Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+2201.1.0%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

#### `ftp` Package

- Introduced the `ftp:Caller` API and added it as an optional parameter in the `onFileChange` method
- Added compiler plugin validation support for the `ftp:Service`
- Added code-actions to generate a `ftp:Service` template

##### `http` Package

- Introduced `ResponseInterceptor` and `ResponseErrorInterceptor`
- Introduced `DefaultErrorInterceptor`
- Added code-actions to generate the interceptor method template
- Allowed records to be annotated with `@http:Header`
- Added basic type support for header parameters in addition to `string` and `string[]`
- Added `anydata` support for service and client data binding
- Added common constants for HTTP status-code responses
- Added union type support for service and client data binding
- Added OpenAPI definition field in the service config

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

##### `kafka` Package

- Added data binding support for `kafka` producer and consumer

##### `rabbitmq` Package

- Added data binding support for `rabbitmq` clients and services
- Added code-actions to generate a `rabbitmq:Service` template

##### `nats` Package

- Added data binding support for `nats` clients and services
- Added code-actions to generate a `nats:Service` template

##### `regex` Package

- Introduced the API to extract the first substring from the start index in the given string that matches the regex
- Introduced the API to extract all substrings in the given string that match the given regex
- Introduced the API to replace the first substring from the start index in the given string that matches the given regex with the provided replacement string or the string returned by the provided function. The `replaceFirst()` API is being deprecated by introducing this API
- Allowed passing a replacer function to `replace` and `replaceAll` APIs. Now the regex matches can be replaced with a new string value or the value returned by the specified replacer function

##### `file` Package

- Introduced the constants for path and path list separators
  - `file:pathSeparator`: It is a character used to separate the parent directories, which make up the path to a specific location. For windows, it’s `\` and for UNIX it’s `/`
  - `file:pathListSeparator`: It is a character commonly used by the operating system to separate paths in the path list. For windows, it’s `;` and for UNIX it’s `:`

##### `os` Package
- Introduced the `setEnv()` function to set an environment variable
- Introduced the `unsetEnv()` function to remove an environment variable from the system
- Introduced the `listEnv()` function to list the existing environment variables of the system

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

##### `grpc` Package

- Fix incorrect stub generation for repeated values of any, struct, timestamp, and duration messages
- Fix incorrect caller type name validation in the gRPC compiler plugin
- Fix passing protobuf predefined types as repeated values and values in messages

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%222201.1.0%22+label%3AType%2FBug).

### Code to Cloud Updates

#### Improvements
- Reduced the package size
- Docker image generation now relies on the user's docker client

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.1.0 of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.1.0%22)

### `ballerinax/awslambda` package

#### Improvements
- Removed the package from the Ballerina distribution. For existing projects, change the version to `2.1.0` in the `Dependencies.toml` file.

### `ballerinax/azure_functions` package

#### Improvements
- Removed the package from the Ballerina distribution. For existing projects, change the version to `2.1.0` in the `Dependencies.toml` file.

### Developer Tools Updates

#### New Features

##### AsyncAPI Tool

- Ballerina AsyncAPI tooling will make it easy for you to start the development of an event API documented in an AsyncAPI contract in Ballerina by generating Ballerina service and listener skeletons. Ballerina Swan Lake supports the AsyncAPI Specification version 2.x. For more information, see [Ballerina AsyncAPI support](http://ballerina.io/learn/ballerina-asyncapi-support) and [AsyncAPI CLI documentation](http://ballerina.io/learn/cli-documentation/asyncapi/#asyncapi-to-ballerina).

##### GraphQL Tool

- Introduced the Ballerina GraphQL tool, which will make it easy for you to generate a client in Ballerina given the GraphQL schema (SDL) and GraphQL queries. Ballerina Swan Lake supports the GraphQL specification [October 2021 edition](https://spec.graphql.org/October2021/). For more information, see [Ballerina GraphQL support](http://ballerina.io/learn/ballerina-graphql-support/) and [Graphql CLI documentation](http://ballerina.io/learn/cli-documentation/graphql/#graphql-to-ballerina).

#### Improvements

##### Debugger
- Added rutime breakpoint verification support. With this improvement, the debugger is expected to verify all the valid breakpoint locations in the current debug source. All the breakpoints that are set on non-executable lines of code (i.e., Ballerina line comments, documentation , blank lines, declarations, etc.) will be marked as `unverified` in the editor.

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake 2201.1.0 of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+label%3ATeam%2FLanguageServer+milestone%3A%22Ballerina+Swan+Lake+2201.1.0%22)
- [Debugger](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+label%3AArea%2FDebugger+milestone%3A%22Ballerina+2201.1.0%22)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+2201.1.0%22)

#### Ballerina Packages Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake 2201.1.0](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+2201.1.0%22+label%3AType%2FBug).

### Breaking Changes

<style>.cGitButtonContainer, .cBallerinaTocContainer {display:none;}</style>
