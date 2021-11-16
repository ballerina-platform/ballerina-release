---
layout: ballerina-left-nav-release-notes
title: Swan Lake Beta4
permalink: /downloads/swan-lake-release-notes/swan-lake-beta4/
active: swan-lake-beta4
redirect_from: 
    - /downloads/swan-lake-release-notes/swan-lake-beta4
    - /downloads/swan-lake-release-notes/
    - /downloads/swan-lake-release-notes
---
### Overview of Ballerina Swan Lake Beta4

<em>This is the fourth Beta release in a series of planned Alpha and Beta releases leading up to the Ballerina Swan Lake GA release.</em> 

It introduces the new language features planned for the Swan Lake GA release and includes improvements and bug fixes done to the compiler, runtime, standard library, and developer tooling after the Swan Lake Beta3 release.

### Updating Ballerina

If you are already using Ballerina, you can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Ballerina Swan Lake Beta4 as follows. 

To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake Beta4.

> `bal dist pull slbeta4`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

##### Support for Numeric Operations with Operands of Optional Numeric Types

Unary expressions (`+`, `-`, and `~`), multiplicative expressions, additive expressions, shift expressions, and binary bitwise expressions can now be used with operands of optional numeric types. If the static type of an operand is an optional numeric type, the static type of the result will also be an optional numeric type.

The following examples are now allowed.

```ballerina
import ballerina/io;
 
public function main() {
   int? a = 10;
   int? b = 5;
   int? c = ();
 
   int? d = a + b;
   io:println(d is ()); // prints `false`
   io:println(d); // prints `15`
 
   int? e = a - c;
   io:println(e is ()); // prints `true`
 
   // Also allowed.
   int? f = a * b;
   int? g = a << c;
   int? h = a & b;
   int? i = -a;
   int? j = +c; // result is `()`
}
```

#### Improvements

##### Restrictions When Calling a Function or a Method in a Match Guard

Restrictions have been introduced for when a function or a method is called in a match guard, in order to ensure that the match guard does not mutate the value being matched.

A function or method call is now allowed in a match guard only if it meets one of the following conditions.
- the type of the expression following `match` is a subtype of `readonly` or
- the function/method is `isolated` and the types of any and all arguments are subtypes of `readonly`

The following will now result in compilation errors.

```ballerina
type Data record {
   string name;
   boolean valid;
   int id?;
   decimal price?;
};
 
public function main() {
   Data data = {name: "Jo", valid: false};
   [int, decimal] currentValues = [1234, 20.5];
 
   match data {
       var {id, price} => {
       }
       // Now results in compilation errors for the match guard since neither the type of the matched
       // expression nor the types of the arguments are subtypes of `readonly`.
       var {name} if stillValid(data, currentValues) =>  {
       }
   }
}
 
isolated function stillValid(Data data, [int, decimal] values) returns boolean {
   // ...
   data.id = values[0];
   data.price = values[1];
   return false;
}
```

##### Improved support for unreachability

Unreachability analysis has been improved for if-else statements and `while` statements. Constant conditions that are known to be either true or false at compile-time are now considered in unreachability analysis.

The following conditions are taken into consideration in the analysis of unreachability.

1. If a statement block is unreachable, then every statement in it is unreachable.
2. `if` statements with constant conditions are not errors except insofar as they lead to statements being unreachable.
3. An `is` expression is constant `true` if the static type of the expression is a subtype of the type against which the check is done. 
4. Calling a function with a return type of `never` cannot complete normally, making subsequent code unreachable.

```ballerina
import ballerina/io;

function fn1() {
    if false {
        io:println("unreachable"); // this will now result in a compilation error: unreachable code
    }

    while false {
        io:println("unreachable"); // this will now result in a compilation error: unreachable code
    }
}

function fn2() {
    if true {
        io:println("reachable");
    } else {
        io:println("unreachable"); // this will now result in a compilation error: unreachable code
    }
}

function fn3() {
    if true {
        return;
    }
    io:println("unreachable"); // this will now result in a compilation error: unreachable code
}

function fn4() {
    while true {
        return;
    }
    io:println("unreachable"); // this will now result in a compilation error: unreachable code
}
```

```ballerina
enum E { X, Y, Z }

function fn1(E e) {
    if e is X {
        doX();
    } else if e is Y {
        doY();
    } else if e is Z {
        doZ();
    } else {
        // any statement in this block will now be unreachable
    } 
}

function fn2(E e) {
    if e is X {
        doX();
    } else if e is Y {
        doY();
    } else if e is Z {
        doZ();
    } else if e is Y {
        // any statement in this block will now be unreachable
    } 
}

function fn3(E e) returns int {
    if e is X {
        return 1;
    } 
    if e is Y {
        return 2;
    } 
    if e is Z {
        return 3;
    } 
    // any statement here will now be unreachable
}
```

##### Type Narrowing Following an `if` Statement Without an `else` Block if the `if` Statement Block Cannot Complete Normally

Building on the improvements introduced to unreachabillity analysis, types are now narrowed following an `if` statement without an `else` block, if the `if` statement block cannot complete normally.

```ballerina
function populate(int[] arr, string str) returns error? {
    int|error res = int:fromString(str);

    if res is error {
        return error("Invalid Value", res);
    }

    // The type of `res` is now narrowed to `int` here.
    // The variable `res` can be used as an `int` and can therefore be used in an `array:push` call with an `int[]`.
    arr.push(res);
}
```

This narrowing may lead to other compilation errors since the static type of the variable will now be a narrowed type.

```ballerina
function populate(int[] arr, string str) returns error? {
    int|error res = int:fromString(str);

    if res is error {
        return error("Invalid Value", res);
    }

    // Previously allowed, now a compilation error since `res`'s type is now `int` and doesn't include `error`.
    int intRes = check res;

    arr.push(intRes);
}
```

##### Restrictions on Assignments to Narrowed Variables within Loops

Within a `while` statement or a `foreach` statement, it is no longer possible to assign a value to a variable that was narrowed outside the statement, unless the loop terminates after the assignment. I.e., at the end of the loop body and at every `continue` statement there must be no possibility that a narrowed variable has been assigned to.

The following sample, which previously resulted in a runtime panic, will now result in a compilation error.

```ballerina
function validate(int?[] arr) returns boolean {
    int? value = let int length = arr.length() in length > 0 ? length : ();

    if value is int {
        foreach int? item in arr {
            int currentValue = value;

            if item is () {
                value = (); // error: invalid attempt to assign a value to a variable narrowed outside the loop
                continue;
            }

            return item < value;
        }
    }

    return false;
}
 
public function main() {
   boolean validationRes = validate([(), 2, 1]);
}
```

##### Change in Expected Return Statements in a Function with an Optional Type as the Return Type

A function having an optional type that is not a subtype of `error?` as the return type is now expected to explicitly return a value. A warning is emitted when such a function does not explicitly return a value and falls off the end of the function body. 

```ballerina
function parse(string str) returns int? { // Now results in a warning. 
    int|error a = int:fromString(str);
    if a is int {
        return a;
    }
}
```

#### Bug Fixes and Breaking Changes

- The trailing dot format of the floating point literal has been disallowed to avoid lexical ambiguity.

```ballerina
// The following are now disallowed.
decimal d1 = 2.;
decimal d2 = 2.d;
decimal d3 = 2.D;
decimal d4 = 2.e12;
float f1 = 2.f;
float f2 = 2.F;
float f3 = 0x1A.;
float f4 = 0x1A.p4;

// The following can be used instead.
decimal d11 = 2.0;
decimal d12 = 2.0d;
decimal d13 = 2.0D;
decimal d14 = 2.0e12;
float f11 = 2.0f;
float f12 = 2.0F;
float f13 = 0x1A.0;
float f14 = 0x1A.0p4;
```

- Intervening white spaces have been disallowed in the qualified identifier to avoid a parsing ambiguity between the ternary conditional expression and qualified identifier.
  
```ballerina
import ballerina/io;

public function main() {
    io:print("Ballerina"); // Valid.
    io : print("Ballerina"); // compilation error: intervening whitespaces are not allowed in a qualified identifier.
}
```

With this, `x ? a : b:c` will now be parsed as `x ? a : (b:c)` since the colon with spaces is interpreted only as part of a conditional expression.

- A bug that resulted in hash collisions not being handled correctly in `table` values has been fixed. 

```ballerina
import ballerina/io;
 
public function main() {
    table<record {readonly int? k;}> key(k) t = table [];
    t.add({k: 0});
    io:println(t.hasKey(()));
}
```

The above code snippet, which previously printed `true` will now print `false`.

- Object type inclusion with an object that has private fields or members has been disallowed.

```ballerina
class Person {
    string firstName;
    string lastName;
    private string dob;

    function init(string firstName, string lastName, string dob) {
        self.firstName = firstName;
        self.lastName = lastName;
        self.dob = dob;
    }

    private function getName() returns string => self.firstName + self.lastName;
}
 
class Employee {
    *Person; // Will now result in an error.
    int id;

    function init(string firstName, string lastName, string dob, int id) {
        self.firstName = firstName;
        self.lastName = lastName;
        self.dob = dob;       
        self.id = id;
    }

    private function getName() returns string => self.firstName;	
}
```

- A bug that resulted in compilation errors not being emitted for invalid `xml` template expressions has been fixed.

```ballerina
xml x = xml `</>`; // Will now result in an error.
```

- `xml:createElement` now accepts the attribute map as the second argument.

```ballerina
xml:Element jo = xml:createElement("name", {id: "1234"}, xml `Jo`);
```

- The `xml:get` function’s return type has been updated to return the exact type `T` when the `xml` sequence is of type `xml<T>`.

```ballerina
xml<xml:Element> employees = xml `<e1><name>Jo</name></e1><e2><name>Mary</name></e2>`;
xml:Element employee1 = employees.get(0);// Now allowed.
```

- The `table:map` function’s function argument `func` and the return type have been updated to work with subtypes of mapping types instead of any type.

```ballerina
table<record {int id; string name;}> tb = table [
   {id: 1234, name: "Jo"},
   {id: 2345, name: "May"}
];

var idTable = tb.map(function (record {int id; string name;} r) returns int { // No longer allowed.
   return r.id;
});
```

- Few deviations in the `lang.error` module have been corrected according to the language specification. The `CallStack` class and `CallStackElement` records have been removed. Now a stack frame is represented by an `error:StackFrame` object.
	
Prior to Swan Lake Beta4, the `error:stackTrace()` function returned an `error:CallStack` object which had the following structure, which was a deviation from the specification.

```ballerina
public class CallStack {
   public CallStackElement[] callStack = [];
}
```

This has now been fixed, and it is no longer possible to retrieve an `error:CallStack` object or directly access the `callStack` array as follows.

```ballerina
error:CallStack callStack = err.stackTrace(); // `CallStack` is undefined
error:CallStackElement[] elements = err.stackTrace().callStack; // Not allowed, `CallStackElement` is undefined, no `callStack` field.
```

The `error:stackTrace` function now returns an array of StackFrame objects.

```ballerina
public type StackFrame readonly & object {
   public function toString() returns string;
};
```

```ballerina
error:StackFrame[] stackTrace = e.stackTrace(); // Now returns `error:StackFrame[]`.
```

- The return type of the `error:detail` function in the lang.error module is now a subtype of `readonly`. It is the intersection of `readonly` and the detail type of the error.

```ballerina
type Detail record {|
   int code;
|};
 
type Error error<Detail>;
 
function fn(Error e) {
   Detail & readonly detail = e.detail(); // Now allowed.
}
```

- A deviation in the `stream:next` function’s stream argument name has been fixed. The name has been changed from `strm` to `stm`.

- A bug in `array:sort` which was sorting the original list has been rectified. The function now returns a new sorted array. The original array remains unchanged.

- The name of the argument to `transaction:setData()` has been changed from `e` to `data`. Moreover, the static type of the argument to `transaction:setData()` and the return type of `lang.transaction:getData()` have been changed to `readonly`. They were previously of type `(any|error) & readonly` and even this change would accept/return the same set of values.

- The `float:min()` and `float:max()` functions now return `float:NaN` if an argument is `float:NaN`. 

```ballerina
import ballerina/io;

public function main() {
    float result = float:min(1, float:NaN);
    io:println(result === float:NaN); // prints true

    result = float:max(5, float:NaN);
    io:println(result === float:NaN); // prints true
}
```

- A bug in the `decimal:fromString()` function which allowed parsing a string that matched the `HexFloatingPointLiteral` has been fixed. It now returns an error.

```ballerina
import ballerina/io;

public function main() {
   decimal|error result = decimal:fromString("0xab12"); // Now returns an error.
   io:println(result is error); // prints true
}
```

- A bug in the `float:fromString()` function allowed parsing a string that had matched a `DecimalFloatingPointNumber` with `FloatingPointTypeSuffix` has been fixed. This will now return an error.

```ballerina
import ballerina/io;

public function main() {
    float|error result = float:fromString("12.24f"); // Now returns an error
    io:println(result is error); // prints true
}
```

- The `float:fromHexString()` function now returns an error if the provided string argument does not match a `HexFloatingPointLiteral`. 

```ballerina
import ballerina/io;
 
public function main() {
   float|error result = float:fromHexString("12.3");
   io:println(result is error); // prints true, error message - invalid hex string: ‘12.3’
}
```

- A spec deviation was fixed in `int:toHexString` which was causing it to convert negative values to a positive number before converting to a hexadecimal string.

- A deviation in the `lang.error` `RetryManager` and `DefaultRetryManager` objects' `shouldRetry` method argument type is fixed. The type has been changed from `error?` to `error`.
	
```ballerina
public class CustomRetryManager {
   private int count;

   public function init(int count = 3) {
       self.count = count;
   }

   public function shouldRetry(error e) returns boolean {
       if e is CustomError && self.count > 0 {
           self.count -= 1;
           return true;
       } else {
           return false;
       }
   }
}
```

- A spec deviation was fixed when declaring out of range float value. With current behaviour this gives a compile time error.

- Spec deviation related to numeric literal have been corrected according to the language specification. 

If the numeric literal is not include float type suffix or  decimal type suffix and not a hex floating point literal the type of that numeric literal will be based on following rules.

1. If the literal is floating point literal then the possible basic types in order of preference are float or decimal otherwise they are int, float or decimal.
2. If there is contextual expected type and there is a basic type int, decimal or float in contextual expected type, Use the most perrered type in the order of int, float or decimal.
3. Otherwise, use the most preferred possible basic type in the order of int, float or decimal.

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Beta4%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake <VERSION> of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22)
- [Docker](https://github.com/ballerina-platform/module-ballerina-docker/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22)
- [AWS Lambda](https://github.com/ballerina-platform/module-ballerinax-aws.lambda/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22)
- [Azure Functions](https://github.com/ballerina-platform/module-ballerinax-azure.functions/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22) 

### Developer Tools Updates

#### Language Server 

To view bug fixes, see the [GitHub milestone for Swan Lake <VERSION>](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22+label%3AType%2FBug+label%3ATeam%2FLanguageServer).

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake <VERSION> of the repositories below.

- [Language](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22+label%3AType%2FBug+label%3ATeam%2FDevTools)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Beta4%22) 

#### Ballerina Packages Updates

### Breaking Changes
