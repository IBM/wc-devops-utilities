#!/bin/bash

#global variable
componentType="";

#update index name in the sample filebeat.yml
function updateIndexName(){
	echo "Start to change Index Name to $1"
	sed -i "s/sampleIndex/$1/g" /etc/filebeat_search_store.yml
	sed -i "s/sampleIndex/$1/g" /etc/filebeat_ts_app.yml
	sed -i "s/sampleIndex/$1/g" /etc/filebeat_ts_web.yml
	echo "Update Index Name Done"
}

#update ElasticSearch in the sample filebeat.yml
function updateTargetELK(){
	echo "Start to change target ElasticSearch to $1"
	sed -i "s/targetElkHost/$1/g" /etc/filebeat_search_store.yml
	sed -i "s/targetElkHost/$1/g" /etc/filebeat_ts_app.yml
	sed -i "s/targetElkHost/$1/g" /etc/filebeat_ts_web.yml
	echo "Update Target ES Done"
}

#show the usage if input parameters is incorrect
function usage(){
	echo "The expected parameter are"
	echo "   -indexName <The_Index_Name>"
	echo "   -targetELK <The_ELK_Hostname>"
}
if [ -f "/etc/filebeat/filebeat_cus.yml" ]; then
	echo Launch Filbeat with customized yml file...
	exec filebeat -c /etc/filebeat/filebeat_cus.yml
	exit 0
fi


#change file permission
chmod go-w /etc/filebeat_search_store.yml
chmod go-w /etc/filebeat_ts_app.yml
chmod go-w /etc/filebeat_ts_web.yml

#get the parameters from pipeline, update Index Name and Target ElasticSearch
while [ -n "$1" ]
do
	case "$1" in
		-indexName) indexName=$2; updateIndexName $indexName; shift 2;;
		-targetELK) targetELK=$2; updateTargetELK $targetELK; shift 2;;
		-componentType) componentType=$2; shift 2;;
		*) usage; break;;
	esac
done

#launch filebeat by componentType
case $componentType in
	search-app-master) exec filebeat -c /etc/filebeat_search_store_xc.yml;;
	search-app-repeater) exec filebeat -c /etc/filebeat_search_store_xc.yml;;
	search-app-slave) exec filebeat -c /etc/filebeat_search_store_xc.yml;;
	xc-app) exec filebeat -c /etc/filebeat_search_store_xc.yml;;
	crs-app) exec filebeat -c /etc/filebeat_search_store_xc.yml;;
	ts-app) exec filebeat -c /etc/filebeat_ts_app.yml;;
	ts-web) exec filebeat -c /etc/filebeat_ts_web.yml;;
	*) echo incorrect componentType '"'$componentType'"'
esac
