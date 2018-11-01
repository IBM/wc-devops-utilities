from kubernetes.client.rest import ApiException
import kube_vars as globalvars
import kube_factory as factory
import kube_pod
import re

def CheckContainerLog(Client,PodName,ContainerName,NameSpace,Message,Possization=0):
    print("Run CheckContainerLog in kube_log model")
    _CoreV1Api = Client

    if _CoreV1Api == None:
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')

    isMatch,matchStr= checkContainerLog(_CoreV1Api, PodName, ContainerName, NameSpace,Message,Possization)

    if isMatch:
        return True,matchStr
    return False,None


def checkContainerLog(Client,PodName,ContainerName,NameSpace,Message,Possization):

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
        return False,None
    try:
        if ContainerName != None:
          api_response = Client.read_namespaced_pod_log(_matchedPod, _namespace, container=ContainerName,pretty=True)
        else:
          api_response = Client.read_namespaced_pod_log(_matchedPod, _namespace,pretty=True)
        print(api_response)
        isBingo, matchStr= bingoTarget(_message,api_response,Possization)
        if isBingo:
            return True,matchStr
    except ApiException as e:
        print("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)
    return False,None

def prehandleMessage(message):
    return message.replace("\'","").replace("\"","")

def detectPodName(Client,NameSpace,PodNamePattern):
    return kube_pod.ListPods(Client,NameSpace,PodNamePattern)

def bingoTarget(target,source,posization):
    pattern = re.compile(target)
    print(target)
    if re.match(pattern,source.replace("\n","")) !=None:
       print("Find pattern %s " %(re.match(pattern,source.replace("\n","")).group(posization)))
       return True,re.match(pattern, source.replace("\n", "")).group(posization)
    print("not find target pattern %s" %(target))
    return False,None


