#/bin/bash
#
#
#
#
#
#
#
#
#
#`################################

#Get current directory
current_dir=$(pwd)
#Prepare files to build cross-image
cp $current_dir/EventAgent.go cross-build/
#Build cross-image
cd cross-build
docker build -t build-agent:latest .
rm $current_dir/cross-build/EventAgent.go
#Copy binary from cross-image to local directory
docker create --name build build-agent:latest

docker cp build:/go/EventAgent $current_dir/cross-build/
#clean build environment
docker rm build
#Prepare building eventagent image with binary
mv EventAgent $current_dir
cd $current_dir
docker build -t eventagent:latest .
#clean build environment
rm -rf EventAgent
