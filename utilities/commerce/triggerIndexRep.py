import json
import time
import argparse
import requests
from requests.auth import HTTPBasicAuth

#Get ts url from args
cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("tenant_id", help="The tenant_id is used to create a unique group and two Jobs")
cmd_parser.add_argument("environment", help="The environment name")
cmd_parser.add_argument("namespace", help="Specify the target namespace for environment")
cmd_parser.add_argument("spiuser", help="Specify spiuser name")
cmd_parser.add_argument("spipwd", help="Specify spiuser password")

args = cmd_parser.parse_args()
trigger_auth = HTTPBasicAuth(args.spiuser, args.spipwd)
#Connect search-replica to get jobStatusID searchrptsecure-demoqalive.cn.ibm.com
triggerUrl = "https://"+args.tenant_id+args.environment+"livesearch-app-repeater."+args.namespace+".svc.cluster.local:3738/search/admin/resources/index/replicate"

triggerRes = requests.post(url = triggerUrl, auth = trigger_auth, verify = False)
triggerJson = triggerRes.json()
jobStatusID = triggerJson['jobStatusId']
print(triggerRes)
#verify build index status rest call

search_url = "https://"+args.tenant_id+args.environment+"livesearch-app-repeater."+args.namespace+".svc.cluster.local:3738/search/admin/resources/index/replicate/status?jobStatusId="+str(jobStatusID)

count = 0

while True:
    search_r = requests.get(url=search_url, auth=trigger_auth, verify=False)

    progress = search_r.json()
    print(progress)
    status = progress['status']
    time.sleep(5)
    count += 1
    if int(status) == 0:
        print("Indexing replicate finished successfully for masterCatalogId:"+ str(jobStatusID) +".")
        break
    if count == 30:
        print("Time Out for this build, please try again.")
        break
    print("replicate indexing process is still in progress")
