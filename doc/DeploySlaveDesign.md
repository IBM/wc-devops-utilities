# Deploy Slave Design #

## OverView ##
Deploy Slave be build as Jenkins slave. It includes doccker daemon, helm and pre-defined utiliies

Deploy slave is not like the deploy control, which is created by demand. Deploy Slave is a job executor, when a job is triggered
in jenkins master ui, one temporary slave pod will be created. Once the job is finished, the temporary slave pod will be 
deleted. This is very flexible. No job, no slave node which can help enhance resouce usage. 

## Requirement ##

In this project, the slave must can do the following things.

* Build docker image

* Get helm chart from chart repository and do helm deployment

* Execute pre-defined task

## Implement ##

Base on these requirements,  the deploy salve chooses "docker in docker" image as the base image.  This base image include
a simple daemon, which can do docker related actions in a docker container. This image can totally meet the first and most import
requirement. For the second and the third requirements, they are easy to implement. Add the helm binary file and configuration file
to the "docker in docker" image , copy the pre-defined scripts to it , install necessary runtime library. 

The pre-defined scripts are wrote by python, which can be used to communicate with kubenetes master server and supoort deployment flow.

## Build DeploySlave For Helm TLS ##

### Background ###

Helm server support to enable TLS. ( Since `ICP 2.1.0.3`, Helm TLS has been enabled as default ). It require helm client command must have '--tls' in parameters.

and put the certification on your helm local folder.  In DevOps Utilities, helm client be embedded into DeploySlave. As default it not have the certification files. So if your


### Objective ###

This doc will guide how to rebuild DeploySlave for using DevOps Utilities in ICP 2.1.0.3

### Steps ###

1. Logon ICP Master node and copy helm binary file under /user/bin and copy helm file to commerce-devops-utilities/kubernetes/DeploySlave/BuildICPSlave ( ICP customized Helm, so you must use ICP helm client )
2. Get certification files on ICP Master node under path /root/.helm ( ca.pem / cer.pem / key.pem ) and copy those files to commerce-devops-utilities/kubernetes/DeploySlave/BuildICPSlave/certs
3. Run BuildDocker.sh under path commerce-devops-utilities/kubernetes/DeploySlave/BuildICPSlave