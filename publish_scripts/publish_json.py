import requests
import json
import os
from shutil import copyfile
import sys

if (len(sys.argv)!=3):
    print ('Please provide two args <url of archived_releases.json> and <url of latest_releases.json>')
    sys.exit()
  
# endpoint of archived_releases.json
##URL_archived = "https://product-dist.ballerina.io/downloads/archived_releases.json"
URL_archived = sys.argv[1]

# endpoint of latest_release.json
##URL_latest = "https://product-dist.ballerina.io/downloads/latest_release.json?982"
URL_latest = sys.argv[2]

# target location of modified json
subDir = "/target/output/"

# output filename
outputJson_rel = "release_notes_versions.json"
outputJson_arch = "archived_releases.json"

# getting the archived_realease.json
r = requests.get(url = URL_archived) 
data = r.json()

# getting the latest_realease.json
r = requests.get(url = URL_latest) 

# append both json
data.append(r.json())

# write to release_notes_versions.json
baseDir = os.path.dirname(os.path.realpath(__file__))
outputFile_rel = baseDir + subDir + outputJson_rel
os.makedirs(os.path.dirname(outputFile_rel), exist_ok=True)
with open(outputFile_rel, "w") as f:
    json.dump(data, f)

# create archived_releases.json
outputFile_arch = baseDir + subDir + outputJson_arch
copyfile(outputFile_rel, outputFile_arch)

print (".../target/output/")
