# Architecture Design #

This topic illustrates the architecture design of the DevOps Utilities. After reading this doc，
you will be able to understand how each utilities container works and the basic flow of managing multiple WebSphere Commerce V9 environments for Dev\QA\PreProd\Prod purposes.

<!--For better understand it, there also have a End2End Usage which be draft as a story with several
Role which is more close a real scenario that a team or a company will pass through with DevOps
Utilities. See [End2End Usage Story](End2EndUsage.md)

 <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/Overview.png" width = "700" height = "450" alt="Overview" align=center /><br>-->

In the DevOps Utilities:

* `Long Run Pod` includes the core components, including DeployController, Vault, and Nexus.
* `Temporary Run Pod` includes the independent components, such as SupportContainer and DeploySlave.

All these components are dockerlized, so you can easily leverage the Kubernetes platform to deploy the components without manual setup.

DevOps Utilities leverage Jenkins capability of task scheduling and Kubernetes capability of resource scheduling.
Thus, when you trigger some long-run or asynchronous job through Jenkins, such as installing Helm or building Docker images,
the pre-defined Jenkins job pipeline will start a  temporary Pod using the DeploySlave Docker container. When the job is complete, the temporary Pod is also released.

In DevOps Utilises, the concept "Docker Build In Docker" is also involved, which mean, when you start to build customized Docker image, the build process will be launched in a temporary Pod with the DeploySalve Docker Image.

The DevOps Utilities are implemented with Python. Each Jenkins job calls a Python script. All python scripts are grouped in a Python package, which is consisted of several Python modules. You can find the Python modules under `commerce-devops-utilities/utilises`.

## DeployController  ##
It be build as Jenkins Master and most like a "hub" to orchestrate deployment Job
1. Connect to Vault to manage environment related data
2. Connect to Nexus to fetch customized package for build customization Docker Image
3. Connect to Docker Repository to push customized Docker Image
4. Connect to Kubernetes as InCluster Mode to manage environment related data with ConfigMap ( e.g Environment Info / Dockerfile )
5. Connect to Kubernetes and assign Jenkins Job on DeploySlave Pod.

When start DeployController, some parameters need to be input as below table shows

Parameter  |  Usage
------------- | -------------
VaultUrl |  Specify Vault URL ( e.g http://9.112.245.194:30552/v1 ). If InCluster equal true, this value is not mandatory
VaultToken  | Specify Vault Root Token for rest access . If InCluster equal true, this value is not mandatory
BundleRepo | Specify customize package repository, Nexus is the default bundle repository ( e.g  http://9.110.182.156:8081/nexus/content/repositories/releases/commerce )
DockerRepo | Specify Docker Image repository (e.g DockerRepoHostname:RepoPort )
KubernetesUrl | Specify Kubernetes url for remote call from Jenkins. If InCluster equal true, this value is not mandatory
DockerRepoUser   | Specify User Name of Docker Image Repository for logon when download Docker Image
DockerRepoPwd  | Specify User Password of Docker Image Repository for logon when download Docker Image
HelmChartsRepo  | Specify Helm Charts Repository for update Helm Charts | handle helm pre and post install hook / as InitContainer to controller startup sequence (e.g http://9.112.245.194:8879/charts)
InCluster | true or false as default.  Specify if this deploy controler be deployed inside of out side of Kubernetes cluster, if InCluster equal true, DeployController will auto defect Vault token and use default Vault and Jenkins Service

### Start DeployController Without Configurtion ###
```
docker run -d -p 8080:8080 -p 50000:50000 deploycontroller:latest
```

by this way, deploycontroller will be startup without any configuration. When it startup, you can logon it and edit

Manage Jenkins --> Configure System --> Environment variables

to input those parameter by manually then save the change

 <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/DeployController-GlobalConfig1.png" width = "700" height = "450" alt="Overview" align=center /><br>

 <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/DeployController-GlobalConfig2.png" width = "700" height = "450" alt="Overview" align=center /><br>


You can trigger Jenkins Job through UI. For better integrate with existed CD pipeline, it also can be triggered from web hook or Jenkins API.

## Vault  ##
It is default support third-party to provide Certification Issue service and Key-Value feature to store environment related data.

We recommend to use Vault PKI to present Certification Agent, This can let you auot issue certification for each component from same CA. This
can make manage security connection between each component more easier.

Vault Key-Value is the default support feature in Commerce V9 OOTB. IF you set
OOTB Container's config mode as CONFIGURE_MODE=Vault, the OOTB will try to fetch environment data from Vault

Since 9.0.0.4, Commerce V9 can better support ConfigMap, so if you don't want store environment data on Vault Key-Value, you can create ConfigMap and mount into Docker Container. See [End2End Usage](End2EndUsage.md)

## Nexus ##
It is default support third-party to provide capacity to store and manage customization package. In Build Customization Job, if you just input
the bundle version, the backend scripts will try to fetch related customized package from default configured Nexus server. But please be aware that
Nexus

## DeploySlave ##
DeploySlave embedded Helm and Dockerd inside. So when launch Jenkins Job to based on input to deploy or update a new Commerce V9 environment. The master will assign the Job on
a auto created DeploySlave Pod which is a temporary Pod and launch Helm client in it.

Same as launch build customized Docker Image, the Job will auto create a temporary Pod and based on user's input to fetch related Dockerfile from dedicated ConfigMap and use embedded Dockerd
to build new Docker Images. For launch customized Docker Build Job, there have a limitation that need to change default container size, 20GB is the default value which is enough for build search or ts-web,
but if we want to build ts-app, we need to increase the Docker Container Disk size to over 30 GB. IF you want to build more component Docker Image at one time, you need more container disk

## Helm Charts ##
It is the smallest unit of deployment and can be execute independently. In DeployController, Helm Repository is the init parameter for startup. When do deployment
Helm Repository will be pass to DeploySlave and the embedded helm will init the Helm Repository in DeploySalve with name stable. The deployment UI on DeployController
support to let user specify the Helm Charts name with and There have Jenkins Job named "DeployWCSCloud" can let user to specify Helm Charts name from Helm Repository

## SupportContainer ##
It will be used in Helm Charts as InitContainer for component container startup to

1. Run as Helm Pre-Install Hook to create Secret
2. Run as Helm Pre-Install Hook to create PVC
3. Run as Helm Post-Delete Hook to remove PVC and Secret
4. Run as InitContainer to control component startup sequence.
