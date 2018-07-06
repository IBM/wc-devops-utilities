# WebSphere Commerce DevOps Utilities #

WebSphere commerce DevOps Utilities is a reference tool chain to support deploying and operating WebSphere Commerce V9 in a Kubernetes environment.

For more information about WebSphere Commerce V9, see [WebSphere Commerce Version 9 knowledge Center](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/landing/wc_welcome.htm).

By using WebSphere Commerce DevOps Utilities, you can also deploy WebSphere Commerce V9+ in IBM Cloud Private (ICP). For more information on ICP, see [IBM Cloud Private](https://www.ibm.com/cloud/private).

WebSphere Commerce DevOps Utilities are built and deployed as Docker images, including the following:
* DeployController
* DeploySlave
* SupportContainer

Docker image |  Embedded assets  | Role and description
------------- | -------------| -------------
DeployController | Jenkins/ Pre-defined Jenkins job/ DevOps backend scripts |  A Jenkins-based tool to work as the controller to trigger related jobs and fulfill tasks such as environment deployment and Docker image build
DeploySlave  | Dockerd / Helm client / DevOps backend scripts | Can be triggered by DeployController to build customized Docker image including your customization package and can then be deployed in the Kubernetes environment  with Helm
SupportContainer | DevOps backend scripts | Handles Helm pre- and post-deployment hook/ Works as commander to control the startup sequence

Vault and Nexus Docker images, by default, are seamlessly integrated with the DevOps Utilities.

In the WebSphere Commerce DevOps utilities:

 * [Vault](https://www.vaultproject.io/) works as the Certification Agent to automatically issue certification as well as the remote configuration center to store environment related configurations. These configurations can be retrieved during Docker startup and set environment-specific configurations into the Docker container. For more information about Vault, see [Managing certificates with Vault](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/com.ibm.commerce.install.doc/refs/rigcertificates_vault.htm) and [Environment data structure in Consul/Vault](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/com.ibm.commerce.install.doc/refs/rigvaultmetadata.htm).

 * [Nexus](https://www.sonatype.com/nexus-repository-sonatype) works as the store to manage your customization packages. The customization packages are retrieved from Nexus and burned into the custom docker image when the custom Docker image is built.

You can deploy the DevOps Utilities by using Helm Chart. For more information about Helm Chart, see [Commerce DevOps Utilities Helm Charts](https://github.com/IBM/wc-helmchart)

The following diagram shows the components of the WebSphere Commerce using DevOps Utilities.
  <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/Overview.png" width = "700" height = "450" alt="Overview" align=center /><br>

<!--## Design ##

* [Architecture Design](doc/ArchitectureDesign.md) <br>
* [DeployController Design](doc/DeployControllerDesign.md) <br>
* [Utilites Design](doc/UtilitiesDesign.md) <br>
* [DeploySlave Design](doc/DeploySlaveDesign.md) <br>
* [SupportContainer Design](doc/SupportContainerDesign.md)-->

## Preparing Docker images for DevOps Utilities ##

Before you deploy WebSphere Commerce V9, build all required Docker images for WebSphere Commerce DevOps Utilities.

Before you run build Docker images, ensure that your machine has Docker (DockerCE or EE  17.06) installed and that your machine is connected to the Internet.

1. Go to the  `commerce-devops-utilities/kubernetes/DeployController` directory, and run the following command to build the DeployController Docker image:

        ./BuildDocker.sh

    **Note**: you can specify the Docker image tag in the following pattern:
        ./BuildDocker.sh deploycontroller:<newtag>

2. Go to the `commerce-devops-utilities/kubernetes/DeploySlave` directory, and run the following command to build the DeploySlave Docker image:

   ```
   ./BuildDocker.sh
   ```
    **Note**: You can specify the Docker image tag in the following pattern:
        ./BuildDocker.sh deployslave:<newtag>

3. Go to the  `commerce-devops-utilities/kubernetes/DeploySupport`directory, and run the following command to build the DeploySupport Docker image:
   ```
   ./BuildDocker.sh
   ```
   **Note**: You can specify the Docker image tag in the following pattern:
       ./BuildDocker.sh deploysuppor:<newtag>

## Deploying DevOps Utilites##

To quickly deploy DevOps Utilities, you need to use Helm Chart. For more information about Helm Chart, see [Commerce DevOps Utilities Helm Charts](https://github.com/IBM/wc-helmchart/tree/master/WCSDevOps).

Ensure to deploy WebSphere Commerce DevOps Utilities under the `default` Kubernetes namespace.

**Note**: If you already have a WebSphere Commerce V9 environment deployed, or you do not want to deploy Utilities on the Kubernetes cluster or ICP, you can also manually deploy each DevOps utilities container to serve your existing environments.

After the deployment is completed, you can access the DeployController user interface by logging into `http://IngressIPAddress:31899` with the default user name and password (`admin/admin`), and check the following pre-defined jobs:

<img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/DeployControllerJobList.png" width = "700" height = "450" alt="Overview" align=center /><br>

**Tip**:
 For each job in DeployController, make sure to open the `config` page and click `Save`, so that the Parameter plugin can be loaded.

## Using WebSphere Commerce Utilities ##

Refer to [DeployController design](doc/DeployControllerDesign.md) for detailed information.

##### Project structure  #####
Structure  |   Description
------------- | -------------
doc | Documents and pictures
kubernetes  | Scripts for building Docker images
utilities |  DevOps backend scripts

For DeployController<!--Tiffany:After reading through the list, I didn't get what it relates to the users. -->:
* Add new or updated plugin version in `commerce-devops-utilities/kubernetes/DeployController/plugins.txt`
* Modify the pre-defined Jenkins job under `commerce-deveops-utilities/kubernetes/DeployController/setup/jobs`
* Modify the default admin user by editing `commerce-deveops-utilities/kubernetes/DeployController/users/admin/config.xml`
* Modify global variables for Jenkins by editing `commerce-deveops-utilities/kubernetes/DeployController/config.xml`
* Modify Jenkins startup logic by modifying `jenkins.sh`


You can find DevOps backend scripts at:<br> `commerce-deveops-utilities/utilities`

## Contrbuting to the project ##

After you try the DevOps utilities out, you are welcomed to contribute to this project. If you'd like to do so, contact the administrators in [Contact List](CONTACT.md) so that you can be added as a project member.

## Support ##

* Creating issues

  You can create issues in this project or propose enhancements whenever needed. We will evaluate and assign contributors to fix or handle issues.

* Slack Channel

* To be added as a contributor, see the [Contact List](CONTACT.md).
