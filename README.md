# Commerce DevOps Utilities #

Commerce DevOps Utilities，as a sample tool chain for reference, support Commerce V9+ deploy on Kubernetes, see [Commerce Version 9](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/landing/wc_welcome.htm)

Commerce DevOps Utilities also can well support Commerce V9+ deploy on IBM Cloud Private, see [IBM Cloud Private](https://www.ibm.com/cloud/private)

Commerce DevOps Utilities will be build and deploy as Docker container. It includes DeployController, DeploySlave and SupportContainer

Docker Image  |  Embed Assets  | Usage
------------- | -------------| -------------
DeployController | Jenkins / Pre defined Job / DevOps backend scripts |  As the Controller to trigger related Jobs.
DeploySlave  | Dockerd / Helm client / DevOps backend scripts | Triggered by DeployController to build customized docker image and deploy with helm
SupportContainer | DevOps backend scripts | handle helm pre and post install hook / as InitContainer to controller startup sequence

Vault and Nexus Docker image, as default integration with DevOps Utilities. [Vault](https://www.vaultproject.io/) will be the Certification Agent to auto issue certification and Remote Configuration Center to store
environment related configuration. [Nexus](https://www.sonatype.com/nexus-repository-sonatype) will store /  manage customization package and support build customization Docker Image.

For quick deploy HelmChart be provided. see [Commerce DevOps Utilities Helm Charts](https://github.com/IBM/wc-helmchart)

  <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/Overview.png" width = "700" height = "450" alt="Overview" align=center /><br>

## Build  ##

Note: before you run build, make user your machine has installed Docker ( DockerCE or EE  17.06 ) and You can connect to internet well

1. Located to path `commerce-devops-utilities/kubernetes/DeployController` and run command to build DeployController Docker image

    ```
    ./BuildDocker.sh

    ( you can specify docker image tag by ./BuildDocker.sh deploycontroller:newtag )
    ```

2. Located to path `commerce-devops-utilities/kubernetes/DeploySlave` and run command to build DeploySlave Docker image

   ```
   ./BuildDocker.sh

   ( you can specify docker image tag by ./BuildDocker.sh deployslave:newtag )
   ```

3. Located to path `commerce-devops-utilities/kubernetes/DeploySupport` and run command to build DeploySupport Docker image
   ```
   ./BuildDocker.sh

   ( you can specify docker image tag by ./BuildDocker.sh deploysupport:newtag )
   ```

## Deploy ##

For quick deploy HelmChart be provided. see [Commerce DevOps Utilities Helm Charts](https://github.com/IBM/wc-helmchart)

Please deploy Commerce DevOps Utilities under `default` namespace. Otherwise you need to create BACE to make the backend scripts has right permission

You can access DeployController UI through `http://IngressIPAddress:31899`, default user and accound is `admin/admin`

IF you already have a environment or you don't want to deploy Utilities inside of Kubernetes cluster ( or IBM Cloud Private ), you can choose manually
deploy each container. For how to configure please reference Helm Charts


## Usage ##

See [Commerce DevOps Utilities End2End Usage](doc/End2EndUsage.md)

## Development ##

You are welcome to contribute to this project.  Please contact the admin in Contact List to add you as the member.

##### Project Structure  #####
Structure  |   Usage
------------- | -------------
doc | Document and Pictures
kubernetes  | Scripts for build Docker Images
utilities |  DevOps backend scripts

For DeployController:
* Add new or update plugin version in commerce-devops-utilities/kubernetes/DeployController/plugins.txt
* Modify the pre defined Jenkins job under path commerce-deveops-utilities/kubernetes/DeployController/setup/jobs
* Modify the default admin user by edit commerce-deveops-utilities/kubernetes/DeployController/users/admin/config.xml
* Modify global variables for Jenkins by edit commerce-deveops-utilities/kubernetes/DeployController/config.xml
* Modify jenkins startup logic by modify jenkins.sh


For DevOps backend scripts:<br>
They are be put under `commerce-deveops-utilities/utilities`


## Support ##

* Issue Report

  You can create issue in this project or raise a new enhancement. We will evaluate and assign contributor to fix or handle it

* Slack Channel


* [Contact List](CONTACT.md)
