WCSDevOps is used for doing preparation before deploying and running CI/CD pipeline. WCSDevOps contains three deployments: vault & consul, jenkins and nexus. 

Vault is used to provide PKI service, and encrypt data of Consul. Consul is used to keep the information of Commerce environment, or you could keep environment parameters with env key-values in value.yaml.

Deploycontroller is a deploy controller, with all the CI/CD pipeline in it, including:
- AddCerts
- BuildDockerImage
- BundleCert
- CreateDockerfile
- CreateGroup
- DeployWCSCloud
- PopCustomTemp
- PrepareEnv
- RollBackGroup
- TriggerBuildIndex
- TriggerIndexReplica

Deploycontroller Container support some environment parameters to enable auto-configuration, such as:

Parameter  |  Usage
------------- | -------------
VaultUrl |  Specify Vault URL ( e.g http://9.112.245.194:30552 ). If InCluster equal true, this value is not mandatory
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

All the environment parameters have default value, it is just for feature testing. In most case, you only have to change one or two of these parameters based your cluster information.

nexus server is used to:.....