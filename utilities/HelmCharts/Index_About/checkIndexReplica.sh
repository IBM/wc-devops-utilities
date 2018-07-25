#!/bin/bash
curl -X GET -u spiuser:passw0rd https://searchrepeater.demoqalive.ibm.com/search/admin/resources/index/replicate/status?jobStatusId=$1 -k
