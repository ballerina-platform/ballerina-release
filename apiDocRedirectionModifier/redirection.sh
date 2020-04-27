#!/bin/bash
echo "....API doc modification started...."

# API_DOCS_DIR is location where the api docs, that need to be changed, located.
API_DOCS_DIR=$1
# REDIRECT_VERSION is versions of the doc (ex: v1-2 or v1-1) to redirect from.
REDIRECT_VERSION=$2
# PERMALINK_PREFIX this is the path comes after the version. ex: /learn/api-docs/ballerina/ or /learn/api-docs/ballerinax/ 
PERMALINK_PREFIX=$3
# OUTPUT_LOCATION is the location where the modified files should be saved to.
OUTPUT_LOCATION=$4

go run addFrontMatter.go $API_DOCS_DIR $REDIRECT_VERSION $PERMALINK_PREFIX $OUTPUT_LOCATION
echo "....API doc modification Completed...."
