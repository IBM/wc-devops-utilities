# WebSphere Commerce DevOps Utilities #

WebSphere commerce DevOps Utilities<!--Tiffany: This seems to be a new term, which I didn't see anywhere. What does that mean? What are contained in this utility?-->, as a sample tool chain for reference<!--Tiffany: What does this mean?-->, support deploying WebSphere Commerce V9 on Kubernetes. For more information, see [WebSphere Commerce Version 9 knowledge Center](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/landing/wc_welcome.htm)<!--Tiffany: I don't think we have reference on Kubernetes on KC-->.

WebSphere Commerce DevOps Utilities can also support WebSphere Commerce V9+ deployment on IBM Cloud Private (ICP). For details on ICP, see [IBM Cloud Private](https://www.ibm.com/cloud/private).

WebSphere Commerce DevOps Utilities can be built and deployed as a Docker container, which includes DeployController, DeploySlave, and SupportContainer Docker images.

Docker Image  |  Embed Assets  | Description
------------- | -------------| -------------
DeployController | Jenkins / Pre-defined job / DevOps backend scripts |  Work as the controller to trigger related jobs
DeploySlave  | Docker / Helm client / DevOps backend scripts | Can be triggered by DeployController to build customized Docker image and can be deployed with Helm
SupportContainer | DevOps backend scripts | Handle Helm pre- and post-installation hook<!--Tiffany: What does "hook" mean?--> / Work as InitContainer to control the startup sequence

Vault and Nexus Docker image by default is integrated with the DevOps Utilities.

 [Vault](https://www.vaultproject.io/) acts as the Certification Agent to automatically issue certification and Remote Configuration Center to store environment related configuration.

 [Nexus](https://www.sonatype.com/nexus-repository-sonatype) stores and  manages customization packages and support building customization Docker Image.

To quickly deploy HelmChart, see [Commerce DevOps Utilities Helm Charts](https://github.com/IBM/wc-helmchart)

Below is a high-level architecture of deploying WebSphere Commerce using DevOps Utilities.
  <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/Overview.png" width = "700" height = "450" alt="Overview" align=center /><br>

## Design ##

* [Architecture Design](doc/ArchitectureDesign.md) <br>
* [DeployController Design](doc/DeployControllerDesign.md) <br>
* [Utilites Design](doc/UtilitiesDesign.md) <br>
* [DeploySlave Design](doc/DeploySlaveDesign.md) <br>
* [SupportContainer Design](doc/SupportContainerDesign.md)

## Building  ##

Note: Before you run build<!--Tiffany: What build? Can we be more specific?-->, ensure that your machine has installed Docker ( DockerCE or EE  17.06 ) and that your machine is connected to the Internet.

1. Go to the  `commerce-devops-utilities/kubernetes/DeployController` directory, and run the following command to build the DeployController Docker image:

        ./BuildDocker.sh

    **Note**: you can specify the Docker image tag in the following pattern:
        ./BuildDocker.sh deploycontroller:newtag

2. Go to the `commerce-devops-utilities/kubernetes/DeploySlave` directory, and run the following command to build the DeploySlave Docker image:

   ```
   ./BuildDocker.sh
   ```
    **Note**: You can specify the Docker image tag in the following pattern:
        ./BuildDocker.sh deployslave:newtag

3. Go to the  `commerce-devops-utilities/kubernetes/DeploySupport`directory, and run the following command to build the DeploySupport Docker image:
   ```
   ./BuildDocker.sh
   ```
   **Note**: You can specify the Docker image tag in the following pattern:
       ./BuildDocker.sh deploysuppor:newtag

## Deploying ##

To quickly deploy HelmChart that is provided, see [Commerce DevOps Utilities Helm Charts](https://github.com/IBM/wc-helmchart).

Ensure to deploy WebSphere Commerce DevOps Utilities under the `default` namespace.

To access DeployController user interface, log in `http://IngressIPAddress:31899` with the default user name and password (`admin/admin`).

If you already have a WebSphere Commerce environment, or you do not want to deploy Utilities on the Kubernetes cluster or ICP, you can also manually deploy each container.

After the deployment is completed, you can log into DeployController to check the following pre-defined jobs:

<img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/DeployControllerJobList.png" width = "700" height = "450" alt="Overview" align=center /><br>

**Tips**:
 For each job in DeployController, make sure to open the `config` page to save it<!--Tiffany: What does "it" refer to? Is it the job?-->, so that the auto parameter<!--Tiffany: What is auto marameter?--> plugin can be loaded.

## Usage ##

See [Commerce DevOps Utilites End2End Usage](doc/End2EndUsage.md)

## Developing ##

This is an ongoing project and we welcome you to contribute to the content of this project.  If you'd like to do so, contact the administrators in [Contact List](CONTACT.md) so that you can be added as a project member.

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


## Support ##

* Creating issues

  You can create issues in this project or propose a enhancements whenever needed. We will evaluate and assign contributors to fix or handle issues.

* Slack Channel

* To be added as a contributor, see the [Contact List](CONTACT.md).
