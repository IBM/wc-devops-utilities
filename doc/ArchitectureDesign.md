# Architecture Design #

This topic illustrates the architecture design of the DevOps Utilities. After reading this topic，you will be able to understand how each utilities container works and the basic flow of managing multiple WebSphere Commerce V9 environments for Dev，QA，PreProd，and Prod purposes.

<!--For better understand it, there also have a End2End Usage which be draft as a story with several
Role which is more close a real scenario that a team or a company will pass through with DevOps
Utilities. See [End2End Usage Story](End2EndUsage.md)

 <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/Overview.png" width = "700" height = "450" alt="Overview" align=center /><br>-->

In the DevOps Utilities:

* `Long Run Pod` includes the core components, including DeployController, Vault, and Nexus.
* `Temporary Run Pod` includes the independent components, such as SupportContainer and DeploySlave.

All these components are dockerlized, so you can easily leverage the Kubernetes platform to deploy the components without manual setup.

DevOps Utilities leverage the task-scheduling capability of Jenkins and the resource-scheduling capability of Kubernetes.
Thus, when you trigger some long-run or asynchronous job through Jenkins, such as installing Helm or building Docker images,
the pre-defined Jenkins job pipeline will start a  temporary pod using the DeploySlave Docker container. When the job is complete, the temporary Pod is also released.

In DevOps Utilises, the concept *Docker Build In Docker* is also involved, which mean, when you start to build customized Docker image, the build process will be launched in a temporary pod with the DeploySalve Docker Image.

The DevOps Utilities are implemented with Python. Each Jenkins job calls a Python script. All python scripts are grouped in a Python package, which is composed of Python modules. You can find the Python modules under `commerce-devops-utilities/utilises`.

## DeployController  ##
DeployController is built as the Jenkins Master and acts as a "hub" to orchestrate deployment job. Its responsibilities include:
1. Connect to Vault to manage environment-related data
2. Connect to Nexus to fetch customized package for building customization Docker Image
3. Connect to Docker Repository to push customized Docker Image
4. Connect to Kubernetes in InCluster Mode to manage environment-related data with ConfigMap (such as Environment Info / Dockerfile )
5. Connect to Kubernetes and assign Jenkins jobs on the DeploySlave Pod.

When DeployController is started, you need to input the parameters as shown in the following table:

Parameter  | Description
------------- | -------------
VaultUrl |  Vault URL ( e.g. http://9.112.245.194:30552/v1 ). If `InCluster` is set to true, this value is not mandatory.
VaultToken  | Vault Root Token for REST API access . If `InCluster` is set to true, this value is not mandatory.
BundleRepo | Customized package repository. Nexus is the default bundle repository ( e.g.  http://9.110.182.156:8081/nexus/content/repositories/releases/commerce )
DockerRepo | Docker image repository (e.g. DockerRepoHostname:RepoPort )
KubernetesUrl | Kubernetes URL for remote call from Jenkins. If `InCluster` is set to true, this value is not mandatory.
DockerRepoUser   | User name for logging onto the Docker image repository when downloading the Docker image.
DockerRepoPwd  |User password for logging onto the Docker image repository when downloading the Docker image.
HelmChartsRepo  | Helm Charts Repository for updating Helm Charts. HelmChartsRepo handles Helm pre- and post-installation hook, and acts as InitContainer to control startup sequence (e.g. http://9.112.245.194:8879/charts)
InCluster | Specifies whether the DeployController is deployed inside or outside of the Kubernetes cluster. If `InCluster` is set to true, DeployController will automatically detect the Vault token and use the default Vault and Jenkins Services. The value can be true or false. False is the default value.

### Starting DeployController without configuration ###
You can start DeployController with the default settings:
```
docker run -d -p 8080:8080 -p 50000:50000 deploycontroller:latest
```

When DeployController is started, you can log into it and make configurations through **Manage Jenkins**>**Configure System**>**Environment variables**.

 <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/DeployController-GlobalConfig1.png" width = "700" height = "450" alt="Overview" align=center /><br>

 <img src="https://github.com/IBM/wc-devops-utilities/raw/master/doc/images/DeployController-GlobalConfig2.png" width = "700" height = "450" alt="Overview" align=center /><br>

You can trigger Jenkins job through the UI. To better integrate with the existing CD pipeline, You can also trigger DeployController with the web hook or Jenkins API.

## Vault  ##
Vault by default supports third-party applications for the certificate issue services and the Key-Value feature to store environment-related data.

It is suggested to use Vault PKI to present the Certificate Agent, which can automatically issue certificates for each component from the same CA and easily manage security connections between components.

Vault Key-Value is the default feature in WebSphere Commerce V9. If you set the out-of-box container's configuration mode to `CONFIGURE_MODE=Vault`, the out-of-box container will try to fetch environment data from Vault.

Since V9.0.0.4, WebSphere Commerce can better support ConfigMap, so if you do not want to store the environment data through Vault Key-Value, you can create ConfigMap and mount into the Docker container. <!--See [End2End Usage](End2EndUsage.md)-->

## Nexus ##
Nexus by default supports third-party applications to store and manage customization package. When building customization jobs, if you input
only the bundle version, the backend scripts will try to fetch related customized package from the default configured Nexus server. But please be aware that
Nexus <!--Tiffany: Incomplete sentence-->

## DeploySlave ##
Helm and Dockerd are embedded with DeploySlave. When you launch Jenkins jobs based on input to deploy or update a new WebSphere Commerce V9 environment, the master (DeployController) will assign the job on
an auto-created DeploySlave temporary pod and launch the Helm client.

Similar to launching the build customization <!--What is the name for the image and job? build customization?--> Docker image, the job automatically creates a temporary pod, fetches related Dockerfile from dedicated ConfigMap based on the user input, and leverages embedded Dockerd to build new Docker images. To launch customized Docker build job, you might need to change the default container size. 20 GB is capacity for the default container. It is enough for building search or ts-web.
However, if you want to build ts-app, increase the Docker container disk size to a minimum of 30 GB. If you want to build more than one component Docker image at one time, allocate more capacity for the container.

## Helm Charts ##
Helm Chart is the smallest executable component unit for deployment. In DeployController, the Helm repository is the init parameter for startup. During deployment, the Helm repository is passed to DeploySlave. The embedded Helm initializes the Helm Repository in DeploySalve with name stable <!--Tiffany: What is name stable?-->. The deployment UI of DeployController
supports specifying Helm Chart names. You can also specify Helm Chart names through the Jenkins job named "DeployWCSCloud" from the Helm repository.

## SupportContainer ##
SupportContainer can be used in Helm Charts as InitContainer for component container startup to:

1. Run as Helm Pre-Install Hook to create Secret.
2. Run as Helm Pre-Install Hook to create PVC.
3. Run as Helm Post-Delete Hook to remove PVC and Secret.
4. Run as InitContainer to control the component startup sequence.
