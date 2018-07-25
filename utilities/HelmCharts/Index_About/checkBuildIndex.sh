#!/bin/bash
curl -X GET -u spiuser:passw0rd https://search.demoqaauth.ibm.com/search/admin/resources/index/build/status?jobStatusId=$1 -k
