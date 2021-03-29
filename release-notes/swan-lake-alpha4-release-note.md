---
layout: ballerina-blank-page
title: Release Note
---
### Overview of Ballerina Swan Lake Alpha4

<em>This is the fourth Alpha release in a series of planned Alpha and Beta releases leading up to the Ballerina Swan Lake GA release.</em> 

It introduces the new language features planned for the Swan Lake GA release and includes improvements and bug fixes done to the compiler, runtime, standard library, and developer tooling after the Swan Lake Alpha 3 release.

- [Updating Ballerina](#updating-ballerina)
- [Installing Ballerina](#installing-ballerina)
- [Highlights](#highlights)
- [Language Updates](#language-updates)
    - [New Features](#new-features)
    - [Improvements](#improvements)
    - [Bug Fixes](#bug-fixes)
- [Runtime Updates](#runtime-updates)
    - [New Features](#new-features)
    - [Improvements](#improvements)
    - [Bug Fixes](#bug-fixes)
- [Standard Library Updates](#standard-library-updates)
    - [New Features](#new-features)
    - [Improvements](#improvements)
    - [Bug Fixes](#bug-fixes)
- [Code to Cloud Updates](#code-to-cloud-updates)
    - [New Features](#new-features)
    - [Improvements](#improvements)
    - [Bug Fixes](#bug-fixes)
- [Developer Tools Updates](#developer-tools-updates)
    - [New Features](#new-features)
    - [Improvements](#improvements)
    - [Bug Fixes](#bug-fixes)
- [Ballerina Packages Updates](ballerina-packages-updates)
- [Breaking Changes](#breaking-changes)

### Updating Ballerina

If you are already using Ballerina, you can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Ballerina Swan Lake Alpha4 as follows. 

To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake Alpha4.

> `bal dist pull slalpha3`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Highlights

### Language Updates

#### New Features

##### Relational Expressions With All Ordered Types

Relational expressions (`<`, `>`, `<=`, and `>=`) are supported with all [ordered types](https://ballerina.io/spec/lang/draft/v2020-12-17/#ordering). The static type of both operands must belong to the same ordered type.

##### Inferring the Argument of a Dependently-Typed Function from the Contextually-Expected Type

When the default value of a `typedesc` parameter of a dependently-typed function is `<>` and an argument is not provided for the parameter when calling the function, the argument will be inferred from the contextually-expected type of the function call.
```ballerina
function func(typedesc<anydata> td = <>) returns td = external;

public function main() {
    // The argument for `td` is inferred to be `int`.
    int value = func();
}
```

#### Improvements

##### Improvements to Dependently-Typed Lang Library Functions to Infer the Argument from the Contextually-Expected Type

The `lang:value:ensureType` lang library function is now dependently-typed.

The `typedesc` argument of the `lang.value:cloneWithType`, `lang.value:fromJsonWithType`, `lang.value:fromJsonStringWithType`, and `lang.value:ensureType` dependently-typed lang library functions will be inferred from the contextually-expected type if it is not passed as an argument.

```ballerina
import ballerina/io;

type Person record {|
    string name;
    int age;
|};

public function main() {
    map<anydata> anydataMap = {name: "Amy", age: 30};

    // The `typedesc` argument is inferred to be `Person`
    // based on the contextually expected type.
    Person|error result = anydataMap.cloneWithType();
    io:println(result is Person); // Prints `true`.
}
```

##### Improvements to the Return Type of `lang.value:cloneReadOnly`

The return type of the `lang.value:cloneReadOnly` lang library function has been changed from the type of the value (`T`) to the intersection of the type and `readonly` (`T & readonly`).

```ballerina
type Person record {|
    string name;
    int age;
|};

public function main() {
    Person mutablePerson = {name: "Amy", age: 30};

    // The result of `cloneReadOnly()` can be directly assigned
    // to a variable of type `Person & readonly`.
    Person & readonly immutablePerson = mutablePerson.cloneReadOnly();
}
```

##### Changes to the Return Types of `lang.value:fromJsonFloatString` and `lang.value:fromJsonDecimalString`

The return types of the `lang.value:fromJsonFloatString` and `lang.value:fromJsonDecimalString` lang library functions have been changed from `json` to `lang.value:JsonFloat` and `lang.value:JsonDecimal` respectively.

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha4%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha4%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Alpha4%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake <VERSION> of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha4%22)
- [Docker](https://github.com/ballerina-platform/module-ballerina-docker/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha4%22)
- [AWS Lambda](https://github.com/ballerina-platform/module-ballerinax-aws.lambda/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha4%22)
- [Azure Functions](https://github.com/ballerina-platform/module-ballerinax-azure.functions/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha4%22) 

### Developer Tools Updates

#### Language Server 

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha4%22+label%3AType%2FBug+label%3ATeam%2FLanguageServer).

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake <VERSION> of the repositories below.

- [Language](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha4%22+label%3AType%2FBug+label%3ATeam%2FDevTools)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha%22) 

#### Ballerina Packages Updates

### Breaking Changes

- A compilation error occurs if the inferred type of an unused variable that is declared with `var` includes a subtype of the `error` type.
- The `error<*>` syntax has been removed.
- Relational expressions are no longer supported with numeric values when the static types of the operands belong to different ordered types.
- The `lang.array:indexOf` and `lang.array:lastIndexOf` lang library functions cannot be used with values that do not belong to `anydata`.
- An object used as the iterable value in a `foreach` statement, `from` clause, or `join` clause  must be a subtype of `object:Iterable`.
- The `RawTemplate` type is now a distinct type.
- The filler value of the `decimal` type is now `+0d`.
- Completion type `C` in `stream<T, C>` has been changed from `error|never` to `error?`. `stream<T>` is equivalent to `stream<T, ()>`. `stream<T>` and `stream<T, error>` are assignable to `stream<T, error?>`.
- Annotations with the `service` attach point cannot be used with service classes.
- Checking keywords (`check` and `checkpanic`) are allowed in a statement only if the statement is a call statement (i.e., when the expression is a function or method call).
- The precedence of the `trap` expression has been lowered.
