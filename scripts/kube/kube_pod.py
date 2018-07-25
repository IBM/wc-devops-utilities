from kubernetes.client.rest import ApiException
import kube_vars as globalvars
import kube_factory as factory


def ListPods(Client,NameSpace,PodNamePattern):
    _CoreV1Api = Client

    if _CoreV1Api == None:
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')

    if NameSpace == None:
        _namespace = "default"
    else:
        _namespace = NameSpace

    return listPods(_CoreV1Api,_namespace,PodNamePattern)


def listPods(Client,NameSpace,PodNamePattern):

    candaditePods=[]
    try:
        podlistObj = Client.list_namespaced_pod(NameSpace, pretty=True)
        for item in podlistObj.items:
           if PodNamePattern in item.metadata.name:
               candaditePods.append(item.metadata.name)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
        exit(1)
    return candaditePods