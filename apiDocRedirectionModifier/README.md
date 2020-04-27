# Ballerina API doc modifier
This will modify the generated api docs. 

# How to run

### Required

- Install latest version of the golang


Run the `redirection.sh` with following parameters

```bash
./redirection.sh <API_DOCS_DIR> <REDIRECT_VERSION> <PERMALINK_PREFIX> <OUTPUT_LOCATION>
```

### API_DOCS_DIR

This is the directory where the generated apidocs are located. Tool will use these to add the modification.
ex: 
`/<root>/ballerina-dev-website/learn/api-docs/ballerina/`
or
`/<root>/ballerina-dev-website/learn/api-docs/ballerinax/`

### REDIRECT_VERSION

This is the version of the pages which should be redirected to the given new API docs.
ex:
`v1-2` or `v1-1`

### PERMALINK_PREFIX

This is prefix of the permalink path of the api docs without the api doc name and the version.
ex: 
`/learn/api-docs/ballerina/` or `/learn/api-docs/ballerinax/`

### OUTPUT_LOCATION

This is the directory name to where the modified api-docs should be copied to.
ex:
`target`

# Example Usage

### Modify Ballerina std libs

```bash
./redirection.sh <root>/ballerina-dev-website/learn/api-docs/ballerina/ v1-2 /learn/api-docs/ballerina/ target
```

### Modify Ballerinax std libs

```bash
./redirection.sh <root>/ballerina-dev-website/learn/api-docs/ballerinax/ v1-2 /learn/api-docs/ballerinax/ targetx
```
