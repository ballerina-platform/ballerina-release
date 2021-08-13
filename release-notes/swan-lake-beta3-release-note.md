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

##### Introduction of the `!is` Operator

The `!is` operator has been introduced to check if a value does not belong to a given type. This is the negation of the `is` operator.

```ballerina
import ballerina/io;
 
public function main() {
   int|string? x = 10;
 
   if x !is () {
       io:println("int or string value: ", x);
   }
}
```

##### Inferring Types for Numeric Literals in Additive and Multiplicative Expressions

The type for numeric literals in additive and multiplicative expressions is now inferred from the contextually-expected type.

When the contextually-expected type for an additive or multiplicative expression is `float`, the type of a literal used as a sub expression is inferred to be `float`. Similarly, if the contextually-expected type is `decimal`, the type of the literal is inferred to be `decimal`.

```ballerina
float a = 10 + 3.0 + 5.0;
float b = 5 / 10.2;
decimal c = 10.0 * 3;
decimal d = 10 + 5 - 3.0;
```

##### Isolated Inference

The compiler now infers `isolated` for service objects, class definitions, variables, and functions in scenarios where if all of them explicitly specify an `isolated` qualifier, they would meet the requirements for isolated functions and isolated objects.

The following service and its methods are now inferred to be isolated.
```ballerina
import ballerina/http;
 
int defaultIncrement = 10;
 
service / on new http:Listener(8080) {
   private int value = 0;
 
   resource function get value() returns int {
       int value;
       lock {
           value = self.value;
       }
 
       lock {
           return value + defaultIncrement;
       }
   }
 
   resource function post increment(int i) {
       lock {
           self.value += i;
       }
   }
}
```

The compiler does not infer `isolated` for any constructs that are exposed outside the module.

##### Type Narrowing in the `where` Clause of a Query Expression/Action

The `where` clause in a query now narrows the types similar to `if` statements.

```ballerina
import ballerina/io;
 
public function main() returns error? {
   int?[] v = [1, 2, (), 3];
   int total = 0;
   check from int? i in v
       where i is int
       do {
           // Type of `i` is narrowed to `int`.
           total += i;
       };
   io:println(total); // Prints 6.
}
```

#### Improvements

##### Enum Declarations with Duplicate Members

Enum declarations can have duplicate members.

For example, the following declarations where both `LiftStatus` and `TrailStatus` have the same `OPEN` and `CLOSED` members are now allowed.
```ballerina
enum LiftStatus {
   OPEN,
   CLOSED = "0",
   HOLD
}
 
enum TrailStatus {
   OPEN,
   CLOSED = "0"
}
```

However, it is an error if the same enum declaration has duplicate members. Similarly, it is also an error if different enums initialize the same member with different values.

##### `string:Char` as the Static Type of String Member Access

The static type of the member access operation on a value of type `string` has been updated to be `string:Char` instead of `string`.

```ballerina
public function main() {
   string str = "text";
 
   // Can now be assigned to a variable of type `string:Char`.
   string:Char firstChar = str[0];
}
```

##### Directly Calling Function-typed Fields of an Object

Fields of an object that are of a function type can now be directly called via an object value using the method call syntax.

```ballerina
class Engine {
   boolean started = false;
  
   function 'start() {
       self.started = true;
   }
}
 
class Car {
   Engine engine;
 
   function () 'start;
 
   function init() {
       self.engine = new;
       // Delegate `car.start` to `engine.start`.
       self.'start = self.engine.'start;
   }
}
 
public function main() {
   Car car = new;
   car.'start(); // Call the function via the object field.
}
```

##### Tuple to JSON Compatibility

A tuple value whose members are JSON compatible can now be used in a context that expects a JSON value.

```ballerina
[string, int, boolean...] a = ["text1", 1, true, false];
// Now allowed.
json b = a;
```

##### Error Return in the `init` Method of a Service Declaration

Previously, the `init` method of a service declaration could not have a return type containing an error. That restriction has been removed with this release.
If the `init` method of a service declaration returns an error value, it will result in the module initialization failing.

```ballerina
import ballerina/http;
 
service / on new http:Listener(8080) {
   function init() returns error? {
       // Return an error for demonstration.
       // This will result in module initialization failing.
       return error("Service init failure!");
   }
}
```

##### Using `check` in Object Field Initializers

`check` can now be used in the initializer of an object field if the class or object constructor expression has an `init` method with a compatible return type (i.e., the error type that the expression could evaluate to is a subtype of the return type of the `init` method).

If the expression used with `check` results in an error value, the `init` method will return the error resulting in either the `new` expression returning an error or the object constructor expression resulting in an error.

```ballerina
import ballerina/io;
 
int? value = ();
 
class NumberGenerator {
   int lowerLimit;
 
   // `check` can be used in the field initializer
   // since the `init` method's return type allows `error`.
   int upperLimit = check value.ensureType();
 
   function init(int lowerLimit) returns error? {
       self.lowerLimit = lowerLimit;
   }
}
 
public function main() {
   NumberGenerator|error x = new (0);
 
   if x is error {
       io:println(x);
   }
}
```

##### Wildcard Binding Pattern Support in Variable Declarations

The wildcard binding pattern can now be used in a variable declaration with a value that belongs to type `any`.

```ballerina
import ballerina/io;
 
float _ = 3.14;
var _ = io:println("hello");
```

Using the wildcard binding pattern when the value is an error will result in a compilation error.

```ballerina
var _ = error("custom error"); // Compilation error.
```

##### Relaxed Static Type Requirements for `==` and `!=`

Previously, `==` and `!=` were allowed only when both operands were of static types that are subtypes of `anydata`. This has now been relaxed to allow `==` and `!=` if the static type of at least one operand is a subtype of `anydata`.
```ballerina
error? x = ();
 
// Now allowed.
if x == () {
 
}
``` 

#### Bug Fixes

- In a stream type `stream<T, C>`; the completion type `C` should always include nil if it is a bounded stream. A bug where this was not validated for stream implementors has been fixed.

```ballerina
class StreamImplementor {
   public isolated function next() returns record {|int value;|}|error? {
       return;
   }
}
 
stream<int, error> stm = new (new StreamImplementor()); // Will now result in an error.
```

- Resource methods are no longer added to the type via object type inclusions. This was previously added even though resource methods do not affect typing.

```ballerina
service class Foo {
   resource function get f1() returns string {
       return "foo";
   }
 
   function f2() returns int => 42;
}
 
// It is no longer required to implement the `get f1` resource method.
service class Bar {
   *Foo;
 
   function f2() returns int => 36;
}
```

- A bug in string unescaping of unicode codepoints > `0xFFFF` has been fixed.

```ballerina
import ballerina/io;
 
public function main() {
  string str = "Hello world! \u{1F600}";
  io:println(str);
}
```

The above code snippet which previously printed `Hello world!  ὠ0` will now print `Hello world! 😀`.

- A bug in escaping `NumericEscape` has been fixed.

```ballerina
import ballerina/io;
 
public function main() {
  string str = "\\u{61}pple";
  io:println(str);
}
```

This code snippet, which previously printed `\u0061pple` will now print `\u{61}pple`.

- A bug that resulted in `NumericEscape` in the template string not being interpreted literally has been fixed.

```ballerina
import ballerina/io;
 
public function main() {
  string str = string `\u{61}pple`;
  io:println(str);
}
```

The code snippet above, which previously printed `\u0061pple` will now print `\u{61}pple`.

- A bug that resulted in self-referencing not being detected when referenced via a `let` expression or a constant reference expression has been fixed.

The following will now result in errors.

```ballerina
const int INTEGER = INTEGER; // Compilation error.

public function main() {
    string s = let string[] arr = [s] in arr[0]; // Compilation error.
}
```
To view all bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

#### Bug Fixes

- The completion type of a stream is now considered in runtime assignability checks.

```ballerina
stream<int, error?> stm = new (new StreamImplementor());
 
// Evaluated to true in SL Beta2, evaluates to false now.
boolean streamCheck = stm is stream<int>;
```

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

##### Crypto Package
- Improved the hash APIs for cryptographic salt

##### GraphQL Package
- Added field alias support for GraphQL documents
- Added variable support in GraphQL requests
- Added mutation support for GraphQL services
- Added typename introspection

##### gRPC Package
- Added declarative auth configurations
- Added timestamp, duration, and struct type support

##### HTTP Package
- Enabled HTTP trace and access log support
- Added HATEOAS link support
- Introduced the `http:CacheConfig` annotation to the resource signature
- Introduced support for the service-specific media-type subtype prefix
- Introduced the introspection resource method to get the generated OpenAPI document of the service

##### JWT Package
- Added HMAC signature support for JWT
  
##### Log Package
- Added observability span context values to the log messages when observability is enabled.

##### SQL Package
- Added support for `queryRow()` in the database connectors. This method allows retrieving a single row as a record, or a single value from the database.
```ballerina
record{} queryResult = sqlClient->queryRow(`SELECT * FROM ExTable where row_id = 1`)
int count = sqlClient->queryRow(“SELECT COUNT(*) FROM ExTable”)
```

#### Improvements

##### GraphQL Package
- Validate the `maxQueryDepth` at runtime as opposed to validating it at compile time

##### HTTP Package
- Added support for the `map<json>` as query parameter type
- Added support for nilable client data binding types

##### WebSocket Package
- Made the WebSocket caller isolated
- Introduced a write timeout for the WebSocket client

##### SQL Package
- Improved the throughput performance with asynchronous database queries
- Introduced new array out parameter types in call procedures.
- Changed the return type of the SQL query API to include the completion type as nil in the stream. The SQL query code below demonstrates this change.
    
    **Previous Syntax**
    ```ballerina
    stream<RowType, error> resultStream = sqlClient->query(“”);
    ```
    **New Syntax**
    ```ballerina
    stream<RowType, error?> resultStream = sqlClient->query(“”);
    ```

##### IO Package
- Changed the `io:readin` function input parameter to optional. In the previous API, it was required to pass a value to be printed before reading the user input as a string. Remove it due to the breaking change and made it optional. It is not recommended to pass a value to print it in the console.

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Beta3%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Beta3](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22).

### Developer Tools Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake Beta2 of the repositories below.

- [Language Server](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta3%22+label%3AType%2FBug+label%3ATeam%2FLanguageServer)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta%22)
- [Debugger](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+label%3AType%2FBug+label%3AArea%2FDebugger+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta2%22)
- [Test Framework](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+label%3ATeam%2FTestFramework+milestone%3A%22Ballerina+Swan+Lake+-+Beta2%22+label%3AType%2FBug+)

#### Ballerina Packages Updates

### Breaking Changes
