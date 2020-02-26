# 1. *publish_json.py*
## This script will create json files needed for the creation of [Release Notes](https://ballerina.io/downloads/release-notes/) and [Archived downloads](https://ballerina.io/downloads/archived/) pages of Ballerina website

Requires 2 arguments to run this script 
1. Path of *archived_releases.json*
2. Path of *latest_release.json*

Example Usage
```
python3 ./publish_scripts/publish_json.py ./publish_scripts/archived_releases.json ./publish_scripts/latest_release.json
```

# 2. *release_note_md_to_html.py*
## This script will create html for given md file

Requires an argument to run this script 
1. Path of md file

Example Usage
```
python3 ./publish_scripts/release_note_md_to_html.py ./publish_scripts/release_note.md
```
