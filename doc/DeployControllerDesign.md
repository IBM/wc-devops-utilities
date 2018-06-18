# Deploy Controller Design #

## OverView ##
Deploy Controller be build as Jenkins Master. It includes Global variables , Pre-defined Jenkins Job and Backend scripts

Deploy Controller is most like a "Hub" used to integrate all tool chain which you will needed to deploy Commerce V9. User can customized those Job and backend scripts to match different requirement.
With this Deploy Controller, user can finish all related work through UI portal, instead of logon same server to run command or scripts.

Admin also can use role based access control to create different view for different user.

Jenkins Job is most like MVC framework.  Jenkins UI define the View layer. You can change the Jenkins Job UI through "Configuration" page.
each Jenkins Job has pipeline which is most like controller to control the sequence of stage in current Job.  Backend scritps is most like the
model layer to finish the real action and manage data.

## Global Variables ##

Parameter  |  Usage
------------- | -------------
vault_url |  Specify Vault URL ( e.g http://9.112.245.194:30552/v1 ). If InCluster equal true, this value is not mandatory
vault_token  | Specify Vault Root Token for rest access . If InCluster equal true, this value is not mandatory
bundleRepo | Specify customize package repository, Nexus is the default bundle repository ( e.g  http://9.110.182.156:8081/nexus/content/repositories/releases/commerce )
dockerRepoHost | Specify Docker Image repository (e.g DockerRepoHostname:RepoPort )
dockerRepoUser   | Specify User Name of Docker Image Repository for logon when download Docker Image
dockerRepoPwd  | Specify User Password of Docker Image Repository for logon when download Docker Image
helmChartsRepo  | Specify Helm Charts Repository for update Helm Charts | handle helm pre and post install hook / as InitContainer to controller startup sequence (e.g http://9.112.245.194:8879/charts)

Global can be configured when you do deploy by pass related value to Docker Container, or you can configure them by manually in "Configuration System" page of Jenkins <br>
<img src="./images/DeployController-GlobalConfig1.png" width = "500" height = "350" alt="Overview" align=center /><br>

## Pre-Defined Jobs ##

### AddCerts_Base ###

Job Description: <br>

Create third-party certification for specified environment on specified tenant. After add third-party certification, you can use "BundleCert" job to bundle
specify certification on target component. IF deploy Commerce V9 with configure mode Vault_CA=true. the component's container will try to fetch bundled certification
and apply it.

Job UI: <br>

<img src="./images/AddCertUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Usage
------------- | -------------
Tenant |  Tenant Name  ( One Tenant could have multiple enviornment. In Kubernetes, Tenant can be isolated with NameSpace )
EnvName  | Environment Name
CertName | Specify Name of Certification, It will be the alias name in keystore.
PrivateKey | Content of private key  for the certification. IF the certification used for two way authentication, this value is mandatory. <br> e.g -----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAtuWgQ5P9KjpgplOyejAEj5pDgSmQ6mZkbqY6gnIIKlw1I4Vu\nlaigmeiir37NcAHtLA9HrpqafKoQqt3RPIFqMq2qb728JUNqdkmgp1QRnXdRVqrv\nGxT3o6XLMmxpkniwL+f3A/qFzuBgDJVltKLn1e0O3conPiiGtqaZ70+1lccKkKvi\nLoin13T+27gFFws6dT74znCxT8c/ikXGMja1TDEddd+qkXlo4At104Fo7Uhx95JW\norSljSTaCQkEeOjX+8SJHkARSrKeGEvkBESpXD23oUY9MlxGQnldioLAI5Eu8fRo\n3PKQUhuFnuoxTr0pO7R60AEe8E0sVU/cE3UtswIDAQABAoIBAB3kQ6An1K2NIvSs\nIzRTGru5k6TNfVDB8VIgOtnM90atEUY/7YXqLG1bFxOlnr/aoL+ds7J2tB8B0H2M\niUDhSdEEjyF6GgDhFspEWExgsgxRTuriPvfnIl4Nn7sa+tokfW8m8zkkPbBE/Y2w\n8RFnuoo9FzvqaSWAjBvX+LqjBWN4AGHxPcBcZs/H4U7RvdO0etX2Zbpjs62K/KO3\ni3e4MXgGZtj0Vx2LYD/AYSbqEoo1v8/U1AbGmsCTTNc2EwARhyb1zUgO7yc9yft6\nUoAC6pZjxOFsJtwz26jpNdqXz9t1xml3XnNusqHe+hgStQlIL2mgU8qj18q5pqpu\nkehM9LECgYEAxiU9WA7kQTp8hGKTRqrRbcGBsLTGxsYeILFQggtJBOZ5ngOH35Nd\nUIzQ1EjKODFEzGH9qPBBfE6BNdl3naHuYgIS3Uz8FCAwsOZAW6X8tC7VU/ZrwKUA\nF3Rc2iek+J1bdaz5o3hnR2eY/6kVuNHznxqIzK+JuZ7Dq/wEMlAL4gkCgYEA7Eyb\n4uyQFMXfPLiZPn7opNlgmi4i5lNLbPAjJq0dagdP8HbhLBqQThMcyAnu9rJmNm6t\n2Wu8kkKIpcZiGOVzFQvoTWOm6KGU/nIFFH1p6AAz/hvhATFA8HpLe9B7la9T6c5R\nabbtFbUNrHyoieMsIxkrjPo1zVIThLJeIVdoUNsCgYEAwuhKyV4MpSU06rxUhsTs\nsXwRaJLKnSiw5hPFT8ZuE0XrB8YNV52LwvphSRA46sF8HVeevxlmMTK/4wqBoSty\nZDIKAGoD5IAtpTU4xW4nf845xhe1spAb4PZzh5xLqMqQ9tYp0eVUImcDlyjp1x2e\n+TiOrFlXrqE/dOO39Q3MQpECgYEA5plMd4OMh/kiBcvQIOEQf+9zCoODo2od7U3b\nv96pGdPQ+0XIMJYrxUV5jO3EuhMXFH+mQMuW1tT/LWgQS2N/j0ZziTJ6rAMjt7vl\noT1SoQmxs4XZaqR6TzPJfibStBzJsx2Y7aWKcOijU3TDtOxxIj9p9MYowxoZ2iGH\nItp9/okCgYEAh6lbVbf77NArp1FsocQoeZ2ZL1hsOXpmRwpNmePPA6DfjqJyttpH\ngSh8Z0daqMvojStilhwIkEURy9ITuPYoKt2blWQY8RY//H1zFnwKg2AJR5PvlWcT\n0JBxt4cHMYy6jW2Q8/ZTVuttPd+UVIDehTFN6oyWF6FBgKxLO5bSjzc=\n-----END RSA PRIVATE KEY-----
IssuingCA   | Content of trust certification. It is mandatory <br> e.g -----BEGIN CERTIFICATE-----\nMIIFJjCCAw6gAwIBAgIUDUnfHPvwqpztM2lJh40lVUmTjV8wDQYJKoZIhvcNAQEL\nBQAwKzEpMCcGA1UEAwwgc2VsZnNlcnZlX3Byb2R1Y3Rpb25fcGtpIFJvb3QgQ0Ew\nHhcNMTcwODI1MDUwNTEzWhcNMjcwODIzMDUwNTQzWjArMSkwJwYDVQQDDCBzZWxm\nc2VydmVfcHJvZHVjdGlvbl9wa2kgUm9vdCBDQTCCAiIwDQYJKoZIhvcNAQEBBQAD\nggIPADCCAgoCggIBAM5LpBH9Qyg5VjTkdMj61gt72CVIrqE5s9iD+Bpb2hlLnWdb\n52FtcgCxIRca8kJhCYK53dNVmCP8d7LSzogxdIHyzEe5f405ukJVZIbYEYcA4BLK\n3UU322bYJkTTToABwV+XhlHjLhaze9GLo4snCklxAzafWvqR1C0faB2dPtq5WyQi\n/2uCvGHcpqe/ozNvZON6eYkjQpCwHftR0TwVVb435hvJb6FeeV95MgVq/C0pZFG4\nGLgJNj4GK4BtG2wsIDVMMcaoFrSKfKDqyE+4ekvzYP4nDzbYK5XsgH7/7XB9tL7w\nwMVj0J1mR3TbxVTBZyk509F0oXqBcNb6vvybJevhDlkXMQPgxyOmogm6GUQ3beMX\nsRpN5uotnbWaF0MQbgo8YrgQX3BGrLmKRfk9rIMoBKabptDMRw5Df1ouu5D9Jb3b\n3nlelkRXR5qb0R68CM0S78KqVB32NQsLixQ58YUKmcvlQcaIF9cwC28+LYm4sRq/\nV0tCl68K19PmgZT+Qr0Apakw+vlQ8ojvT+/wTVtg+gphuG7Ovv00xRXa/dpoC3Ff\nOktxUmu3bh4YU/IVCT3+YbwB7vyOfKGTwSmVK+s5gt4MDM65zX58xa85psJI8mqP\nCwKGDleglrAIrHxxg2wKrIibiIriSnjJsKqCzpcm9+6V4zewwQFqdfr1R92rAgMB\nAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQW\nBBQNl+8T/jYl1zV4Sct1EKqHBDcUUzANBgkqhkiG9w0BAQsFAAOCAgEAYo+vaKzi\nW2YTogGvuDvWnFzDtRa6zfB1UNqUTiacmr9ISqTDGJPOE7o7+5//31yS63/VuPAb\nsskfjtbywGUcjLEoa//vqDUA5VPQSr2MGpqZItt+QQ7eIQPQEt6IaqohmIxvgyDI\nvV35Ld06slZju9IZJdOx5GyRU49ZrhTciNeHBFJbPTzTWw7swjP1Kj13BJ9++YlU\ndHHnJecMgRPXbbFn8cThcIUwhaTEWFhlC7zc4YUpTm8nmHaCLmG8TM7tYLaymHqd\nypMBa3TrGr4+XIgwkWWb9h9+JnlBXc+aq2pJulErzN3raytzv+iTOwcI+YCufgee\nAf25Zzk9t75KIHjSdqu1U/QXiPSgJgr7o2yrtZbeLT+eMHuhCfbuWduipuRgTlUk\na8hvoiFDabCrlJABDYHNO8WMCIqX9qja0crqA1JbPXAEMiYwdtoU+p27CtNupGVE\nQENamacyYD5VhApTnxACwwakMep0jDYQUXUYTeLz6Aj3vVUJl54/3Uqbh6fxKamh\n8xDeb+HjhO5UKDkfAH0qe17qSGGVftMI3YMPCEqrvnnoVl8VHxpvdVjjJoHEEKoE\ne8mrX4Jp9O3xVcGFItMQQzvWc1A47ewqIy6x+bk+0W8fL6+rKd+8U7aRIvC7LFiw\nluvq3QIacuHULtox36A7HFmlYDQ1ozh+tLI=\n-----END CERTIFICATE-----
KeyStorePass  | Specify keystore password. If this value is empty, the default valule "ibmkey" will be assigned
DestinationHost |Not Mandatory, just work for TS-APP. Specify the Destination this certification will be used. <br> e.g testhost

### BuildDockerImage_Base ###

Job Description: <br>

Build Customized Docker Image with specified based docker image and customized package version for specified Environment on target Tenant
Based on user's input (Tenant/NameSpace/EnvName/EnvType) to find target Dockerfile. Dockerfile will be store as ConfigMap and named following
naming pattern <Tenant><EnvName><EnvType>-<Component>-dockerfile. You can use "ManageDockerfile" Job to create Dockerfile for specified component or environment

The backend logic will based on input to detect if there have target Dockerfile in ConfigMap under specified NameSpace.

Job UI: <br>

<img src="./images/BuildDockerImageUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Usage
------------- | -------------
Tenant | Tenant Name ( One Tenant could have multiple enviornment. In Kubernetes, Tenant can be isolated with NameSpace )
NameSpace | Specify the target NameSpace this Tenant belong to ( will search related Dockerfile config on ConfigMap under specifie NameSpace based on input tenant / envname / entype )
EnvName  | Environment Name
ForcePush | Specify if need to force push docker image
ForcePull | Content of private key  for the certification. IF the certification used for two way authentication, this value is mandatory. <br> e.g -----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAtuWgQ5P9KjpgplOyejAEj5pDgSmQ6mZkbqY6gnIIKlw1I4Vu\nlaigmeiir37NcAHtLA9HrpqafKoQqt3RPIFqMq2qb728JUNqdkmgp1QRnXdRVqrv\nGxT3o6XLMmxpkniwL+f3A/qFzuBgDJVltKLn1e0O3conPiiGtqaZ70+1lccKkKvi\nLoin13T+27gFFws6dT74znCxT8c/ikXGMja1TDEddd+qkXlo4At104Fo7Uhx95JW\norSljSTaCQkEeOjX+8SJHkARSrKeGEvkBESpXD23oUY9MlxGQnldioLAI5Eu8fRo\n3PKQUhuFnuoxTr0pO7R60AEe8E0sVU/cE3UtswIDAQABAoIBAB3kQ6An1K2NIvSs\nIzRTGru5k6TNfVDB8VIgOtnM90atEUY/7YXqLG1bFxOlnr/aoL+ds7J2tB8B0H2M\niUDhSdEEjyF6GgDhFspEWExgsgxRTuriPvfnIl4Nn7sa+tokfW8m8zkkPbBE/Y2w\n8RFnuoo9FzvqaSWAjBvX+LqjBWN4AGHxPcBcZs/H4U7RvdO0etX2Zbpjs62K/KO3\ni3e4MXgGZtj0Vx2LYD/AYSbqEoo1v8/U1AbGmsCTTNc2EwARhyb1zUgO7yc9yft6\nUoAC6pZjxOFsJtwz26jpNdqXz9t1xml3XnNusqHe+hgStQlIL2mgU8qj18q5pqpu\nkehM9LECgYEAxiU9WA7kQTp8hGKTRqrRbcGBsLTGxsYeILFQggtJBOZ5ngOH35Nd\nUIzQ1EjKODFEzGH9qPBBfE6BNdl3naHuYgIS3Uz8FCAwsOZAW6X8tC7VU/ZrwKUA\nF3Rc2iek+J1bdaz5o3hnR2eY/6kVuNHznxqIzK+JuZ7Dq/wEMlAL4gkCgYEA7Eyb\n4uyQFMXfPLiZPn7opNlgmi4i5lNLbPAjJq0dagdP8HbhLBqQThMcyAnu9rJmNm6t\n2Wu8kkKIpcZiGOVzFQvoTWOm6KGU/nIFFH1p6AAz/hvhATFA8HpLe9B7la9T6c5R\nabbtFbUNrHyoieMsIxkrjPo1zVIThLJeIVdoUNsCgYEAwuhKyV4MpSU06rxUhsTs\nsXwRaJLKnSiw5hPFT8ZuE0XrB8YNV52LwvphSRA46sF8HVeevxlmMTK/4wqBoSty\nZDIKAGoD5IAtpTU4xW4nf845xhe1spAb4PZzh5xLqMqQ9tYp0eVUImcDlyjp1x2e\n+TiOrFlXrqE/dOO39Q3MQpECgYEA5plMd4OMh/kiBcvQIOEQf+9zCoODo2od7U3b\nv96pGdPQ+0XIMJYrxUV5jO3EuhMXFH+mQMuW1tT/LWgQS2N/j0ZziTJ6rAMjt7vl\noT1SoQmxs4XZaqR6TzPJfibStBzJsx2Y7aWKcOijU3TDtOxxIj9p9MYowxoZ2iGH\nItp9/okCgYEAh6lbVbf77NArp1FsocQoeZ2ZL1hsOXpmRwpNmePPA6DfjqJyttpH\ngSh8Z0daqMvojStilhwIkEURy9ITuPYoKt2blWQY8RY//H1zFnwKg2AJR5PvlWcT\n0JBxt4cHMYy6jW2Q8/ZTVuttPd+UVIDehTFN6oyWF6FBgKxLO5bSjzc=\n-----END RSA PRIVATE KEY-----
BuildInfo | Specify the build information

For BuildInfo is like a Json format to specify customzied docker build information for each component

For example:  IF you input Tenant=demo Namespace=default  EnvName=qa In DockerImage you defined the search-app  as below
{
     "name":"search-app",
     "base":"xxxxx",   // this is the base docker image tag, as default it will download docker image from <dockerRepo>/commerce/<name>:<base>
     "bundle": "xxxx", // this is customization package url, you can input a http://... link directly here or you can integrate with Nexus
     "version": "xxx"   // this is the new docker image tag. For example. when finish build the docker image, it will be tag as  <dockerRepo>/<Tenant>/search-app-cus:<version> and based on this docker image name to push to dockerRepo
}

### BundleCert_Base ###

Job Description: <br>

Bundle third-party certification to target component. This can be next action after AddCert Job. One Component can be bundle multiple third-party certification.

Job UI: <br>

<img src="./images/BundleCertUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Usage
------------- | -------------
Tenant | Tenant Name ( One Tenant could have multiple enviornment. In Kubernetes, Tenant can be isolated with NameSpace )
EnvName  | Environment Name
Component | Specify target component to bundle third-party certification
BundledCerts | Based on Tenant/EnvName auto fetch the certs which already bundled on current component
SelectedCerts | Based on Tenant to auto list all third-party certification record. Select the target certification and click build button will bundle the certification to target component.

### CreateTenant_Base ###

Job Description:<br>

Create Tenant. This job will create a new storage backend which named as the Tenant name. After create new tenant finish
User can use AddCert/BundleCert/ManageVaultConfig to manage data on Vault.

Job UI: <br>
<img src="./images/CreateTenantUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Usage
------------- | -------------
Tenant | Tenant Name ( One Tenant could have multiple enviornment. In Kubernetes, Tenant can be isolated with NameSpace )
DedicatedRootCA  | Specify if need to create dedicated RootCA backend which named as the Tenant name
CreatedDedicatedView | Specify if need to create a dedicated Jenkins View for target Tenant

### DeployWCSCloud_Base ###

Job Description: <br>

Based on input to deploy/update/delete Commerce V9 environment with Helm by launch a temporary Pod with DeploySlave

Job UI: <br>
<img src="./images/DeployWCSCloudUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Usage
------------- | -------------
Tenant | Tenant Name ( One Tenant could have multiple enviornment. In Kubernetes, Tenant can be isolated with NameSpace )
EnvName  | Specify target environment name
EnvType | Specify target environment type
NameSpace | Specify target NameSpace this environment will be deployed
DeployAction | Specify action need to do. Support install / update / delete action
HelmChart_Values | Specify the Helm Charts Values. Job will provide default Values based on input from other field. But user must make sure some other values.

Before you trigger this job, please make sure all value in HelmChart_Values are correct.

Tenant / EnvType / NameSpace / EnvType / Vault Token / Vault URL will be updated based on the input from field on UI or get from Jenkins global variables.

But there still have some other important configuration must set correctly
1. ImageRepo
2. SPIUserName
3. SPIUserPWDAES
4. SPIUserPWDBase64
5. Merchantkey
6. Commerce V9 Image Tag
7. SupportC Image Tag
8. ExternalDomian
9. ConfigureMode ( Vault is the default config mode )

### ManageConfigMap_Base ###

Job Description: <br>

Create ConfigMap object on Kubernetes. From this Job the ConfigMap object is most like filefrom model
the key will be the filename. The ConfigMap object will be named as <Tenant><EnvName><EnvType>-<filename> under target NameSpace

It also can use to help check the value from existed ConfigMap, if you can input the correct key

Job UI: <br>
<img src="./images/ManageConfigMapUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Usage
------------- | -------------
Tenant | Tenant Name ( One Tenant could have multiple enviornment. In Kubernetes, Tenant can be isolated with NameSpace )
EnvName  | Specify target environment name
EnvType | Specify target environment type
NameSpace | Specify target NameSpace this environment will be deployed
FileName | Specify the FileName as the key to store date in ConfigMap object. IF you want to create key/value pare. please name file name with "xxx.properies".
ValueData | Specify

### ManageVaultConfig_Base ###

Job Description: <br>

Add or Update key/value on Vault under specified tenant and environment.

Job UI: <br>
<img src="./images/ManageVaultConfigUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Usage
------------- | -------------
Tenant | Tenant Name ( One Tenant could have multiple enviornment. In Kubernetes, Tenant can be isolated with NameSpace )
EnvName  | Specify target environment name
ConfigureOnVault | Auto fetch the existed Vault key/value on Vault based on Tenant / EnvName. IF there don't have any config will show empty

### TriggerBuildIndex_Base ###

Job Description: <br>

Trigger Search Build Index on Target Environment

Job UI: <br>
<img src="./images/TriggerBuildIndexUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Usage
------------- | -------------
Tenant | Tenant Name ( One Tenant could have multiple enviornment. In Kubernetes, Tenant can be isolated with NameSpace )
EnvName  | Specify target environment name
EnvType | Specify target environment type
NameSpace | Specify target NameSpace this environment will be deployed
MasterCatalogId | Specify MasterCatalogId
SpiUser | Specify spi user name
SpiPwd  | Specify spi user password

### TriggerIndexReplica_Base ###

Job Description:  <br>

Trigger Search Build Index Replica on Target Environment

Job UI: <br>

<img src="./images/TriggerIndexReplicaUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Usage
------------- | -------------
Tenant | Tenant Name ( One Tenant could have multiple enviornment. In Kubernetes, Tenant can be isolated with NameSpace )
EnvName  | Specify target environment name
NameSpace | Specify target NameSpace this environment will be deployed
SpiUser | Specify spi user name
SpiPwd  | Specify spi user password

## Backend Scripts ##

Backend scripts located under path /commerce-devops-utilities/utilities in DeployController