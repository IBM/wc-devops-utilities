#!/bin/bash

cp -r ../../utilities/kube .
mv ./kube ./kube-python

if [ $# = 1 ];then
  docker build -t $1 .
else
  docker build -t 'deploycontroller:latest' .
fi

rm -rf ./kube-python