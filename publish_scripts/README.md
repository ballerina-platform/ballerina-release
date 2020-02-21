# *publish_json.py*
## This script will create json files needed for the creation of [Release Notes](https://ballerina.io/downloads/release-notes/) and [Archived downloads](https://ballerina.io/downloads/archived/) pages of Ballerina website

Requires 2 arguments to run this script 
1. URL of *archived_releases.json*
2. URL of *latest_release.json*

Example Usage
```
python3 publish_json.py https://product-dist.ballerina.io/downloads/archived_releases.json https://product-dist.ballerina.io/downloads/latest_release.json?982
```

# *release_note_md_to_html.py*
## This script will create html for given md file

Requires an argument to run this script 
1. Filepath of md file

Example Usage
```
python3 release_note_md_to_html.py /home/sajeer/Desktop/release-notes-master/release-notes-1.1.3.md
```
