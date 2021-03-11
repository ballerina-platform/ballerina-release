---
layout: ballerina-blank-page
title: Release Note
---
### Overview of Ballerina Swan Lake Alpha3

This Alpha3 release includes the language features planned for the Ballerina Swan Lake release. Moreover, this release includes improvements and bug fixes to the compiler, runtime, standard library, and developer tooling. This release note lists only the features and updates added after the Alpha2 release of Ballerina Swan Lake.

- [Updating Ballerina](#updating-ballerina)
    - [For Existing Users](#for-existing-users)
    - [For New Users](#for-new-users)
- [Highlights](#highlights)
- [What is new in Ballerina Swan Lake Alpha3](#what-is-new-in-ballerina-swan-lake-alpha3)
    - [Language](#language)
    - [Runtime](#runtime)
    - [Standard Library](#standard-library)
    - [Code to Cloud](#code-to-cloud)
    - [Developer Tools](#developer-tools)
    - [Breaking Changes](#breaking-changes)

### Updating Ballerina

You can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to update to Ballerina Swan Lake Alpha3 as follows.

#### For Existing Users

If you are already using Ballerina, you can directly update your distribution to the Swan Lake channel using the [Ballerina Update Tool](/learn/tooling-guide/cli-tools/update-tool/). To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake Alpha3.

> `bal dist pull slalpha3`

#### For New Users

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Highlights

### What is new in Ballerina Swan Lake Alpha3

#### Language

##### Support for Module-level Variables with List, Mapping, and Error Binding Patterns

Variable declarations with list, mapping, and error binding patterns are now allowed at module level. Unlike simple variables, these variables must be initialized in the declaration.

Also, these variable declarations cannot contain an `isolated` or `configurable` qualifier.

```ballerina
type Person record {|
    string name;
    boolean married;
|};

function getList() returns [int, float] => [1, 2.5];

function getPerson() returns Person => {name: "John", married: true};

function getError() returns error => error("error message", code = 1001, fatal = true);

// Module-level variable declaration with a list binding pattern. 
[int, float] [a, b] = getList();

// Module-level variable declaration with a mapping binding pattern.
Person {name: firstName, married: isMarried} = getPerson();

// Module-level variable declaration with an error binding pattern.
error error(message, code = errCode) = getError();
```

##### Support for Module-level Public Variables

Module-level variables can now be declared as public using the `public` qualifier. Such variables will be visible outside the modules in which they are declared.

Isolated variables and variables declared with `var` cannot be declared as public variables.

```ballerina
public string name = "Ballerina";

public [int, float] [a, b] = [1, 2.5];
```

##### Improvement to Annotation Attachment with Empty Mapping Constructor Expression

If the type of the annotation is a mapping type for which an empty mapping constructor is valid, the mapping constructor expression is no longer mandatory in the annotation attachment.

The absence of the mapping constructor expression in such an annotation attachment is equivalent to specifying a mapping constructor expression with no fields.
```ballerina
type Annot record {|
    int[] i = [];
|};

public annotation Annot v1 on function;

@v1 // Same as `@v1 {}`
public function main() {
}
```

##### Improved lang library functions

###### New `xml:text()` function

This function can be used to select all the items in a sequence that are of type `xml:Text`.

```ballerina
xml name = xml `<name>Dan<middleName>Gerhard</middleName><!-- This is a comment -->Brown</name>`;
xml:Text nameText = (name/*).text();
io:println(nameText); // "DanBrown"
```

#### Runtime

#### Standard Library

#### Code to Cloud

#### Developer Tools

##### Language Server

##### Ballerina Shell

Ballerina Shell now supports redefining module-level declarations and variable declarations. `/remove NAMES` command can be used to remove one or multiple declarations from snippet memory.

```ballerina
=$ int i = 3;
=$ string j = "Hi";
=$ string i = "Hello";  // Same variable can be redefined
=$ /remove i j   // Variables can be removed
=$ i
| error: undefined symbol 'i'
|       i
|       ^
| Compilation aborted due to errors.
```

Module-level declarations within a file can be loaded using the `-f` or `--file` command-line arguments. `/file <FILENAME` command can also be used for this purpose, from within the shell. Note that `--force-debug` will now have only a long option; `-f` short option is now used to open the file.

```bash
$ bal shell -f my_file.bal
```

Also, error messages for error objects, panics, and fails will show distinct error messages from each other. Panics will show `panic: ERROR` and fails will show `fail ERROR`. Error-values will simply be evaluated to their value.

```ballerina
=$ error("Error") // Error values will simply evaluate
error("Error")
=$ panic error("Error")  // Panics will show as panic runtime errors
panic: {ballerina}DivisionByZero {"message":" / by zero"}
| Execution aborted due to unhandled runtime error.
=$ fail error("Error")  // Fails will show as fails
fail: Error {}
```

Qualifiers (e.g., `final`) will now correctly work and `public` will declarations are allowed. Additionally, Ballerina Shell will now correctly work with cyclic type definitions and array binding patterns.

A bug causing some snippets (e.g., `json x = {`) to be incorrectly identified as complete, was fixed.

##### Debugger

Now, the debugger supports conditional breakpoints. Conditional expressions can be configured for Ballerina breakpoints in the VSCode debug view.

#### Breaking Changes
