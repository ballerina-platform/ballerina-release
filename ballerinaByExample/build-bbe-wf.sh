#!/bin/bash
echo ".....Building BBE Site....."

BASEDIR=$(dirname $0)
# SITE_VERSION is the version of the Ballerina that these BBEs are belongs to. ex: v1-1 or v1-0
SITE_VERSION=$1
# BBE_GEN_DIR is the location where the generated files will be placed.
BBE_GEN_DIR=""
# If true, Generate BBE with jekyll front matter. If false, Generate BBE without jekyll front matter.
GEN_FOR_JEKYLL=""
# If true, Generate BBE for latest version hence ditch the version in perma link.
# If false, Generate BBE with version in permalink.
IS_LATEST_VERSION=""
# Ballerina distribution version
BALLERINA_VERSION="";

if [ -z "$BBE_GEN_DIR" ] && [ -z "$BAL_VERSION" ] && [ -z "$GEN_FOR_JEKYLL" ] && [ -z "$IS_LATEST_VERSION" ];
then
  site_folder="`jq -r '.version' $SITE_VERSION`"
  array=($(echo $site_folder | tr "." "\n"))
  SITE_VERSION="${array[0]}.${array[1]}"
  BBE_GEN_DIR="by-example"
  GEN_FOR_JEKYLL="true"
  IS_LATEST_VERSION="true"

  BALLERINA_VERSION=$site_folder
fi

go get github.com/russross/blackfriday

echo "-----------------------------------------------------------------------------------------------------------------------"
echo "curl https://dist-dev.ballerina.io/downloads/$BALLERINA_VERSION/ballerina-$BALLERINA_VERSION.zip --output ballerina.zip"
# curl https://dist-dev.ballerina.io/downloads/$BALLERINA_VERSION/ballerina-$BALLERINA_VERSION.zip --output ballerina.zip
unzip ballerina.zip

rm -rf target/dependencies/ballerina-examples
mkdir -p target/dependencies/ballerina-examples/
mv ./ballerina-$BALLERINA_VERSION/distributions/jballerina-$BALLERINA_VERSION/examples/index.json ballerinaByExample/tools/all-bbes.json
mv ./ballerina-$BALLERINA_VERSION/distributions/jballerina-$BALLERINA_VERSION/examples target/dependencies/ballerina-examples/

rm -rf $BBE_GEN_DIR
mkdir -p $BBE_GEN_DIR

echo "------------------------------------------------------------------------------------------------------------------------------------------------"
echo "go run ballerinaByExample/tools/generate.go target/dependencies/ballerina-examples $SITE_VERSION $BBE_GEN_DIR $GEN_FOR_JEKYLL $IS_LATEST_VERSION"
go run ballerinaByExample/tools/generate.go "target/dependencies/ballerina-examples" $SITE_VERSION $BBE_GEN_DIR $GEN_FOR_JEKYLL $IS_LATEST_VERSION
echo "....Completed building BBE Site...."

echo "-------------------------------------"
echo "rm -rf ./ballerina-$BALLERINA_VERSION"
rm -rf ./ballerina-$BALLERINA_VERSION
