#  Using WebSphere Commerce DevOps utility #

## Overview ##
The DeployController component is built as a Jenkins Master, which includes pre-defined Jenkins jobs and backend scripts. There are global variables to define and control the execution context of the utility, such as the global configuration center and Docker repository host.

DeployController is acting like a "Hub" to integrate all tools that you need to deploy WebSphere Commerce V9. You can customize the jobs and backend scripts based on your requirements. You can deploy your WebSphere Commerce environment through user interface, instead of running commands on varies servers.

<!--Admin also can use role based access control to create different view for different user.

Jenkins Job is most like MVC framework.  Jenkins UI define the View layer. You can change the Jenkins Job UI through "Configuration" page.
each Jenkins Job has pipeline which is most like controller to control the sequence of stage in current Job.  Backend scritps is most like the
model layer to finish the real action and manage data.-->

## Configuring your operational context through global variables ##
Before you start the operational job, configure the global variables. These variables can be configured when you perform deployment tasks by passing related values to the Docker container. Or you can configure the variables manually on the `Configuration System` page of Jenkins.

Parameter  |  Description
------------- | -------------
vault_url |  Specify the Vault URL (for example, http://9.112.245.194:30552/v1 ). If InCluster is set to `true`, vault_url is not mandatory.
vault_token  | Specify the Vault Root Token for REST access. If InCluster is set to `true`, tvault_toke is not mandatory. For more information, see [Vault/Cousul based configuration management](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/com.ibm.commerce.install.doc/refs/rigvaultmetadata.htm).
bundleRepo | Specify the repository destination for storing the customization packages. Nexus is the default bundle repository (for example,  http://9.110.182.156:8081/nexus/content/repositories/releases/commerce).
dockerRepoHost | Hostname for the Docker image repository (for example, DockerRepoHostname:RepoPort).
dockerRepoUser   | User ID to access the Docker image repository when downloading the Docker image.
dockerRepoPwd  | Password to access the Docker image repository when downloading the Docker image.
helmChartsRepo  | The Helm Charts repository for storing Helm Charts to be triggered by the Jenkins job.
| Handles Helm pre- and post- installation hook / Serves as InitContainer to control startup sequence (e.g http://9.112.245.194:8879/charts)

<!--Global can be configured when you do deploy by pass related value to Docker Container, or you can configure them by manually in "Configuration System" page of Jenkins <br>
<img src="./images/DeployController-GlobalConfig1.png" width = "500" height = "350" alt="Overview" align=center /><br>-->

## Pre-defined operational jobs ##

### AddCerts_Base ###

Job Description: <br>

Create third-party certificate for the specified environment on a specified tenant<!--Tiffany: Replace tenant?>. After adding third-party certificate, you can use the "BundleCert" job to bundle
specific certificate on target component. If you deploy WebSphere Commerce V9 by setting the Configure Mode `Vault_CA` to `true`, the component container will fetch the bundled certificate
and apply it.

Job UI: <br>

<img src="./images/AddCertUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant |  Tenant name. One tenant can contain multiple environments. In Kubernetes, tenant can be isolated by NameSpace.
EnvName  | Environment name
CertName | Certificate name. The alias name in keystore.
PrivateKey | Content of private key for the certificate. If the certificate uses for two-way authentication, this value is mandatory. <br> e.g -----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAtuWgQ5P9KjpgplOyejAEj5pDgSmQ6mZkbqY6gnIIKlw1I4Vu\nlaigmeiir37NcAHtLA9HrpqafKoQqt3RPIFqMq2qb728JUNqdkmgp1QRnXdRVqrv\nGxT3o6XLMmxpkniwL+f3A/qFzuBgDJVltKLn1e0O3conPiiGtqaZ70+1lccKkKvi\nLoin13T+27gFFws6dT74znCxT8c/ikXGMja1TDEddd+qkXlo4At104Fo7Uhx95JW\norSljSTaCQkEeOjX+8SJHkARSrKeGEvkBESpXD23oUY9MlxGQnldioLAI5Eu8fRo\n3PKQUhuFnuoxTr0pO7R60AEe8E0sVU/cE3UtswIDAQABAoIBAB3kQ6An1K2NIvSs\nIzRTGru5k6TNfVDB8VIgOtnM90atEUY/7YXqLG1bFxOlnr/aoL+ds7J2tB8B0H2M\niUDhSdEEjyF6GgDhFspEWExgsgxRTuriPvfnIl4Nn7sa+tokfW8m8zkkPbBE/Y2w\n8RFnuoo9FzvqaSWAjBvX+LqjBWN4AGHxPcBcZs/H4U7RvdO0etX2Zbpjs62K/KO3\ni3e4MXgGZtj0Vx2LYD/AYSbqEoo1v8/U1AbGmsCTTNc2EwARhyb1zUgO7yc9yft6\nUoAC6pZjxOFsJtwz26jpNdqXz9t1xml3XnNusqHe+hgStQlIL2mgU8qj18q5pqpu\nkehM9LECgYEAxiU9WA7kQTp8hGKTRqrRbcGBsLTGxsYeILFQggtJBOZ5ngOH35Nd\nUIzQ1EjKODFEzGH9qPBBfE6BNdl3naHuYgIS3Uz8FCAwsOZAW6X8tC7VU/ZrwKUA\nF3Rc2iek+J1bdaz5o3hnR2eY/6kVuNHznxqIzK+JuZ7Dq/wEMlAL4gkCgYEA7Eyb\n4uyQFMXfPLiZPn7opNlgmi4i5lNLbPAjJq0dagdP8HbhLBqQThMcyAnu9rJmNm6t\n2Wu8kkKIpcZiGOVzFQvoTWOm6KGU/nIFFH1p6AAz/hvhATFA8HpLe9B7la9T6c5R\nabbtFbUNrHyoieMsIxkrjPo1zVIThLJeIVdoUNsCgYEAwuhKyV4MpSU06rxUhsTs\nsXwRaJLKnSiw5hPFT8ZuE0XrB8YNV52LwvphSRA46sF8HVeevxlmMTK/4wqBoSty\nZDIKAGoD5IAtpTU4xW4nf845xhe1spAb4PZzh5xLqMqQ9tYp0eVUImcDlyjp1x2e\n+TiOrFlXrqE/dOO39Q3MQpECgYEA5plMd4OMh/kiBcvQIOEQf+9zCoODo2od7U3b\nv96pGdPQ+0XIMJYrxUV5jO3EuhMXFH+mQMuW1tT/LWgQS2N/j0ZziTJ6rAMjt7vl\noT1SoQmxs4XZaqR6TzPJfibStBzJsx2Y7aWKcOijU3TDtOxxIj9p9MYowxoZ2iGH\nItp9/okCgYEAh6lbVbf77NArp1FsocQoeZ2ZL1hsOXpmRwpNmePPA6DfjqJyttpH\ngSh8Z0daqMvojStilhwIkEURy9ITuPYoKt2blWQY8RY//H1zFnwKg2AJR5PvlWcT\n0JBxt4cHMYy6jW2Q8/ZTVuttPd+UVIDehTFN6oyWF6FBgKxLO5bSjzc=\n-----END RSA PRIVATE KEY-----
IssuingCA   | Content of the trusted certificate. It is mandatory. <br> e.g -----BEGIN CERTIFICATE-----\nMIIFJjCCAw6gAwIBAgIUDUnfHPvwqpztM2lJh40lVUmTjV8wDQYJKoZIhvcNAQEL\nBQAwKzEpMCcGA1UEAwwgc2VsZnNlcnZlX3Byb2R1Y3Rpb25fcGtpIFJvb3QgQ0Ew\nHhcNMTcwODI1MDUwNTEzWhcNMjcwODIzMDUwNTQzWjArMSkwJwYDVQQDDCBzZWxm\nc2VydmVfcHJvZHVjdGlvbl9wa2kgUm9vdCBDQTCCAiIwDQYJKoZIhvcNAQEBBQAD\nggIPADCCAgoCggIBAM5LpBH9Qyg5VjTkdMj61gt72CVIrqE5s9iD+Bpb2hlLnWdb\n52FtcgCxIRca8kJhCYK53dNVmCP8d7LSzogxdIHyzEe5f405ukJVZIbYEYcA4BLK\n3UU322bYJkTTToABwV+XhlHjLhaze9GLo4snCklxAzafWvqR1C0faB2dPtq5WyQi\n/2uCvGHcpqe/ozNvZON6eYkjQpCwHftR0TwVVb435hvJb6FeeV95MgVq/C0pZFG4\nGLgJNj4GK4BtG2wsIDVMMcaoFrSKfKDqyE+4ekvzYP4nDzbYK5XsgH7/7XB9tL7w\nwMVj0J1mR3TbxVTBZyk509F0oXqBcNb6vvybJevhDlkXMQPgxyOmogm6GUQ3beMX\nsRpN5uotnbWaF0MQbgo8YrgQX3BGrLmKRfk9rIMoBKabptDMRw5Df1ouu5D9Jb3b\n3nlelkRXR5qb0R68CM0S78KqVB32NQsLixQ58YUKmcvlQcaIF9cwC28+LYm4sRq/\nV0tCl68K19PmgZT+Qr0Apakw+vlQ8ojvT+/wTVtg+gphuG7Ovv00xRXa/dpoC3Ff\nOktxUmu3bh4YU/IVCT3+YbwB7vyOfKGTwSmVK+s5gt4MDM65zX58xa85psJI8mqP\nCwKGDleglrAIrHxxg2wKrIibiIriSnjJsKqCzpcm9+6V4zewwQFqdfr1R92rAgMB\nAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQW\nBBQNl+8T/jYl1zV4Sct1EKqHBDcUUzANBgkqhkiG9w0BAQsFAAOCAgEAYo+vaKzi\nW2YTogGvuDvWnFzDtRa6zfB1UNqUTiacmr9ISqTDGJPOE7o7+5//31yS63/VuPAb\nsskfjtbywGUcjLEoa//vqDUA5VPQSr2MGpqZItt+QQ7eIQPQEt6IaqohmIxvgyDI\nvV35Ld06slZju9IZJdOx5GyRU49ZrhTciNeHBFJbPTzTWw7swjP1Kj13BJ9++YlU\ndHHnJecMgRPXbbFn8cThcIUwhaTEWFhlC7zc4YUpTm8nmHaCLmG8TM7tYLaymHqd\nypMBa3TrGr4+XIgwkWWb9h9+JnlBXc+aq2pJulErzN3raytzv+iTOwcI+YCufgee\nAf25Zzk9t75KIHjSdqu1U/QXiPSgJgr7o2yrtZbeLT+eMHuhCfbuWduipuRgTlUk\na8hvoiFDabCrlJABDYHNO8WMCIqX9qja0crqA1JbPXAEMiYwdtoU+p27CtNupGVE\nQENamacyYD5VhApTnxACwwakMep0jDYQUXUYTeLz6Aj3vVUJl54/3Uqbh6fxKamh\n8xDeb+HjhO5UKDkfAH0qe17qSGGVftMI3YMPCEqrvnnoVl8VHxpvdVjjJoHEEKoE\ne8mrX4Jp9O3xVcGFItMQQzvWc1A47ewqIy6x+bk+0W8fL6+rKd+8U7aRIvC7LFiw\nluvq3QIacuHULtox36A7HFmlYDQ1ozh+tLI=\n-----END CERTIFICATE-----
KeyStorePass  | Specifies the keystore password. If no value is specified, the default value "ibmkey" will be assigned.
DestinationHost | Specifies the Destination of the certificate. For example, testhost. Optional.

### BuildDockerImage_Base ###

Job Description: <br>

This job is to build a customized Docker image with the specified base docker image, and to build a customization package for a specified environment based on user's input (Tenant/NameSpace/EnvName/EnvType) to find target Dockerfile. Dockerfile is stored as ConfigMap and named with following naming pattern --dockerfile. You can use the "ManageDockerfile" job to create Dockerfile for the specified component or environment.

The backend logic is to detect if a target Dockerfile in ConfigMap is under the specified namespace with the UI input.<!--Tiffany: Meaning unclear-->

Job UI: <br>

<img src="./images/BuildDockerImageUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant | Tenant name. One tenant can contain multiple environments. In Kubernetes, tenant can be isolated by NameSpace.
NameSpace | Specifies the target NameSpace that the tenant belongs to.
EnvName  | Environment name
ForcePush | Specifies if whether force push for the Docker image is needed.
ForcePull | Content of the private key for the certificate. If the certificate is for two-way authentication, this value is mandatory. <br> e.g -----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAtuWgQ5P9KjpgplOyejAEj5pDgSmQ6mZkbqY6gnIIKlw1I4Vu\nlaigmeiir37NcAHtLA9HrpqafKoQqt3RPIFqMq2qb728JUNqdkmgp1QRnXdRVqrv\nGxT3o6XLMmxpkniwL+f3A/qFzuBgDJVltKLn1e0O3conPiiGtqaZ70+1lccKkKvi\nLoin13T+27gFFws6dT74znCxT8c/ikXGMja1TDEddd+qkXlo4At104Fo7Uhx95JW\norSljSTaCQkEeOjX+8SJHkARSrKeGEvkBESpXD23oUY9MlxGQnldioLAI5Eu8fRo\n3PKQUhuFnuoxTr0pO7R60AEe8E0sVU/cE3UtswIDAQABAoIBAB3kQ6An1K2NIvSs\nIzRTGru5k6TNfVDB8VIgOtnM90atEUY/7YXqLG1bFxOlnr/aoL+ds7J2tB8B0H2M\niUDhSdEEjyF6GgDhFspEWExgsgxRTuriPvfnIl4Nn7sa+tokfW8m8zkkPbBE/Y2w\n8RFnuoo9FzvqaSWAjBvX+LqjBWN4AGHxPcBcZs/H4U7RvdO0etX2Zbpjs62K/KO3\ni3e4MXgGZtj0Vx2LYD/AYSbqEoo1v8/U1AbGmsCTTNc2EwARhyb1zUgO7yc9yft6\nUoAC6pZjxOFsJtwz26jpNdqXz9t1xml3XnNusqHe+hgStQlIL2mgU8qj18q5pqpu\nkehM9LECgYEAxiU9WA7kQTp8hGKTRqrRbcGBsLTGxsYeILFQggtJBOZ5ngOH35Nd\nUIzQ1EjKODFEzGH9qPBBfE6BNdl3naHuYgIS3Uz8FCAwsOZAW6X8tC7VU/ZrwKUA\nF3Rc2iek+J1bdaz5o3hnR2eY/6kVuNHznxqIzK+JuZ7Dq/wEMlAL4gkCgYEA7Eyb\n4uyQFMXfPLiZPn7opNlgmi4i5lNLbPAjJq0dagdP8HbhLBqQThMcyAnu9rJmNm6t\n2Wu8kkKIpcZiGOVzFQvoTWOm6KGU/nIFFH1p6AAz/hvhATFA8HpLe9B7la9T6c5R\nabbtFbUNrHyoieMsIxkrjPo1zVIThLJeIVdoUNsCgYEAwuhKyV4MpSU06rxUhsTs\nsXwRaJLKnSiw5hPFT8ZuE0XrB8YNV52LwvphSRA46sF8HVeevxlmMTK/4wqBoSty\nZDIKAGoD5IAtpTU4xW4nf845xhe1spAb4PZzh5xLqMqQ9tYp0eVUImcDlyjp1x2e\n+TiOrFlXrqE/dOO39Q3MQpECgYEA5plMd4OMh/kiBcvQIOEQf+9zCoODo2od7U3b\nv96pGdPQ+0XIMJYrxUV5jO3EuhMXFH+mQMuW1tT/LWgQS2N/j0ZziTJ6rAMjt7vl\noT1SoQmxs4XZaqR6TzPJfibStBzJsx2Y7aWKcOijU3TDtOxxIj9p9MYowxoZ2iGH\nItp9/okCgYEAh6lbVbf77NArp1FsocQoeZ2ZL1hsOXpmRwpNmePPA6DfjqJyttpH\ngSh8Z0daqMvojStilhwIkEURy9ITuPYoKt2blWQY8RY//H1zFnwKg2AJR5PvlWcT\n0JBxt4cHMYy6jW2Q8/ZTVuttPd+UVIDehTFN6oyWF6FBgKxLO5bSjzc=\n-----END RSA PRIVATE KEY-----
BuildInfo | Specifies the build information.

<!--For BuildInfo is like a Json format to specify customzied docker build information for each component

For example:  IF you input Tenant=demo Namespace=default  EnvName=qa In DockerImage you defined the search-app  as below
{
     "name":"search-app",
     "base":"xxxxx",   // this is the base docker image tag, as default it will download docker image from <dockerRepo>/commerce/<name>:<base>
     "bundle": "xxxx", // this is customization package url, you can input a http://... link directly here or you can integrate with Nexus
     "version": "xxx"   // this is the new docker image tag. For example. when finish build the docker image, it will be tag as  <dockerRepo>/<Tenant>/search-app-cus:<version> and based on this docker image name to push to dockerRepo
}-->

### BundleCert_Base ###

Job Description: <br>

BundleCert_Base bundles third-party certificates with the target component. This job is done after the AddCert job. One component can be bundled with multiple third-party certificates.

Job UI: <br>

<img src="./images/BundleCertUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI Parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant | Tenant name. One tenant can contain multiple environments. In the Kubernetes context, the tenant environments can be isolated <!--Tiffany: divided?--> by NameSpace.
EnvName  | Environment name for a specific tenant.
Component | Specify the target component to bundle third-party certificates.
BundledCerts | Automatically fetches the certificates that are bundled with current components.
SelectedCerts | Based on the selection of tenant names, it can automatically list all third-party certification record. You can select the target certificates and click the build button will bundle the certification to target component. <!--Tiffany: What values are included? What will the param. do?-->

### CreateTenant_Base ###

Job Description:<br>

This job will create a new storage backend which named as the Tenant name. After create new tenant finish
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
