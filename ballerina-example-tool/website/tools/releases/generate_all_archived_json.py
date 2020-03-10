import os, fnmatch
import json
import sys

baseDir = '/var/www/html/products/downloads'
metadataFile = '*metadata.json'
outputFile = 'archived_releases.json'
if len(sys.argv) > 1:
    topdir = sys.argv[1]
else:
    topdir = '.'
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

allMetadataFiles = find(metadataFile, baseDir)
allMetadata = []
for metadataFile in allMetadataFiles:
    print('Reading metadata from '+metadataFile)
    metadata = json.load(open(metadataFile))
    allMetadata.append(metadata)

with open(os.path.join(baseDir,outputFile), 'w') as outfile:
    json.dump(allMetadata, outfile)
