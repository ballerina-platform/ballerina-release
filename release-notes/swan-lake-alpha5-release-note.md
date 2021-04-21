---
layout: ballerina-blank-page
title: Release Note
---
### Overview of Ballerina Swan Lake Alpha5

<em>This is the <fifth> Alpha release in a series of planned Alpha and Beta releases leading up to the Ballerina Swan Lake GA release.</em> 

It introduces the new language features planned for the Swan Lake GA release and includes improvements and bug fixes done to the compiler, runtime, standard library, and developer tooling after the Swan Lake Alpha4 release.

- [Updating Ballerina](#updating-ballerina)
- [Installing Ballerina](#installing-ballerina)
- [Language Updates](#language-updates)
- [Runtime Updates](#runtime-updates)
- [Standard Library Updates](#standard-library-updates)
- [Code to Cloud Updates](#code-to-cloud-updates)
- [Developer Tools Updates](#developer-tools-updates)
- [Ballerina Packages Updates](ballerina-packages-updates)

### Updating Ballerina

If you are already using Ballerina, you can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to directly update to Ballerina Swan Lake Alpha5 as follows. 

To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake Alpha5.

> `bal dist pull slalpha5`

### Installing Ballerina

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Language Updates

#### New Features

##### `lang.xml:data()` Lang Library Function

The `lang.xml:data()`  lang library function has been introduced to get the character data from an `xml` value. This function returns the character data of an `xml:Text` value as a string. For an `xml:Element` value this returns the concatenation of the result of invoking this function over the children of the element. Calling `lang.xml:data()` on comments, processing instructions, and empty sequences returns an empty string.

##### `lang.xml:getDescendants()` Lang Library Function

The `lang.xml:getDescendants()` lang library function has been introduced to retrieve a sequence of the descendant elements for a given element, in document order.

##### Bitwise Operations as Constant Expressions

Bitwise binary operations `<<`, `>>`, `>>>`, `^`, `&`, `|` are now allowed as constant expressions.

```ballerina
const BASE = 0x10;
const int SHIFTED = (BASE << 2) | 0xa;
```

#### Improvements

##### Improvements to the XML Literal

XML template literals now support the inclusion of multiple XML items of the same `xml` subtype as well as different `xml` subtypes.

```ballerina
xml x1 = xml `<ele>item</ele><!--comment-->text<?foo?>`;
xml<xml:Element> x2 = xml `<ele>item1</ele><ele>item2</ele>`;
xml<xml:Comment> x3 = xml `<!--comment1--><!--comment2-->`;
xml<xml:ProcessingInstruction> x4 = xml `<?foo?><?bar?>`;
string interpolation = "Interpolation";
xml<xml:Text> x5 = xml `text ${interpolation}`;
```

##### Normalization of XML Attribute Values
In XML template literals, character references within XML attribute values are now normalized to the referring character. For example, the value of the `e.attr` attribute in the following example is now `a&b`.

```ballerina
xml:Element e = xml `<elem attr="a&amp;b" />`;
```

#### Breaking Changes

- The `lang.array:lastIndexOf` and `lang.array:indexOf` lang library functions can only be used with arrays of which the element types are subtypes of the `anydata` type.
- A compilation error occurs if the field visibility qualifiers in the including type and the included type with object type inclusion are not the same.
- Remote method call action cannot be used to call non-remote methods.
- The `xml` and `readonly` type-descriptors can no longer be used as expressions. A reference to a type definition defined with such type-descriptors needs to be used instead.
- The argument passed to the second parameter of the `attach` method of the listener for service declarations has been fixed as follows. If there is no attach-point in the service, `()` (nil) is passed as the argument. If the attach-point is the root resource path ("/"), an empty array is passed.
- The `lang.xml:getContent()` function no longer accepts `xml:Text` as an argument. The new `lang.xml:data()` function can be used instead.
- `lang.value` functions cannot be called on expressions of type `object`. Function call syntax (`value:func(obj)`) can be used instead.
- The `lang.stream:reduce()` lang library function will only return the reduced value or an error (if the completion type includes a subtype of `error`). It no longer returns a nil `()` value. The return type of `lang.stream:reduce()` has been updated accordingly.
- An issue where the complement of numeric literals returned incorrect values has been fixed.
- An issue that allowed negation with numeric literals has been fixed. Negation can be used only with `boolean` values.
- Subtyping rules have been fixed to consider the `never` type, which denotes an empty set of values as a subtype of any type `T`.
- Relational expressions with lists have been fixed to consider the relative order of lists with different sizes.
- An issue where a non-error value did not match the wildcard match pattern at runtime when the matched expression’s static type included error has been fixed.
- An issue with Isolation analysis where transfer out validation did not happen when `self` was used in a return statement of an isolated object method has been fixed.
- An issue where the method qualifiers were now being set for a `readonly` and `class` intersection has been fixed.

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Alpha5](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha5%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Alpha5](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha5%22+label%3AType%2FBug+label%3ATeam%2FjBallerina).

### Standard Library Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Alpha5](https://github.com/ballerina-platform/ballerina-standard-library/issues?q=is%3Aclosed+is%3Aissue+milestone%3A%22Swan+Lake+Alpha5%22+label%3AType%2FBug).

### Code to Cloud Updates

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake Alpha5 of the repositories below.

- [C2C](https://github.com/ballerina-platform/module-ballerina-c2c/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha5%22)
- [Docker](https://github.com/ballerina-platform/module-ballerina-docker/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha5%22)
- [AWS Lambda](https://github.com/ballerina-platform/module-ballerinax-aws.lambda/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha5%22)
- [Azure Functions](https://github.com/ballerina-platform/module-ballerinax-azure.functions/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha5%22) 

### Developer Tools Updates

#### Language Server 

To view bug fixes, see the [GitHub milestone for Swan Lake Alpha5](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha5%22+label%3AType%2FBug+label%3ATeam%2FLanguageServer).

#### New Features

#### Improvements

#### Bug Fixes

To view bug fixes, see the GitHub milestone for Swan Lake Alpha5 of the repositories below.

- [Language](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha5%22+label%3AType%2FBug+label%3ATeam%2FDevTools)
- [Update Tool](https://github.com/ballerina-platform/ballerina-update-tool/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+project%3Aballerina-platform%2F32)
- [OpenAPI](https://github.com/ballerina-platform/ballerina-openapi/issues?q=is%3Aissue+is%3Aclosed+label%3AType%2FBug+milestone%3A%22Ballerina+Swan+Lake+-+Alpha%22) 

#### Ballerina Packages Updates

### Breaking Changes
