from kubernetes import client, config
import time

config.load_incluster_config()
v1 = client.CoreV1Api()
count = 1
vault_name = ""
while (not vault_name):
    pods = v1.list_namespaced_pod("default")
    for k in pods.items:
        pod_name = k.metadata.name
        if pod_name[0:5] + "x" == "vaultx":
            vault_name = pod_name
    if (count > 5) and (not vault_name):
        exit(1)
    if(not vault_name):
        time.sleep(30)
        count += 1
    else:
        break
if (vault_name):
    ret = v1.read_namespaced_pod_log(vault_name, "default", container="vault")
    strin = ""
    for i in range(ret.find("Root Token") + 12, ret.find("Root Token") + 50):
        strin += ret[i]
    print(strin)