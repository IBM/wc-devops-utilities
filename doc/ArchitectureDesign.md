# Architecture Design #

This doc will illustrate the architecture design with the DevOps Utilities. After read this doc，
you could better understand how each utilities container works and the basic flow to manage multiple
Commerce V9 environment for Dev\QA\PreProd\Prod environment.

For better understand it, there also have a End2End Usage which be draft as a story with several
Role which is more close a real scenario that a team or a company will pass through with DevOps
Utilities. See [End2End Usage Story](End2EndUsage.md)

 <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/Overview.png" width = "700" height = "450" alt="Overview" align=center /><br>

The core component in DevOps Utilities are DeployController /  Vault / Nexus. They are the `Long Run Pod`.
There also have independent component like SupportContainer /  DeploySlave, They are the `Temporary Run Pod`.
All those Utilities are Dockerlized, so you can easy leverage Kubernetes platform to deploy it without any manually setup.

DevOps Utilities mainly leverage the Jenkins's capacity of task scheduling and the Kubernetes's capacity of resource scheduling.
So when user trigger some long run or asynchronous action through Jenkins Job ( for example Helm Install / Build Docker Image ),
the pre-defined Jenkins pipeline in Job will use Kubernetes plugin start up DeploySlave container
as a temporary Pod. When Job finish, temporary Pod will be release. This can bring very good user experience. In
DevOps Utilises, we also involved the concept of "Docker Build In Docker", so when you trigger build customized Docker Image
The process will be launched in a temporary Pod which start up with DeploySalve Docker Image.

The backend logic be implemented with Python. For each Jenkins Job, finally, it call a "command style" python scripts. All python scripts be
grouped as a python package which compose with several python module. You can find them under commerce-devops-utilities/utilises.

## DeployController  ##
It be build as Jenkins Master and most like a "hub" to orchestrate deployment Job
1. Connect to Vault to manage environment related data
2. Connect to Nexus to fetch customized package for build customization Docker Image
3. Connect to Docker Repository to push customized Docker Image
4. Connect to Kubernetes as InCluster Mode to manage environment related data with ConfigMap ( e.g Environment Info / Dockerfile )
5. Connect to Kubernetes and assign Jenkins Job on DeploySlave Pod.

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