import os
import sys
import json
import time
import argparse
import requests
import kube_vars as globalvars
from requests import Request,Session
from requests.auth import HTTPBasicAuth


def buildIndex(parser_args):
    indexDomainName = parser_args.tenant+parser_args.env+"authts-app"
    buildIndexUrl = "https://"+indexDomainName+":5443/wcs/resources/admin/index/dataImport/build?masterCatalogId="+parser_args.masterCatalogId
    print("build Index url is %s" %(buildIndexUrl), flush=True)
    headers = {"Authorization": "Basic " + parser_args.spiEncryptedToken}
    buildIndexResponse = requests.post(url=buildIndexUrl, data={}, headers=headers,verify=False)
    jsonBody = buildIndexResponse.json()
    print("build index response %s" %(jsonBody),flush=True)
    jobID = jsonBody['jobStatusId']
    checkStatusDoaminName=parser_args.tenant+parser_args.env+"authsearch-app-master"
    checkStatusUrl = "https://"+checkStatusDoaminName+":3738/search/admin/resources/index/build/status?jobStatusId="+str(jobID)
    checkBuildStatus(checkStatusUrl,headers, jobID)

def replicaIndex(parser_args):
    indexDomainName = parser_args.tenant+parser_args.env+"livesearch-app-repeater"
    replicaIndexUrl = "https://"+indexDomainName+":3738/search/admin/resources/index/replicate"
    print("replica Index url is %s" %(replicaIndexUrl),flush=True)
    headers = {"Authorization": "Basic " + parser_args.spiEncryptedToken}
    replicaResponse = requests.post(url=replicaIndexUrl, data={}, headers=headers,verify=False)
    jsonBody = replicaResponse.json()
    print("replica index response %s" %(jsonBody),flush=True)
    jobID = jsonBody['jobStatusId']
    checkStatusDoaminName=parser_args.tenant+parser_args.env+"livesearch-app-repeater"
    checkStatusUrl = "https://"+checkStatusDoaminName+":3738/search/admin/resources/index/replicate/status?jobStatusId="+str(jobID)
    checkBuildStatus(checkStatusUrl, headers, jobID)

def checkBuildStatus(url,headers,jobID):
    print("check index status url is %s" %(url))
    count = 0
    while True:
        statusResponse = requests.get(url=url, data={}, headers=headers,verify=False)
        jsonBody = statusResponse.json()
        print("status check response is %s" %(jsonBody),flush=True)
        status = jsonBody['status']
        if int(status) == 0:
           print("The job %s build index successfully" %(jobID),flush=True)
           break
        else:
           time.sleep(60)
           if count == 120:
              print("The job %s build index time out" %(jobID),flush=True)
              break
           count += 1
           print("The job %s is building index" %(jobID),flush=True)

# Init subparser for dependence check related command
buildIndexSubParser = globalvars.get_value('SubCMDParser')

buildIndexParser = buildIndexSubParser.add_parser('buildIndex', help='build search master index in auth enviroment')
buildIndexParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
buildIndexParser.add_argument('-env', type=str, default='qa', help='specify the environment name, default value is qa')
buildIndexParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
buildIndexParser.add_argument('-masterCatalogId', type=str, default='default', help='master catalog Id')
buildIndexParser.add_argument('-spiEncryptedToken', type=str, default='c3BpdXNlcjpwYXNzdzByZA==', help='specfy encrypted spiuser password str by command: echo -n "spiuser:password" | base64')
buildIndexParser.set_defaults(func=buildIndex)

globalvars.set_value('SubCMDParser',buildIndexSubParser)

replicaIndexSubParser = globalvars.get_value('SubCMDParser')

replicaIndexParser = replicaIndexSubParser.add_parser('replicaIndex', help='build search master index in auth enviroment')
replicaIndexParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
replicaIndexParser.add_argument('-env', type=str, default='qa', help='specify the environment name, default value is qa')
replicaIndexParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
replicaIndexParser.add_argument('-masterCatalogId', type=str, default='default', help='master catalog Id')
replicaIndexParser.add_argument('-spiEncryptedToken', type=str, default='c3BpdXNlcjpwYXNzdzByZA==', help='specfy encrypted spiuser password str by command: echo -n "spiuser:password" | base64')
replicaIndexParser.set_defaults(func=replicaIndex)

globalvars.set_value('SubCMDParser',replicaIndexSubParser)
