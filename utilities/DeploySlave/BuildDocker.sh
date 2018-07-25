#!/bin/bash

helmVersion=v2.6.0

mkdir -p ./commerce-devops-utilities
cp -r ../../scripts ./commerce-devops-utilities

wget -O "./helm.tar.gz" https://storage.googleapis.com/kubernetes-helm/helm-${helmVersion}-linux-amd64.tar.gz
tar -zxvf helm.tar.gz
cp ./linux-amd64/helm .

if [ $# = 1 ];then
  docker build -t $1 .
else
  docker build -t 'deployslave:latest' .
fi

rm -rf ./commerce-devops-utilities
rm -rf ./helm.tar.gz
rm -rf ./helm
rm -rf ./linux-amd64