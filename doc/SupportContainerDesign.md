# Support Container Design #

## OverView ##
Support Container is used to support deployment flow just like its name. It can help check service, manage secret, manage
persistent volumes, manage config map for WCV9 application.
Only make a simple deployment for WCV9 application is not enough. The each component is not totally independent, which depends on other components. So we have to define own logic
to control the component dependency. WCV9 is a docker based application, they can not persist the changes once the container is started
due to docker specific character. But for search service, the index will be created dynamically in search docker container after 
the build index process is triggered. If the search service is updated with new image, the index will be lost. If the index
can be stored in a perstent volume, the index will not be lost. For a big index, it is very important. 

## Implement ##

All the specific requirements are implemented with python. So the support container not only includes the implemented python
modules, it also include a python runtime.

The support contain mainly include the following four modules. All the modules can accept the comandline paramters.

*kube_servicecheck.py  This module will load the dependency configuration file to get the dependency for the input component.
And check the service status at some interval. If the dependency service status is ok during the check time, dependency check 
is pass. If the service status always return wrong status during the check time.  The dependency check will fail due to time out.

*Kube_secret.py This module will invoke kubernetes API to create and delete secret. It will create or delete secret based on 
the input action. If the action is "create secret", the module will determine to create new secret or use old secret according to 
input flag.

*Kube_pvc.py This module will invoke kubernetes API to create and delete persistent volume. It will use glusterfs storage class to create 
persistent voluem claim by kubernetes API.

*Kube_configmap.py This module will invoke kubernetes API to manage configmap for input tenant
