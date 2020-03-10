#!/bin/sh
echo ".....Building BBE Site....."
rm -rf $2
mkdir -p $2
mkdir -p $2/withfrontmatter
mkdir -p $2/withoutfrontmatter
#export GOPATH=$3
go get github.com/russross/blackfriday
rm -rf target/dependencies/ballerina-examples

#get BBE from the language master branch
rm -rf ballerina-lang
git clone https://github.com/ballerina-platform/ballerina-lang
git --git-dir=ballerina-lang/.git --work-tree=ballerina-lang/ checkout v1.1.0
mkdir -p target/dependencies/ballerina-examples/
mv ballerina-lang/examples target/dependencies/ballerina-examples/examples/
rm -rf ballerina-lang

#get BBE from BallerinaX
rm -rf docker
git clone https://github.com/ballerinax/docker
git --git-dir=docker/.git --work-tree=docker/ checkout v1.1.0
mkdir -p target/dependencies/ballerina-examples/examples
mv docker/docker-extension-examples/examples/* target/dependencies/ballerina-examples/examples/
rm -rf docker

rm -rf kubernetes
git clone https://github.com/ballerinax/kubernetes
git --git-dir=kubernetes/.git --work-tree=kubernetes/ checkout v1.1.0
mkdir -p target/dependencies/ballerina-examples/examples
mv kubernetes/kubernetes-extension-examples/examples/* target/dependencies/ballerina-examples/examples/
rm -rf kubernetes

rm -rf jdbc
git clone https://github.com/ballerinax/jdbc
git --git-dir=jdbc/.git --work-tree=jdbc/ checkout v1.1.0
mkdir -p target/dependencies/ballerina-examples/examples
mv jdbc/jdbc-extension-examples/examples/* target/dependencies/ballerina-examples/examples/
rm -rf jdbc

rm -rf awslambda
git clone https://github.com/ballerinax/awslambda
git --git-dir=awslambda/.git --work-tree=awslambda/ checkout v1.1.0
mkdir -p target/dependencies/ballerina-examples/examples
mv awslambda/awslambda-examples/examples/* target/dependencies/ballerina-examples/examples/
mkdir -p target/dependencies/ballerina-examples/examples/awslambda-deployment

mv target/dependencies/ballerina-examples/examples/aws-lambda-deployment/aws_lambda_deployment.bal target/dependencies/ballerina-examples/examples/awslambda-deployment/awslambda_deployment.bal
mv target/dependencies/ballerina-examples/examples/aws-lambda-deployment/aws_lambda_deployment.description target/dependencies/ballerina-examples/examples/awslambda-deployment/awslambda_deployment.description
mv target/dependencies/ballerina-examples/examples/aws-lambda-deployment/aws_lambda_deployment.out target/dependencies/ballerina-examples/examples/awslambda-deployment/awslambda_deployment.out

rm -rf awslambda

# $1 arg is the version of the Ballerina that these BBEs are belongs to. ex: v1-1 or v1-0
# $2 arg is the location where the generated files suppose to be placed.
go run tools/ballerinaByExample/tools/generate.go "tools/target/dependencies/ballerina-examples" $1 $2
echo "....Completed building BBE Site...."
