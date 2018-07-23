# Deploy Slave design #

## Overview ##
Deploy Slave is built as a Jenkins slave. It includes doccker daemon, Helm and pre-defined utilities.

Unlike the Deploy Controller, which is created on demand, a Deploy Slave pod is created when a job is triggered in the Jenkins master ui. When the job is done, the temporary slave pod will be
deleted.

## Requirement ##

In this project, a Deploy Slave can perform the following tasks:

* Build the Docker image

* Get Helm Chart from the chart repository and deploy Helm

* Execute pre-defined tasks

## Implementation ##

Base on the requirements, the "docker in docker" image is the base image of the Deploy Salve. A "docker in docker" image includes a daemon to perform docker-related tasks in a Docker container. You can add the Helm binary file and configuration file
to the "docker in docker" image, copy the pre-defined scripts to the image, and install necessary runtime library to perform other tasks.

The pre-defined scripts are created with Python for the communication with the Kubenetes master server and deployment flow support.

## Building DeploySlave for Helm TLS ##

### Background ###

The Helm server supports TLS. Starting from `ICP 2.1.0.3`, Helm TLS is enabled by default.

To support TLS, it is required that the Helm client command has the '--tls' parameter enabled and certificates are in your local Helm folder. In the deployment utilities, the Helm client is embedded into DeploySlave. By default, DeploySlave does not have the certificate files. Thus if your current environment has TLS enabled, you have to rebuild DeploySlave.

To rebuild DeploySlave to use deployment utilities in the ICP 2.1.0.3 environment:

### Steps ###

1. Log into the ICP Master node and copy the Helm binary file from `/user/bin` and copy the Helm file to `commerce-devops-utilities/kubernetes/DeploySlave/BuildICPSlave`.

   **Note**: Because ICP customizes Helm, make sure to use the ICP Helm client.
2. Copy the certificate files on ICP Master node from `/root/.helm` ( `ca.pem / cer.pem / key.pem` ) to `commerce-devops-utilities/kubernetes/DeploySlave/BuildICPSlave/certs`.
3. Run `BuildDocker.sh` in `commerce-devops-utilities/kubernetes/DeploySlave/BuildICPSlave`.
