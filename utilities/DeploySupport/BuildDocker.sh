#!/bin/bash

cp -r ../../scripts/kube .
mv ./kube ./kube-python

if [ $# = 1 ];then
  docker build -t $1 .
else
  docker build -t 'deploycontroller:latest' .
fi

rm -rf ./kube-python