# End-to-end guide on WebSphere Commerce DevOps Utilities#

This page provides you with end-to-end guidance on how to manage configuration through Vault and ConfigMap,
and deploy, update, delete the WebSphere Commerce V9 environment by leveraging the Commerce DevOps Utilities.

To better understand the entire process, I prefer to introduce it as story mode with some special role. This role based story can
help you better understand how to control a distribute environment on cloud platform. But this is not the best practice can match
all case. When you read this story, please base on your company's situation to thinking how to organize the process

Role: Operator <br>
Name: David <br>
As Operator, support Dev team to init environment and manage deploycontroller <br>
<img src="./images/David.png" width = "50" height = "40" alt="Overview" align=center /><br>

Role：Developer <br>
Name: Steve <br>
As Developer, develop code and use deploycontroller UI to build customized docker image
and update environment to verify new code change <br>
<img src="./images/Steve.png" width = "50" height = "40" alt="Overview" align=center /><br>


# Background #

One day, that must be a big day.  The Boss find David and Steve and told them Company decide to buildup self-hosted
E-Commerce site with IBM Commerce V9.  He want David and Steve and cooperate together to buildup this site from scratch.

Get this news update, David and Steve

# Section #

1. [PrepareInfrastructure](End2EndUsage_PrepareInfrastructure.md)
2. [InitTenantEnviornment](End2EndUsage_InitTenantEnvironment.md)
3. [DevelopeAndBuildCustomizedCode](End2EndUsage_DevelopAndBuildCustomizeCode.md)
4. [UpdateEnvWithCustomizedDocker](End2EndUsage_UpdateEnvWithCustomizeDocker.md)
