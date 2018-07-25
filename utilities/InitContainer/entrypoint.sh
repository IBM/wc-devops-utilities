#!/bin/bash

start_tm=$(date +%s%N)
time_out=0
if [ "$ENVTYPE"x = "live"x ];then
  if [ "$COMPONENT"x = "crs-app"x ];then
  until [ $(curl -I -s https://{$TENANT}{$ENVNAME}livesearch-app-slave.$NAMESPACE.svc.cluster.local:3738/search/admin/resources/health/status?type=container "-k|head -1"|cut -d " " -f2)x = "200"x ] || [ $time_out -eq 1 ]
    do echo "waiting for search-service ready"
       sleep 5s
       end_tm=$(date +%s%N)
       use_tm=$(echo $end_tm $start_tm | awk '{ print ($1 - $2) /6000000000 }')
       use_tm=$(printf "%.f" $use_tm)
       time_out=$(echo "$use_tm > 5" | bc)
  done

  else
  until [ $(curl -I -s https://{$TENANT}{$ENVNAME}livets-app.$NAMESPACE.svc.cluster.local:5443/webapp/wcs/stores/servlet/swagger/index.jsp -k|head -1|cut -d " " -f2)x = "200"x ] || [ $time_out -eq 1 ]
    do echo "waiting for tsapp-service ready"
       sleep 5s
       end_tm=$(date +%s%N)
       use_tm=$(echo $end_tm $start_tm | awk '{ print ($1 - $2) /60}')
       use_tm=$(printf "%.f" $use_tm)
       time_out=$(echo "$use_tm > 10" | bc)
  done
  fi
else
  if [ "$COMPONENT"x = "crs-app"x ];then
  until [ $(curl -I -s https://{$TENANT}{$ENVNAME}authsearch-app-master.$NAMESPACE.svc.cluster.local:3738/search/admin/resources/health/status?type=container -k|head -1|cut -d " " -f2)x = "200"x ] || [ $time_out -eq 1 ]
    do echo "waiting for search-service ready"
       sleep 5s
       end_tm=$(date +%s%N)
       use_tm=$(echo $end_tm $start_tm | awk '{ print ($1 - $2) /6000000000 }')
       use_tm=$(printf "%.f" $use_tm)
       time_out=$(echo "$use_tm > 5" | bc)
  done

  else
  until [ $(curl -I -s https://{$TENANT}{$ENVNAME}authts-app.$NAMESPACE.svc.cluster.local:5443/webapp/wcs/stores/servlet/swagger/index.jsp -k|head -1|cut -d " " -f2)x = "200"x ] || [ $time_out -eq 1 ]
    do echo "waiting for tsapp-service ready"
       sleep 5s
       end_tm=$(date +%s%N)
       use_tm=$(echo $end_tm $start_tm | awk '{ print ($1 - $2) /60}')
       use_tm=$(printf "%.f" $use_tm)
       time_out=$(echo "$use_tm > 10" | bc)
  done
  fi
fi
