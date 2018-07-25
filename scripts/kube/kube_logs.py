from kubernetes.client.rest import ApiException
import kube_vars as globalvars
import kube_factory as factory
import kube_pod
import re

def CheckContainerLog(Client,PodName,ContainerName,NameSpace,Message):
    print("Run CheckContainerLog in kube_log model")
    _CoreV1Api = Client

    if _CoreV1Api == None:
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')

    if checkContainerLog(_CoreV1Api, PodName, ContainerName, NameSpace,Message):
        return True
    return False

def checkContainerLog(Client,PodName,ContainerName,NameSpace,Message):

    if NameSpace == None:
        _namespace="default"
    else:
        _namespace=NameSpace
    _message=prehandleMessage(Message)

    #detect target pod and find the random name which given by Kubernetes
    matchPods=detectPodName(Client,NameSpace,PodName)
    if len(matchPods) !=0 :
       _matchedPod=matchPods[0]
       print("find target pod %s" %(_matchedPod))
    else:
        return False
    try:
        api_response = Client.read_namespaced_pod_log(_matchedPod, _namespace,pretty=True)
        print(api_response)
        if bingoTarget(_message,api_response):
            return True
    except ApiException as e:
        print("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)
        exit(1)
    return False

def prehandleMessage(message):
    return message.replace("\'","").replace("\"","")

def detectPodName(Client,NameSpace,PodNamePattern):
    return kube_pod.ListPods(Client,NameSpace,PodNamePattern)

def bingoTarget(target,source):
    pattern = re.compile(target)
    print(target)
    if re.match(pattern,source.replace("\n","")) !=None:
       print("Find pattern %s" %(target))
       return True
    print("not find target pattern %s" %(target))
    return False

