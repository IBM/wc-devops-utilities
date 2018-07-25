#!/bin/bash

if [ $# != 3 ]; then
   echo "please input the tenant_name enviornment_name environment_type. For example: ./vault-pop.sh demo qa auth"
   exit 0
fi

comm_dir=$(cd "$(dirname "$0")"; pwd)

source ./env.profile

# Get info from current kubernetes environment
vault_pod=$(kubectl  get po | grep vault.consul| awk '{print $1}')
pod_status=$(kubectl  get po | grep vault.consul| awk '{print $3}')
while [ $pod_status != "Running" ]
do pod_status=$(kubectl  get po | grep vault.consul| awk '{print $3}') && echo "waiting for vault_consul ready" && sleep 2s
done 

myuname=$(uname)
if [[ "$myuname" == "Darwin" ]]; then
	vault_token=$(kubectl logs $vault_pod -c vault |grep "Root Token:" | awk  '{print $3}' | sed -E "s/"$'\E'"\[([0-9]{1,2}(;[0-9]{1,2})*)?m//g")
	vault_port=$(kubectl get svc | grep vault-consul | awk '{print substr($4,6,5)}')
elif [[ "$myuname" == "Linux" ]]; then
	vault_token=$(kubectl logs $vault_pod -c vault |grep "Root Token:" | awk  '{print $3}' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})*)?m//g")
	vault_port=$(kubectl get svc | grep vault-consul | awk '{print substr($5,6,5)}')
else
	echo "Untested client operating system. Assuming Linux, but results may not be as expected."
	vault_token=$(kubectl logs $vault_pod -c vault |grep "Root Token:" | awk  '{print $3}' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})*)?m//g")
	vault_port=$(kubectl get svc | grep vault-consul | awk '{print substr($5,6,5)}')
fi


init_json='json_data={"type":"generic","description":"description","config":{"max_lease_ttl":"876000"}}'
header="X-Vault-Token:$vault_token"

# init vault and create mount point
echo "Creating mount point for "
sleep 1s
curl -X POST -H $header -H "Content-Type:application/json" -d '{"type":"generic","description":"description","config":{"max_lease_ttl":"876000"}}' http://$kube_minion_ip:$vault_port/v1/sys/mounts/$1


#pop
echo "push dbName to vault"
curl -X POST -H "$header" -d "{\"value\":\"$dbNameAuth\"}" http://$kube_minion_ip:$vault_port/v1/$1/$2/$3/dbName
sleep 1s

echo "push dbPassword to vault"
curl -X POST -H "$header" -d "{\"value\":\"$dbPasswordAuth\"}" http://$kube_minion_ip:$vault_port/v1/$1/$2/$3/dbPassword
sleep 1s


echo "push dbUser to vault"
curl -X POST -H "$header" -d "{\"value\":\"$dbUserAuth\"}" http://$kube_minion_ip:$vault_port/v1/$1/$2/$3/dbUser
sleep 1s

#post dbHost into vault and consul
echo "push dbPort into vault"
curl -X POST -H "$header" -d "{\"value\":\"$dbPortAuth\"}" http://$kube_minion_ip:$vault_port/v1/$1/$2/$3/dbPort
sleep 1s

echo "push dbHost into vault"
curl -X POST -H "$header" -d "{\"value\":\"$dbHostAuth\"}" http://$kube_minion_ip:$vault_port/v1/$1/$2/$3/dbHost
sleep 1s


#post domainName into vault and consul
echo "push domainName into vault" internalDomainName
curl -X POST -H "$header" -d "{\"value\":\"$internalDomainName\"}" http://$kube_minion_ip:$vault_port/v1/$1/$2/domainName

#Config PKI on vault and generate certs
#echo "Create a Root Cert"
#export VAULT_ADDR="http://$kube_minion_ip:$vault_port"
#export VAULT_TOKEN=$vault_token
#$comm_dir/Vault_Consul/vault mount -path=selfserve_production_pki -description="SelfServe Root CA" -max-lease-ttl=87600h pki
#$comm_dir/Vault_Consul/vault write selfserve_production_pki/root/generate/internal common_name="selfserve_production_pki Root CA" ttl=87600h  key_bits=4096 exclude_cn_from_sans=true
#$comm_dir/Vault_Consul/vault write  selfserve_production_pki/roles/generate-cert key_bits=2048  max_ttl=8760h allow_any_name=true

#echo "Init Vault and Consul successfully"
#echo -e "The Vault token is: " "\e[1;33m $vault_token \e[0m"
