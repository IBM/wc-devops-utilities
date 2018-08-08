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

    _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if not _CoreV1Api:
        factory.Factory_InitKubeClient(parser_args.configtype, parser_args.configfile)
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')

    candaditePods=[]

    #sample for label and field_selector: label_selector="group=demoqalive,component=demoqalivecrs-app"  field_selector="status.phase=Running"
    pod_list = _CoreV1Api.list_namespaced_pod(namespace=parser_args.namespace_name, label_selector=parser_args.label_selector,field_selector=parser_args.field_selector)

    for item in pod_list.items:
        if item.status.container_statuses[0].state.running != 'None':
           candaditePods.append(item.metadata.name)
           #print(item.status.container_statuses[0].state.running)
           print(item.metadata.name + "," )


Parser = argparse.ArgumentParser(add_help=True)
SubParsers = Parser.add_subparsers(help='Sub Commands')

# Init subparser for dependence check related command
_secureSubParser=globalvars.get_value('SubCMDParser')
Pod_Parser=_secureSubParser.add_parser('listpods_by_label', help='this command used to list the pod')

Pod_Parser.add_argument('-namespace_name',type=str,default='default',help='the namespace name')
Pod_Parser.add_argument('-label_selector',type=str,default='',help='lable selector')
Pod_Parser.add_argument('-field_selector',type=str,default='',help='A selector to restrict the list of returned objects by their fields, List everything  as default')
Pod_Parser.set_defaults(func=ListPods_by_Label)
globalvars.set_value('SubCMDParser',_secureSubParser)

