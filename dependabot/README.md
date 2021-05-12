# Dependabot Scripts

## Generate Dependency Graph

`update_dependency_graph.py` script will generate the dependency graph within the extensions and assign them to levels based on the shortest dependency paths.

For this will process the 'build.gradle' file in the root folder. This will look for the repository url added for the dependency resolution,
    
    maven {
        url = 'https://maven.pkg.github.com/ballerina-platform/module-ballerina-time'
        credentials {
            username System.getenv("packageUser")
            password System.getenv("packagePAT")
        }
    }

## Update Dependencies in Extensions

`update_dependencies_in_pipeline.py` script will bump dependencies in extensions.

Parameters:
1. Retrigger a failed dependency bump workflow (true/false) - This flag is so that intermediate dependencies will not be bumped to latest, if this set to true

2. Ballerina Lang Version - If an empty string is passed the workflow will bump all extensions to the latest available version. This is
mandatory if the "Retrigger a failed dependency bump workflow" is set to true.

3. Auto Merge PRs - This will stop auto merging the dependency bump PRs if set to true.

4. Event Type (Optional) - USed to differentiate scheduled jobs from manual trigger.

### Configurations

The scripts can be configured in `resources/module_list.json`

1. auto_bump - Used to disable the schedule jobs

2. lang_version_substring - Used to filter language versions in getting the latest version if lang version is not specified when invoking the script

3. modules - Modules that is added in the pipeline

    |Key|Description|Default|
    |:---|:---|:---|
    |name|Repository name|N/A|
    |group_id|Group id of the published package|org.ballerinalang|
    |artifact_id|Artifact id of the published package|<artifact-name>+ "-ballerina"*|
    |version_key|Version Key to be used in gradle.properties|"stdlib" + <Capitalised-Artifact-Name> + "Versions"|
    |auto_merge|Whether to auto merge dependent bump PRs|true|

## Update Dependencies in Connectors

`update_connectors.py` script will bump dependencies in connectors.

Parameters:
1. Ballerina Lang Version

2. Auto Merge PRs - This will stop auto merging the dependency bump PRs if set to true.

### Configurations

The scripts can be configured in `resources/connector_list.json`

1. auto_bump - Used to disable the schedule jobs

3. modules - Modules that is added in the pipeline

   |Key|Description|Default|
   |:---|:---|:---|
   |name|Repository name|N/A|
   |auto_merge|Whether to auto merge dependent bump PRs|true|