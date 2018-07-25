import os
import sys
import json
import time
import argparse
import requests
from requests import Request,Session
from requests.auth import HTTPBasicAuth

# Get ts url from args
cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("tenant_id", help="The tenant_id is used to create a unique group and two Jobs")
cmd_parser.add_argument("environment", help="The environment name")
cmd_parser.add_argument("envtype", help="the environment type, live or auth")
cmd_parser.add_argument("namespace", default="default", help="speicfy the namespace of applicagtion")

# TODO need to support multiple catalogID input
cmd_parser.add_argument("masterCatalogId", default="10001", help="speicfy master catalog ID which need to build index")
cmd_parser.add_argument("spiuser", default="spiuser", help="speicfy spiuser name")
cmd_parser.add_argument("spipwd", default="passw0rd", help="speicfy spiuser password")

args = cmd_parser.parse_args()

# Connect ts-server to get jobStatusID
ts_url = "https://"+args.tenant_id+args.environment+args.envtype+"ts-app."+args.namespace+".svc.cluster.local:5443/wcs/resources/admin/index/dataImport/build?masterCatalogId="+args.masterCatalogId

ts_auth = HTTPBasicAuth(args.spiuser, args.spipwd)

ts_r = requests.post(url=ts_url, data={}, auth=ts_auth, verify=False)
print(ts_r)
content = ts_r.json()
statusID = content['jobStatusId']
print(statusID)

# Verify build index status rest call
# Please be aware, since 9.0.0.1, the search api start to support https and 3738 port
search_url = "https://"+args.tenant_id+args.environment+args.envtype+"search-app-master."+args.namespace+".svc.cluster.local:3738/search/admin/resources/index/build/status?jobStatusId="+statusID

search_auth = HTTPBasicAuth(args.spiuser, args.spipwd)
count = 0

while True:
    search_r = requests.get(url=search_url, auth=search_auth, verify=False)

    progress = search_r.json()
    # print(progress)
    status = progress['status']
    time.sleep(5)
    count += 1
    if int(status) == 0:
        print("Indexing job finished successfully for masterCatalogId:10001.")
        break
    if count == 300:
        print("Time Out for this build, please try again.")
        break
    print("CatalogEntry indexing process is still in progress")
