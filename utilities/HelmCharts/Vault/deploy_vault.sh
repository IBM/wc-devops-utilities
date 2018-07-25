#!/bin/bash

current_dir=$(cd "$(dirname "$0")"; pwd)

# Deploy Vault and Consul.
echo "Deploying Vault and Consul"
kubectl create cm vault --from-file=$current_dir/Vault_Consul/config.json
kubectl create -f $current_dir/Vault_Consul/deployment.yaml
sleep 1s

# Push data to Vault
echo "Preparing data for auth in Vault_Consul"
source $current_dir/Vault_Consul/vault.sh

echo "https://cmc.demoqaauth.ibm.com/lobtools/cmc/ManagementCenter  for cmc"
echo "https://store.demoqaauth.ibm.com/wcs/shop/en/aururaesite  for store"

