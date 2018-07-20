# Deploying WebSphere Commerce V9 with the deployment utilities #

WebSphere commerce deployment utilities are provided as a reference tool chain to support deploying and operating WebSphere Commerce V9 in a Kubernetes environment.

For more information about WebSphere Commerce V9, see [WebSphere Commerce Version 9 knowledge Center](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/landing/wc_welcome.htm).

By using WebSphere Commerce deployment utilities, you can also deploy WebSphere Commerce V9+ in IBM Cloud Private (ICP). For more information on ICP, see [IBM Cloud Private](https://www.ibm.com/cloud/private).

WebSphere Commerce deployment utilities are built and deployed as Docker images, including the following:
* DeployController
* DeploySlave
* SupportContainer

Docker image |  Embedded assets  | Role and description
------------- | -------------| -------------
DeployController | Jenkins/ Pre-defined Jenkins job/ DevOps backend scripts |  A Jenkins-based tool to work as the controller to trigger related jobs and fulfill tasks such as environment deployment and Docker image build
DeploySlave  | Dockerd / Helm client / DevOps backend scripts | Can be triggered by DeployController to build customized Docker image including your customization package and can then be deployed in the Kubernetes environment  with Helm
SupportContainer | DevOps backend scripts | Handles Helm pre- and post-deployment hook/ Works as commander to control the startup sequence

Vault and Nexus Docker images, by default, are seamlessly integrated with the deployment utilities.

In the WebSphere Commerce deployment utilities:

 * [Vault](https://www.vaultproject.io/) works as the Certification Agent to automatically issue certification as well as the remote configuration center to store environment related configurations. These configurations can be retrieved during Docker startup and set environment-specific configurations into the Docker container. For more information about Vault, see [Managing certificates with Vault](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/com.ibm.commerce.install.doc/refs/rigcertificates_vault.htm) and [Environment data structure in Consul/Vault](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/com.ibm.commerce.install.doc/refs/rigvaultmetadata.htm).

 * [Nexus](https://www.sonatype.com/nexus-repository-sonatype) works as the store to manage your customization packages. The customization packages are retrieved from Nexus and burned into the custom docker image when the custom Docker image is built.

<!--You can deploy the deployment utilities by using Helm Chart. For more information about Helm Chart, see [Commerce deployment utilities Helm Charts](https://github.com/IBM/wc-helmchart)-->

The following diagram shows the components of the WebSphere Commerce using deployment utilities.
  <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/Overview.png" width = "700" height = "450" alt="Overview" align=center /><br>

<!--## Design ##

* [Architecture Design](doc/ArchitectureDesign.md) <br>
* [DeployController Design](doc/DeployControllerDesign.md) <br>
* [Utilites Design](doc/UtilitiesDesign.md) <br>
* [DeploySlave Design](doc/DeploySlaveDesign.md) <br>
* [SupportContainer Design](doc/SupportContainerDesign.md)-->

## Preparing Docker images for deployment utilities ##

Before you deploy WebSphere Commerce V9, build all required Docker images for WebSphere Commerce deployment utilities.

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

## Deploying DevOps Utilites ##

<!--To quickly deploy deployment utilities, you need to use Helm Chart. For more information about Helm Chart, see [Commerce DevOps Utilities Helm Charts](https://github.com/IBM/wc-helmchart/tree/master/WCSDevOps).-->

Ensure to deploy WebSphere Commerce DevOps Utilities under the `default` Kubernetes namespace.

**Note**: If you already have a WebSphere Commerce V9 environment deployed, or you do not want to deploy Utilities on the Kubernetes cluster or ICP, you can also manually deploy each DevOps utilities container to serve your existing environments.

After the deployment is completed, you can access the DeployController user interface by logging into `http://IngressIPAddress:31899` with the default user name and password (`admin/admin`), and check the following pre-defined jobs:

<img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/DeployControllerJobList.png" width = "700" height = "450" alt="Overview" align=center /><br>

**Tip**:
 For each job in DeployController, make sure to open the `config` page and click `Save`, so that the Parameter plugin can be loaded.

## Using WebSphere Commerce Utilities ##

Refer to [DeployController design](doc/DeployControllerDesign.md) for detailed information.

### Project structure  ###
The following table shows the folders included in the project.

Folder |   Description
------------- | -------------
doc | Includes documents created in Markdown
kubernetes*  | Includes the scripts for building Docker images
utilities |  Includes DevOps backend scripts

**Note**: The `kubernetes/DeployController` folder contains the following files for customization:
* `plugins.txt`: Includes New or updated plugin version
* `setup/jobs`: Includes pre-defined Jenkins job
* `users/admin/config.xml`: Includes the default admin user information
* `config.xml`:Includes global variables for Jenkins
* `jenkins.sh`: Includes Jenkins startup logic

## Contributing to the project ##

After you try the DevOps utilities out, you are welcomed to contribute to this project by enriching the files list above and improving the documents.

If you'd like to do so, contact the administrators in the [contact list](CONTACT.md) so that you can be added as a project member.

You can also create issues directly to propose enhancements. We will evaluate and assign project members to fix or handle issues.

#### Related links ####

* Slack Channel

* [Contact list](CONTACT.md)
