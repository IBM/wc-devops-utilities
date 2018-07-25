#! /bin/bash -e

# config vault_token if InCluster be specified in Container env parameter
echo "Avaliable environment: InCluster,vault_url,jenkins_server,cloud_url,jenkins_url,bundleRepo,dockerRepoHost,dockerRepoPwd,dockerRepoUser,helmChartsRepo"
if [ -n "${InCluster}" ] && [ "${InCluster}" == "true" ];then
  if [ -z "${vault_token}" ];then
     vault_token=$(python3.6 /usr/local/bin/vault.py)
     if [ -n "${vault_token}" ];then
        echo "begin to mount pki backend"
        data='{"type": "pki", "description": "SelfServe Root CA", "config": {"max_lease_ttl": "87600h"}}'
        curl --header "X-Vault-Token: $vault_token" --request POST --data "$data" http://vault-consul.default.svc:8200/v1/sys/mounts/selfserve_production_pki
        echo "Generate root ca"
        data='{"common_name": "selfserve_production_pki Root CA", "ttl": "87600h", "key_bits": "4096","exclude_cn_from_sans": "true"}'
        curl --header "X-Vault-Token: $vault_token" --request POST --data "$data" http://vault-consul.default.svc:8200/v1/selfserve_production_pki/root/generate/internal
        echo "Generate issue certificate role"
        data='{"key_bits": "2048", "max_ttl": "87600h", "allow_any_name": "true"}'
        curl --header "X-Vault-Token: $vault_token" --request POST --data "$data" http://vault-consul.default.svc:8200/v1/selfserve_production_pki/roles/generate-cert
     else
        echo "vault_token is empty."
     fi
  fi
  echo "-----change vault_token to : "  $vault_token
  sed -i '/vault_token/{n;s/string.*$/string>'$vault_token'<\/string>/g}' /var/jenkins_home/config.xml
fi

if [ -n "${VaultUrl}" ];then
  echo "-----change vault_url to  : " $VaultUrl
  sed -i '/vault_url/{n;s,string.*$,string>'$VaultUrl'<\/string>,g}' /var/jenkins_home/config.xml
else
  echo "no environment for VaultUrl, use default value http://vault-consul.default.svc:8200 "
fi

if [ -z "${InCluster}" ] && [ "${InCluster}" == "false" ];then
  echo "------change jenkins_server to : http://localhost:8080" 
  sed -i '/jenkins_server/{n;s,string.*$,string>http://localhost:8080<\/string>,g}' /var/jenkins_home/config.xml

  echo "--------change jenkins_url in cloud configuration to : http://localhost:8080" 
  sed -i "s,<jenkinsUrl.*$,<jenkinsUrl>http://localhost:8080<\/jenkinsUrl>,g" /var/jenkins_home/config.xml
fi

if [ -n "${KubernetesUrl}" ];then
  echo "--------change cloud_url to : " $KubernetesUrl
  sed -i "s,<serverUrl.*$,<serverUrl>$KubernetesUrl<\/serverUrl>,g" /var/jenkins_home/config.xml
else
  echo "no environment for KubernetesUrl, use default vaule https://kubernetes.default.svc"
fi

if [ -n "${BundleRepo}" ];then
  echo "--------update bundleRepo to : " $BundleRepo
  sed -i '/bundleRepo/{n;s,string.*$,string>'$BundleRepo'<\/string>,g}' /var/jenkins_home/config.xml
else
  echo "no environment for BundleRepo, use default value "
fi

if [ -n "${DockerRepo}" ];then
  echo "---------update Docker Repository to : "$DockerRepo
  sed -i '/dockerRepoHost/{n;s,string.*$,string>'$DockerRepo'<\/string>,g}' /var/jenkins_home/config.xml
else
  echo "no environment for dockerRepoHost, use default value "
fi

if [ -n "${DockerRepoPwd}" ];then
  echo "---------update DockerRepoPwd to : "$DockerRepoPwd
  sed -i '/dockerRepoPwd/{n;s,string.*$,string>'$DockerRepoPwd'<\/string>,g}' /var/jenkins_home/config.xml
else
  echo "no environment for DockerRepoPwd, use default value "
fi

if [ -n "${DockerRepoUser}" ];then
  echo "---------update DockerRepoUser to : "$DockerRepoUser
  sed -i '/dockerRepoUser/{n;s,string.*$,string>'$DockerRepoUser'<\/string>,g}' /var/jenkins_home/config.xml
else
  echo "no environment for DockerRepoUser, use default value "
fi

if [ -n "${HelmChartsRepo}" ];then
  echo "---------update HelmChartsRepo to : "$HelmChartsRepo
  sed -i '/helmChartsRepo/{n;s,string.*$,string>'$HelmChartsRepo'<\/string>,g}' /var/jenkins_home/config.xml
else
  echo "no environment for HelmChartsRepo, use default value "
fi

: "${JENKINS_WAR:="/usr/share/jenkins/jenkins.war"}"
: "${JENKINS_HOME:="/var/jenkins_home"}"
touch "${COPY_REFERENCE_FILE_LOG}" || { echo "Can not write to ${COPY_REFERENCE_FILE_LOG}. Wrong volume permissions?"; exit 1; }
echo "--- Copying files at $(date)" >> "$COPY_REFERENCE_FILE_LOG"
find /usr/share/jenkins/ref/ \( -type f -o -type l \) -exec bash -c '. /usr/local/bin/jenkins-support; for arg; do copy_reference_file "$arg"; done' _ {} +

#Worksaround to install active parameter plugin
cp /usr/share/jenkins/scriptler-2.9.hpi /var/jenkins_home/plugins
cp /usr/share/jenkins/uno-choice-1.5.3.hpi /var/jenkins_home/plugins

# if `docker run` first argument start with `--` the user is passing jenkins launcher arguments
if [[ $# -lt 1 ]] || [[ "$1" == "--"* ]]; then

  # read JAVA_OPTS and JENKINS_OPTS into arrays to avoid need for eval (and associated vulnerabilities)
  java_opts_array=()
  while IFS= read -r -d '' item; do
    java_opts_array+=( "$item" )
  done < <([[ $JAVA_OPTS ]] && xargs printf '%s\0' <<<"$JAVA_OPTS")

  jenkins_opts_array=( )
  while IFS= read -r -d '' item; do
    jenkins_opts_array+=( "$item" )
  done < <([[ $JENKINS_OPTS ]] && xargs printf '%s\0' <<<"$JENKINS_OPTS")

  exec java -Duser.home="$JENKINS_HOME" "${java_opts_array[@]}" -jar ${JENKINS_WAR} "${jenkins_opts_array[@]}" "$@"
fi

# As argument is not jenkins, assume user want to run his own process, for example a `bash` shell to explore this image
exec "$@"
