#!/bin/bash
echo ".....Building BBE Site....."

BASEDIR=$(dirname $0)
# SITE_VERSION is the version of the Ballerina that these BBEs are belongs to. ex: v1-1 or v1-0
SITE_VERSION=$1
# BBE_GEN_DIR is the location where the generated files will be placed.
BBE_GEN_DIR=$2
# Ballerina version to be checkout from git. ex: v1.2.0
BAL_VERSION=$3
# If true, Generate BBE with jekyll front matter. If false, Generate BBE without jekyll front matter.
GEN_FOR_JEKYLL=$4
# If true, Generate BBE for latest version hence ditch the version in perma link.
# If false, Generate BBE with version in permalink.
IS_LATEST_VERSION=$5


if [ -z "$BBE_GEN_DIR" ] && [ -z "$BAL_VERSION" ] && [ -z "$GEN_FOR_JEKYLL" ] && [ -z "$IS_LATEST_VERSION" ];
then
  site_folder="`jq -r '.version' $SITE_VERSION`"
  array=($(echo $site_folder | tr "." "\n"))
  SITE_VERSION="${array[0]}.${array[1]}"
  BBE_GEN_DIR="by-example"
  BAL_VERSION="v${site_folder}"
  GEN_FOR_JEKYLL="true"
  IS_LATEST_VERSION="true"
fi

rm -rf $BBE_GEN_DIR
mkdir -p $BBE_GEN_DIR

go get github.com/russross/blackfriday
rm -rf target/dependencies/ballerina-examples

#get BBE from the language master branch
rm -rf ballerina-lang
git clone https://github.com/ballerina-platform/ballerina-lang
echo "checkout Ballerina lang repo: $BAL_VERSION"
git --git-dir=ballerina-lang/.git --work-tree=ballerina-lang/ checkout $BAL_VERSION
mkdir -p target/dependencies/ballerina-examples/

mv ballerina-lang/examples target/dependencies/ballerina-examples/examples/
rm -rf ballerina-lang

#get BBE from BallerinaX
rm -rf docker
git clone https://github.com/ballerinax/docker
echo "checkout BallerinaX docker repo: $BAL_VERSION"
git --git-dir=docker/.git --work-tree=docker/ checkout $BAL_VERSION
mkdir -p target/dependencies/ballerina-examples/examples
mv docker/docker-extension-examples/examples/* target/dependencies/ballerina-examples/examples/
rm -rf docker

rm -rf kubernetes
git clone https://github.com/ballerinax/kubernetes
echo "checkout BallerinaX kubernetes repo: $BAL_VERSION"
git --git-dir=kubernetes/.git --work-tree=kubernetes/ checkout $BAL_VERSION
mkdir -p target/dependencies/ballerina-examples/examples
mv kubernetes/kubernetes-extension-examples/examples/* target/dependencies/ballerina-examples/examples/
rm -rf kubernetes

rm -rf jdbc
git clone https://github.com/ballerinax/jdbc
echo "checkout BallerinaX jdbc repo: $BAL_VERSION"
git --git-dir=jdbc/.git --work-tree=jdbc/ checkout $BAL_VERSION
mkdir -p target/dependencies/ballerina-examples/examples
mv jdbc/jdbc-extension-examples/examples/* target/dependencies/ballerina-examples/examples/
rm -rf jdbc

rm -rf awslambda
git clone https://github.com/ballerinax/awslambda
echo "checkout BallerinaX aws lambda repo: $BAL_VERSION"
git --git-dir=awslambda/.git --work-tree=awslambda/ checkout $BAL_VERSION
mkdir -p target/dependencies/ballerina-examples/examples
mv awslambda/awslambda-examples/examples/* target/dependencies/ballerina-examples/examples/
mkdir -p target/dependencies/ballerina-examples/examples/awslambda-deployment

mv target/dependencies/ballerina-examples/examples/aws-lambda-deployment/aws_lambda_deployment.bal target/dependencies/ballerina-examples/examples/awslambda-deployment/awslambda_deployment.bal
mv target/dependencies/ballerina-examples/examples/aws-lambda-deployment/aws_lambda_deployment.description target/dependencies/ballerina-examples/examples/awslambda-deployment/awslambda_deployment.description
mv target/dependencies/ballerina-examples/examples/aws-lambda-deployment/aws_lambda_deployment.out target/dependencies/ballerina-examples/examples/awslambda-deployment/awslambda_deployment.out

rm -rf awslambda

go run ballerinaByExample/tools/generate.go "target/dependencies/ballerina-examples/examples" $SITE_VERSION $BBE_GEN_DIR $GEN_FOR_JEKYLL $IS_LATEST_VERSION
echo "....Completed building BBE Site...."
