#  Using WebSphere Commerce DevOps Utilities #

## Overview ##
The DeployController component is built as a Jenkins Master, which includes pre-defined Jenkins jobs and backend scripts. There are global variables to define and control the execution context of the utility, such as the global configuration center and Docker repository host.

DeployController is acting like a "Hub" to integrate all tools that you need to deploy WebSphere Commerce V9. With DeployController, you can customize the jobs and backend scripts based on your requirements, as well as deploying your WebSphere Commerce environment through the user interface instead of the command-line interface.

As default, all container will be triggered from DeployController should be under commerce project with latest tag in private Docker repository.

<!--Admin also can use role based access control to create different view for different user.

Jenkins Job is most like MVC framework.  Jenkins UI define the View layer. You can change the Jenkins Job UI through "Configuration" page.
each Jenkins Job has pipeline which is most like controller to control the sequence of stage in current Job.  Backend scritps is most like the
model layer to finish the real action and manage data.-->

## Configuring your operational context through global variables ##
Before you start the operational job, configure the global variables. These variables can be configured when you perform deployment tasks by passing related values to the Docker container. Or you can configure the variables manually on the `Configuration System` page of Jenkins.

Parameter  |  Description
------------- | -------------
vault_url |  Vault URL (for example, http://9.112.245.194:30552 ). If InCluster is set to `true`, vault_url is not mandatory.
vault_token  | Vault Root Token for REST access. If InCluster is set to `true`, tvault_toke is not mandatory. For more information, see [Vault/Cousul based configuration management](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/com.ibm.commerce.install.doc/refs/rigvaultmetadata.htm).
bundleRepo |Repository destination for storing the customization packages. Nexus is the default bundle repository (for example,  http://9.110.182.156:8081/nexus/content/repositories/releases/commerce).
vault_url |  Vault URL (for example, http://9.112.245.194:30552 ). If InCluster is set to `true`, vault_url is not mandatory.
vault_token  | Vault Root Token for REST access. If InCluster is set to `true`, tvault_toke is not mandatory. For more information, see [Vault/Cousul based configuration management](https://www.ibm.com/support/knowledgecenter/SSZLC2_9.0.0/com.ibm.commerce.install.doc/refs/rigvaultmetadata.htm).
bundleRepo | Repository destination for storing the customization packages. Nexus is the default bundle repository (for example,  http://9.110.182.156:8081/nexus/content/repositories/releases/commerce).
dockerRepoHost | Hostname for the Docker image repository (for example, DockerRepoHostname:RepoPort).
dockerRepoUser   | User ID to access the Docker image repository when downloading the Docker image.
dockerRepoPwd  | Password to access the Docker image repository when downloading the Docker image.
helmChartsRepo  | The Helm Charts repository for storing Helm Charts to be triggered by the Jenkins job. (e.g http://9.112.245.194:8879/charts)


<!--Global can be configured when you do deploy by pass related value to Docker Container, or you can configure them by manually in "Configuration System" page of Jenkins <br>
<img src="./images/DeployController-GlobalConfig1.png" width = "500" height = "350" alt="Overview" align=center /><br>-->

## Pre-defined operational jobs ##

### AddCerts_Base ###

Job description: <br>

Create third-party certificate for the specified environment on a specified tenant. After adding third-party certificate, you can use the "BundleCert" job to bundle
specific certificate on the target component. If you deploy WebSphere Commerce V9 by setting the Configure Mode `Vault_CA` to `true`, the component container will fetch the bundled certificate
and apply it.

Job UI: <br>

<img src="./images/AddCertUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant |  Tenant name. One tenant can contain multiple environments. In Kubernetes, tenant can be separated by NameSpace.
EnvName  | Environment name.
CertName | Certificate name. The alias name in keystore.
PrivateKey | Content of private key for the certificate. If the certificate is used for two-way authentication, this value is mandatory. <br> e.g -----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAtuWgQ5P9KjpgplOyejAEj5pDgSmQ6mZkbqY6gnIIKlw1I4Vu\nlaigmeiir37NcAHtLA9HrpqafKoQqt3RPIFqMq2qb728JUNqdkmgp1QRnXdRVqrv\nGxT3o6XLMmxpkniwL+f3A/qFzuBgDJVltKLn1e0O3conPiiGtqaZ70+1lccKkKvi\nLoin13T+27gFFws6dT74znCxT8c/ikXGMja1TDEddd+qkXlo4At104Fo7Uhx95JW\norSljSTaCQkEeOjX+8SJHkARSrKeGEvkBESpXD23oUY9MlxGQnldioLAI5Eu8fRo\n3PKQUhuFnuoxTr0pO7R60AEe8E0sVU/cE3UtswIDAQABAoIBAB3kQ6An1K2NIvSs\nIzRTGru5k6TNfVDB8VIgOtnM90atEUY/7YXqLG1bFxOlnr/aoL+ds7J2tB8B0H2M\niUDhSdEEjyF6GgDhFspEWExgsgxRTuriPvfnIl4Nn7sa+tokfW8m8zkkPbBE/Y2w\n8RFnuoo9FzvqaSWAjBvX+LqjBWN4AGHxPcBcZs/H4U7RvdO0etX2Zbpjs62K/KO3\ni3e4MXgGZtj0Vx2LYD/AYSbqEoo1v8/U1AbGmsCTTNc2EwARhyb1zUgO7yc9yft6\nUoAC6pZjxOFsJtwz26jpNdqXz9t1xml3XnNusqHe+hgStQlIL2mgU8qj18q5pqpu\nkehM9LECgYEAxiU9WA7kQTp8hGKTRqrRbcGBsLTGxsYeILFQggtJBOZ5ngOH35Nd\nUIzQ1EjKODFEzGH9qPBBfE6BNdl3naHuYgIS3Uz8FCAwsOZAW6X8tC7VU/ZrwKUA\nF3Rc2iek+J1bdaz5o3hnR2eY/6kVuNHznxqIzK+JuZ7Dq/wEMlAL4gkCgYEA7Eyb\n4uyQFMXfPLiZPn7opNlgmi4i5lNLbPAjJq0dagdP8HbhLBqQThMcyAnu9rJmNm6t\n2Wu8kkKIpcZiGOVzFQvoTWOm6KGU/nIFFH1p6AAz/hvhATFA8HpLe9B7la9T6c5R\nabbtFbUNrHyoieMsIxkrjPo1zVIThLJeIVdoUNsCgYEAwuhKyV4MpSU06rxUhsTs\nsXwRaJLKnSiw5hPFT8ZuE0XrB8YNV52LwvphSRA46sF8HVeevxlmMTK/4wqBoSty\nZDIKAGoD5IAtpTU4xW4nf845xhe1spAb4PZzh5xLqMqQ9tYp0eVUImcDlyjp1x2e\n+TiOrFlXrqE/dOO39Q3MQpECgYEA5plMd4OMh/kiBcvQIOEQf+9zCoODo2od7U3b\nv96pGdPQ+0XIMJYrxUV5jO3EuhMXFH+mQMuW1tT/LWgQS2N/j0ZziTJ6rAMjt7vl\noT1SoQmxs4XZaqR6TzPJfibStBzJsx2Y7aWKcOijU3TDtOxxIj9p9MYowxoZ2iGH\nItp9/okCgYEAh6lbVbf77NArp1FsocQoeZ2ZL1hsOXpmRwpNmePPA6DfjqJyttpH\ngSh8Z0daqMvojStilhwIkEURy9ITuPYoKt2blWQY8RY//H1zFnwKg2AJR5PvlWcT\n0JBxt4cHMYy6jW2Q8/ZTVuttPd+UVIDehTFN6oyWF6FBgKxLO5bSjzc=\n-----END RSA PRIVATE KEY-----
IssuingCA   | Content of the trusted certificate. It is mandatory. <br> e.g -----BEGIN CERTIFICATE-----\nMIIFJjCCAw6gAwIBAgIUDUnfHPvwqpztM2lJh40lVUmTjV8wDQYJKoZIhvcNAQEL\nBQAwKzEpMCcGA1UEAwwgc2VsZnNlcnZlX3Byb2R1Y3Rpb25fcGtpIFJvb3QgQ0Ew\nHhcNMTcwODI1MDUwNTEzWhcNMjcwODIzMDUwNTQzWjArMSkwJwYDVQQDDCBzZWxm\nc2VydmVfcHJvZHVjdGlvbl9wa2kgUm9vdCBDQTCCAiIwDQYJKoZIhvcNAQEBBQAD\nggIPADCCAgoCggIBAM5LpBH9Qyg5VjTkdMj61gt72CVIrqE5s9iD+Bpb2hlLnWdb\n52FtcgCxIRca8kJhCYK53dNVmCP8d7LSzogxdIHyzEe5f405ukJVZIbYEYcA4BLK\n3UU322bYJkTTToABwV+XhlHjLhaze9GLo4snCklxAzafWvqR1C0faB2dPtq5WyQi\n/2uCvGHcpqe/ozNvZON6eYkjQpCwHftR0TwVVb435hvJb6FeeV95MgVq/C0pZFG4\nGLgJNj4GK4BtG2wsIDVMMcaoFrSKfKDqyE+4ekvzYP4nDzbYK5XsgH7/7XB9tL7w\nwMVj0J1mR3TbxVTBZyk509F0oXqBcNb6vvybJevhDlkXMQPgxyOmogm6GUQ3beMX\nsRpN5uotnbWaF0MQbgo8YrgQX3BGrLmKRfk9rIMoBKabptDMRw5Df1ouu5D9Jb3b\n3nlelkRXR5qb0R68CM0S78KqVB32NQsLixQ58YUKmcvlQcaIF9cwC28+LYm4sRq/\nV0tCl68K19PmgZT+Qr0Apakw+vlQ8ojvT+/wTVtg+gphuG7Ovv00xRXa/dpoC3Ff\nOktxUmu3bh4YU/IVCT3+YbwB7vyOfKGTwSmVK+s5gt4MDM65zX58xa85psJI8mqP\nCwKGDleglrAIrHxxg2wKrIibiIriSnjJsKqCzpcm9+6V4zewwQFqdfr1R92rAgMB\nAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQW\nBBQNl+8T/jYl1zV4Sct1EKqHBDcUUzANBgkqhkiG9w0BAQsFAAOCAgEAYo+vaKzi\nW2YTogGvuDvWnFzDtRa6zfB1UNqUTiacmr9ISqTDGJPOE7o7+5//31yS63/VuPAb\nsskfjtbywGUcjLEoa//vqDUA5VPQSr2MGpqZItt+QQ7eIQPQEt6IaqohmIxvgyDI\nvV35Ld06slZju9IZJdOx5GyRU49ZrhTciNeHBFJbPTzTWw7swjP1Kj13BJ9++YlU\ndHHnJecMgRPXbbFn8cThcIUwhaTEWFhlC7zc4YUpTm8nmHaCLmG8TM7tYLaymHqd\nypMBa3TrGr4+XIgwkWWb9h9+JnlBXc+aq2pJulErzN3raytzv+iTOwcI+YCufgee\nAf25Zzk9t75KIHjSdqu1U/QXiPSgJgr7o2yrtZbeLT+eMHuhCfbuWduipuRgTlUk\na8hvoiFDabCrlJABDYHNO8WMCIqX9qja0crqA1JbPXAEMiYwdtoU+p27CtNupGVE\nQENamacyYD5VhApTnxACwwakMep0jDYQUXUYTeLz6Aj3vVUJl54/3Uqbh6fxKamh\n8xDeb+HjhO5UKDkfAH0qe17qSGGVftMI3YMPCEqrvnnoVl8VHxpvdVjjJoHEEKoE\ne8mrX4Jp9O3xVcGFItMQQzvWc1A47ewqIy6x+bk+0W8fL6+rKd+8U7aRIvC7LFiw\nluvq3QIacuHULtox36A7HFmlYDQ1ozh+tLI=\n-----END CERTIFICATE-----
KeyStorePass  | Specifies the keystore password. If no value is specified, the default value "ibmkey" will be assigned.
DestinationHost | Specifies the destination of the certificate. For example, testhost. It is optional.

### BuildDockerImage_Base ###

Job description: <br>

This job is to build a customized Docker image with the specified base Docker image, and to build a customization package for a specified environment based on user input (Tenant/NameSpace/EnvName/EnvType) in order to find the target Dockerfile.

Dockerfile is stored as ConfigMap and named according to the following naming pattern `--dockerfile`. You can use the "ManageDockerfile" job to create Dockerfile for the specified component or environment.

The job detects whether a target Dockerfile in ConfigMap is under the specified NameSpace based on the user input.

Job UI: <br>

<img src="./images/BuildDockerImageUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant | Tenant name. One tenant can contain multiple environments. In Kubernetes, tenant can be separated by NameSpace.
NameSpace | Specifies the target NameSpace that the tenant belongs to.
EnvName  | Environment name.
ForcePush | Specifies whether force push for the Docker image is needed.
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

Job description: <br>

BundleCert_Base bundles third-party certificates with the target component. This job is done after the AddCert job. One component can be bundled with multiple third-party certificates.

Job UI: <br>

<img src="./images/BundleCertUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant | Tenant name. One tenant can contain multiple environments. In the Kubernetes context, the tenant environments can be divided by NameSpace.
EnvName  | Environment name for a specific tenant.
Component | Specifies the target component to bundle third-party certificates.
BundledCerts | Automatically fetches the certificates that are bundled with current components.
SelectedCerts | Based on the selection of tenant names, it can automatically list all third-party certificate records. Selecting the target certificates and clicking the **Build** button bundles the certificates to the target component.

### CreateTenant_Base ###

Job description:<br>

This job creates a new storage backend with the name of the tenant. After creating new tenant,
you can use AddCert/BundleCert/ManageVaultConfig to manage data on Vault.

Job UI: <br>
<img src="./images/CreateTenantUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>
Parameters with "*" are mandatory:

Parameter  |  Description
------------- | -------------
Tenant (*) | Tenant name. One tenant can have multiple environments. In Kubernetes, tenant can be separated by NameSpace.
DedicatedRootCA  | Specifies whether to create a dedicated RootCA backend with a name as the tenant
CreatedDedicatedView | Specifies whether to create a dedicated Jenkins view for the target tenant.

### DeployWCSCloud_Base ###

Job description: <br>

Based on user input, this job is to install, update, or delete the WebSphere Commerce V9 environment with Helm by launching a temporary Pod with DeploySlave.

This job supports the following user actions:

+ **Install**: Perform this action to deploy a new WebSphere Commerce V9 environment by running the `helm install` command. If the new environment is of the same Tenant, EnvName, and EnvType, the previous environment is removed before installing the new environment.
+ **Update**: Perform this action to update existing WebSphere Commerce V9 environment by running the `helm update` command. This action can be applied in the following scenarios:
  + **Scale in**: Scaling in the replicas of pods with HelmChart_Values and then perform the update action.
  + **Scale out**: Scaling out the replicas of pods with HelmChart_Values and then perform the update action.
  + **Update the existing pods**: Refreshing the tag of the image with HelmChart_Values and then perform the update action.
+ **Delete**: Run the `Helm delete` command to delete the WebSphere Commerce V9 environment according to Tenant, EnvName, and EnvType.

Job UI: <br>
<img src="./images/DeployWCSCloudUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>
Parameters with "*" are mandatory:

Parameter  |  Description
------------- | -------------
Tenant (*)| Tenant name. One tenant can have multiple environments. In Kubernetes, tenant can be separated by NameSpace.
EnvName (*) |Target environment name.
EnvType (*) |Target environment type.
NameSpace |Target NameSpace that the environment is to deploy.
DeployAction (*)|Specifies deployment actions. Supported actions include install, update, and delete.
HelmChart_Values (*)| Helm Charts values. Default Values are provided based on user input from other fields.
HelmChart (*)|Specifies the Helm Chart name to be used (e.g. stable/HelmChartName  the HelmChart must exist in the remote Helm repository
ForceCreate |Specifies whether to force create a new environment. If you set the parameter to 'true', the existing release is deleted before the deployment
ReuseVaules | Specifies whether to reuse values when do upgrade.
DeleteAllAssociatedObject | Do not use.
EnableTLS | Specifies whether to enable TLS. 'false' is the default value, which means TLS is not enabled. **Note**: If you use ICP 2.1.0.3, Helm TLS will be enabled by default, and you need to build specified DeploySlave for it. For more information, see [How to build deployslave for helm TLS](./DeploySlaveDesign.md).
helm_ca  | If EnableTLS is set to true, this parameIf EnableTLS is set to true, this parameter is set through cert.pem.
helm_key | If EnableTLS is set to true, this parameter is set through key.pem.

Before you trigger this job, make sure all values of the HelmChart_Values parameter are correct.

Values of the Tenant / EnvType / NameSpace / EnvType / Vault Token / Vault URL parameters are to be updated based on the input from fields on the UI or from Jenkins global variables.

The following are some additional parameters that need to be set correctly:
* ImageRepo
2. SPIUserName
3. SPIUserPWDAES
4. SPIUserPWDBase64
5. Merchantkey
6. WebSphere Commerce V9 Image Tag
7. SupportC Image Tag
8. ExternalDomian
9. ConfigureMode ( Vault is the default config mode )


### ManageConfigMap_Base ###

Job description: <br>

This job is to create a ConfigMap object on Kubernetes.

The ConfigMap object name follows the following pattern under the target NameSpace:

``<Tenant><EnvName><EnvType>-<filename>``
Inputting the needed information in the job UI generates a unique object name.

You can also leverage this job to check the value from the existing ConfigMap by providing the correct key.

Job UI: <br>
<img src="./images/ManageConfigMapUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant | Tenant name. One tenant can have multiple enviornments. In Kubernetes, tenant can be separated with NameSpace.
EnvName  |Target environment name.
EnvType |Target environment type.
NameSpace | Target NameSpace that the environment is to deploy.
FileName | The key to store dates in the ConfigMap object. If you want to create a key/value pair, name the file with the `.properies` extension.
ValueData | Specify keys/values in the <key>=<value> format.

### ManageVaultConfig_Base ###

Job description: <br>

Add or update key/value on Vault in the specified tenant and environment.

Job UI: <br>
<img src="./images/ManageVaultConfigUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant | Tenant name. One tenant can have multiple enviornments. In Kubernetes, tenant can be separated with NameSpace.
EnvName  |Target environment name.
ConfigureOnVault | Automatically fetches the existing key/value on Vault based on Tenant / EnvName and displays the pairs in this field. If Vault is not configured, mandatory key paths are generated for you to input values.

### TriggerBuildIndex_Base ###

Job description: <br>

This job triggers the Search Build Index in the target environment.

Job UI: <br>
<img src="./images/TriggerBuildIndexUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant | Tenant name. One tenant can have multiple enviornments. In Kubernetes, tenant can be separated with NameSpace.
EnvName  | Target environment name.
EnvType | Target environment type.
NameSpace |Target NameSpace that the environment is to deploy.
MasterCatalogId |ID of the master catalog.
SpiUser | SPI user name.
SpiPwd  | SPI user password.

### TriggerIndexReplica_Base ###

Job description:  <br>

This job triggers the Search Build Index Replica in the target environment.

Job UI: <br>

<img src="./images/TriggerIndexReplicaUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant | Tenant name. One tenant can have multiple enviornments. In Kubernetes, tenant can be separated with NameSpace.
EnvName  | The name of the target environment that
is to be deployed.
SpiUser | SPI user name.
SpiPwd  | SPI user password.

### Utilities_DBClean_Base ###
Job description:  <br>

This job will launch a utilities docker image with specified tag and it will based on the input parameter to make utilities to do the configuration when startup. Then it will launch dbclean.sh to clean the data in specified table on Commerce database.

This is a sample job for your reference. You can based on it to create more job for your daily job requirement


Job UI: <br>

<img src="./images/Utilities_DBCleanUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant (*)| Tenant name. One tenant can have multiple environments. In Kubernetes, tenant can be separated by NameSpace.
EnvName (*) |Target environment name.
EnvType (*) | Target environment type.
UtilitiesDockerTag (*) | Target Utilities Docker image tag. By default, the tag is input from the WebSphere Commerce project in the private Docker repository.
ObjectName (*) | Specify target table name you want to do dbclean. cacheivl is the default table name for cache
Type (*) | Specify what action you want to do on object you specified. obsolete is the default action for delete object
DBName (*) | Specify target database name. mall is the default database name
DBUser (*) | Specify database user name ( instance user ). wcs is the default database user
DBPwd (*) | Specify database user password ( instance user password).
Day (*) | Specify how long time of data need to be clean. one day is the default value.
DBType (*) | Specify database type, DB2 is the default database type
OptionParameters | Empty as default, you can add option parameters of DBClean in this field


### Utilities_StagingProp_Base ###
Job description:  <br>

This job will launch a utilities docker image with specified tag and it will based on the input parameter to make utilities to do the configuration when startup. Then it will launch stagingprop.sh

Job UI: <br>

<img src="./images/Utilities_StagingPropUI.png" width = "300" height = "450" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant (*)| Tenant name. One tenant can have multiple environments. In Kubernetes, tenant can be separated by NameSpace.
EnvName (*) |Target environment name.
EnvType (*) | Target environment type.
UtilitiesDockerTag (*) | Target Utilities Docker image tag. By default, the tag is input from the WebSphere Commerce project in the private Docker repository.
DBType (*) | Specify database type, DB2 is the default database type
Scope (*) | Specify the scope of staging prop, "__all__" as default value.
SourceDB (*) | Specify the source database (e.g: IP:Port/DBName)
SourceDB_User (*) | Specify the source database user ( instance user )
SourceDBUser_Pwd (*) | Specify the source database user password ( instance user password )
DestDB (*) | Specify the destination database (e.g: IP:Port/DBName)
DestDB_User (*) | Specify the destination database user (instance user )
DestDB_User (*) | Specify the destination database user password
OptionParameters | Empty as default, fill in option parameter of StagingProp

### Utilities_UpdateDB_Base ###
Job description:  <br>

This job launches a utilities docker image with specified tags, configures databases based on input parameters during startup, and then launches `updatedb.sh` to update the database.

This is a sample job for your reference. You can create more jobs based on your business requirements.

Job UI: <br>

<img src="./images/Utilities_UpdateDBUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant (*)| Tenant name. One tenant can have multiple environments. In Kubernetes, tenant can be separated by NameSpace.
EnvName (*) |Target environment name.
EnvType (*) | Target environment type.
UtilitiesDockerTag (*) | Target Utilities Docker image tag. By default, the tag is input from the WebSphere Commerce project in the private Docker repository.
CmdParameters  | Command parameter for updating the database.

### Utilities_VersionInfo_Base ###
Job description:  <br>

This job is used to run `versionInfo.sh` in the Utilities Docker to check the current version information.

This example illustrates how to launch scripts in the Docker container.

Job UI: <br>

<img src="./images/Utilities_VersionInfoUI.png" width = "400" height = "250" alt="Overview" align=center /><br>

Job UI parameters: <br>

Parameter  |  Description
------------- | -------------
Tenant (*)| Tenant name. One tenant can have multiple environments. In Kubernetes, tenant can be separated by NameSpace.
EnvName (*) | Target environment name.
EnvType (*) | Target NameSpace that the environment is to deploy.
UtilitiesDockerTag (*) | SPI user name.
FullConfig  | Specifies whether utilities need to do full configuration, which leverages predefined configuration mode to set the environment in the container. The default value is true.

## Backend Scripts ##

Backend scripts located under path /commerce-devops-utilities/utilities in DeployController
