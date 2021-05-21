# Ballerina Central Tests
## Creating Tests for a New Release

### Modifying Dockerfile
Three changes should be made to the `Dockerfile`, corresponding to the new release under the following sections.
- Get Ballerina releases
- Copy Ballerina runtimes
- Set environment variables

It is advised to follow a similar pattern as in the previous releases when making the above changes.

### Writing Tests for New Release

- 	Directories for the tests of each release can be found at `tests/`.
- Duplicate the directory of the previous release's test cases and rename according to the new release.
    - `tests/<release_name>`
- Modify each test within the duplicated directory to correspond to the new release.
    - Change the release name to the new one.
    - Use the new release's environment variable.
- Add, remove or modify the tests as required.

### Including the New Tests
The newly added tests should be included within `tests/run-tests.sh`.
- Create a new section (subtopic) for the new release.
- Add new lines to execute each test with the required configurations.
- Ensure all new tests are added before the final line, `rm -rf bctest*`.

### Workflow
The workflow can be found at `/.github/ballerina-central-test.yml`. No changes are required to be made to the workflow. 
