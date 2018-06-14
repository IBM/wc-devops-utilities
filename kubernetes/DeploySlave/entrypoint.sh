#!/bin/bash

echo "Configuring repo_name for Helm"

sed -i "/- caFile/{n;s/cache.*$/cache: \/root\/.helm\/repository\/cache\/$repo_name-index.yaml/g}" /root/.helm/repository/repositories.yaml

sed -i '/- caFile/{n;n;n;n;s/name.*$/name: "'$repo_name'"/g}'  /root/.helm/repository/repositories.yaml

echo "Repo_name has been updated to "$repo_name

echo "-----------------------------------------------"

echo "Configuring repo_url for Helm"

sed -i "s,url.*$,url: $repo_url,g" /root/.helm/repository/repositories.yaml

echo "Repo_url has been updated to "$repo_url


echo "The container is running normally"

tail -f /entrypoint.sh
