from kubernetes.client.rest import ApiException
import kube_vars as globalvars
import kube_factory as factory
from kubernetes import client, config
import argparse
import sys

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

def ListPods_by_Label(parser_args):
    if (parser_args.mode == "inCluster") :
        config.load_incluster_config()
    elif (parser_args.mode == "outCluster"):
        config.load_kube_config()
    else:
        print("error mode configuration")
        sys.exit(1)
    v1 = client.CoreV1Api()

    candaditePods=[]
    pod_list = v1.list_namespaced_pod(namespace=parser_args.namespace_name, label_selector=parser_args.label_selector)
    for i in pod_list.items:
        candaditePods.append(i.metadata.name)


Parser = argparse.ArgumentParser(add_help=True)
SubParsers = Parser.add_subparsers(help='Sub Commands')


Pod_Parser = SubParsers.add_parser('listpods_by_label', help='this command used to list the pod')
Pod_Parser.add_argument('-mode',type=str,default='outCluster',help='choose inCluster or outCluster')
Pod_Parser.add_argument('-namespace_name',type=str,default='default',help='the namespace name')
Pod_Parser.add_argument('-label_selector',type=str,default='',help='lable selector')
Pod_Parser.set_defaults(func=ListPods_by_Label)
