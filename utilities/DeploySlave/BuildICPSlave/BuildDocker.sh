#!/bin/bash

mkdir -p ./commerce-devops-utilities
cp -r ../../../scripts ./commerce-devops-utilities

cp ./helm /usr/bin

if [ $# = 1 ];then
  docker build -t $1 .
else
  docker build -t 'deployslave:latest' .
fi

rm -rf ./commerce-devops-utilities
rm -rf ./helm
