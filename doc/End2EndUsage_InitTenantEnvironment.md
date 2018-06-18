# Init tenant environment #
  Once the infrastructure is ready, the operator need to plan to set up a tenant in the infrastructure. The tenant is like 
subsidiary of big company which is composed of many separate subsidiaries. Each subsidiary should take charge of all things 
for itself. A tenant shoulld be separate and isolate to other tenants as the subsidiary. The namespace in kubernetes can help implement tenant resouce isolation. Each tenant should have own namespace, which will reduce the impact of each other.
  
  A subsidary has many different department to handle different work. The tenant like the subsidary has different environment
to handle diffentent requirement, such as dev environment, qa environment, pre-production environment and production envioronment. The topology of dev envronment and qa environment may be diffent from pre-production and production environment, which should be a minimal environment including all the components. The pre-production and production environment should set up the topology based on the business requirements. This chapter will take the qa environment as an example.
  <img src="./images/qatopology.png" width = "700" height = "450" alt="Overview" align=center /><br>
  


  After the deployment topoloy is defined, the operator need to prepare database server and load data firstly. About how to do them, the operator can reference the [WebSphsere Commerce v9 info center](https://www.ibm.com/support/knowledgecenter/en/SSZLC2_9.0.0/com.ibm.commerce.install.doc/tasks/tiginstalldb2overview.htm). Until now, the operator has already set up the infrastruture and database server, he can begin to create a tenant by the deployed devops utility. 
  * Login the deploy controler(jekins master), default password is admin/admin. The operator can see all available jobs.
  <img src="images/joblist.png" width = "700" height = "450" alt="Overview" align=center /><br>
  * The operator use "CreateTenant_Base" job to create tenant. After the job is finished, the vault configuration center can receive the configuration info for this tenant. And the operator can see all the available jobs for this tenant.
  * The operator push db info, merchantkey info, spiuser info to vault configuration center.
  * After the configuration center is ready for this tenant, the operator can deploy the WebSphere Commerce V9 environment.
  By the "DeployWCSCloud_Base" job, the search, store, transaction, web component will be deployed. The ingress and secrete will also be configured.
  
  
  
  
  