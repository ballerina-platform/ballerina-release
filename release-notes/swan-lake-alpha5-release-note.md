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

#### Improvements

#### Bug Fixes

To view bug fixes, see the [GitHub milestone for Swan Lake Alpha5](https://github.com/ballerina-platform/ballerina-lang/issues?q=is%3Aissue+is%3Aclosed+milestone%3A%22Ballerina+Swan+Lake+-+Alpha5%22+label%3AType%2FBug+label%3ATeam%2FCompilerFE).

### Runtime Updates

#### New Features


###### Support for configurable variables with records having fields of record types

```ballerina
public type Person readonly & record {
     string name;
     int id;
     Address address;
};

public type Address  record {
    string city;
    County country;
};

public type County  record {
    string name;
};


configurable Person person = ?;

```

The  `Config.toml` would be as follows.

```toml
[person]
name = "waruna"
id = 10
address.city="Colombo"
address.country.name="Sri Lanka"

```

###### Support for configurable variables with arrays having fields of record types

```ballerina
configurable Person[] & readonly personArray = ?;

```
The  `Config.toml` would be as follows.

```toml
[[personArray]]
name = "manu"
id = 11
address.city="New York"
address.country.name="USA"

[[personArray]]
name = "hinduja"
id = 12
address.city="London"
address.country.name="UK"
```

###### Support for configurable variables with multidimentional arrays

```ballerina
configurable int[][] & readonly int2DArr = ?;
```
The  `Config.toml` would be as follows.

```toml
int2DArr = [[1,2],[3,4]]
```

###### Support for optional module name in TOML syntax of configurable variables

When providing values for the configurable variables, the module information should be provided in the `Config.toml` file according to the following specifications.


* The org-name and module-name are optional for configurable variables defined in the root module of the program.
* The org-name is optional only for configurable variables defined in the root package of the program.
For example, consider a package with the organization name as `myOrg` and root module name as `main`. 

The  `main.bal` would be as follows.

```ballerina
import main.foo;
import importedOrg/mod;
configurable string mainVar = ?;
public function main() {
// use imported modules
}
```

The`foo.bal` file of the `main.foo` module will be as follows.


```ballerina
configurable string fooVar = ?;
```
In the `mod.bal`, which is from another package with the organization name `importedOrg` and module name `mod`, 

```ballerina
configurable string modVar = ?;
```

The values can be provided in `Config.toml` as follows.
```toml
mainVar = "variable from root module"
[main.foo]
fooVar = "variable from non-root module of the root package"
[importedOrg.mod]
modVar = "variable from non-root package"
```
#### Improvements
###### Improved Command-Line Argument Parsing

The command-line arguments are now parsed into:
- options
- option arguments
- operands

**Options**

Included record parameter as the last of the parameter specify options.

```ballerina
public type Person record {
	string name;
	float? score = 0;
};

public function main(*Person person) {
	// Process data here
}
```

```
bal run file.bal -- --name riyafa --score=99.9
```
In the above example, `name` and `score` are options. `riyafa` and `99.9` are arguments of the option.

**Operands**

Other parameters that are not included records specify operands; for these parameters, the position is significant and the name is not.

```ballerina
public type Person record {
	string name;
	float? score = 0;
};
public function main(int efficiency, string character, *Person person) {
	// Process data here
}
```

```
bal run file.bal -- --name riyafa  100 --score=99.9 Good
```

This example, which is the same as above includes `100`, which gets mapped to `efficiency`, and `Good`, which gets mapped to `character` as operands. 

Both operand and option parameters can be of types int, float, decimal, string, array of any of these types and union of any of these types with nil. 
Additionally, option parameters can be of types `boolean`, `boolean[]`, or `boolean?`.

**Operand arrays**

>**Note:** If there is an operand parameter of type O[], then it cannot be followed by parameters of type O[], O?, and O x = d. Here O stands for a type that is a subtype of one of string, float, or decimal. An array value is specified by repeatedly specifying the `option` parameter.

If `scores` is an int array, then,

```ballerina
bal run file.bal -- --scores=10 --scores=20 --scores=30
```
This produces the following int array.
```
[10, 20, 30]
```

**Option boolean parameters**

When there’s an option of `boolean`, `boolean[]`, or `boolean?` type, it does not take an `option` argument. The presence of the option is considered to be `true` and the absence of it is considered to be false. 
In the following example, suppose `results` is a boolean array.
```
bal run file.bal -- --results --results --results
```
This produces the following boolean array.
```
[true, true, true]
```

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
