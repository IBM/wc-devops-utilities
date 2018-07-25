#!/bin/bash
mkdir -p ./commerce-devops-utilities
cp -r ../../scripts ./commerce-devops-utilities

if [ $# = 1 ];then
  docker build -t $1 .
else
  docker build -t 'deploycontroller:latest' .
fi

rm -rf ./commerce-devops-utilities