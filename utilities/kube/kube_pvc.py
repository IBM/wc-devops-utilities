import kube_vars as globalvars
import requests
from requests import Request, Session
import json
import threading
import datetime
import yaml
import os
import kube_factory as factory
from os.path import dirname
from kubernetes import client
from kubernetes.client.rest import ApiException


def CreateKubePVC(parser_args):
    '''
    1.check if there have the spcified storage class exist, if not , exit(1)
    2.check if there have the specified PVC exist
      IF not exist create
      IF exist ignore
    '''
    _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if not _CoreV1Api:
        factory.Factory_InitKubeClient(parser_args.configtype, parser_args.configfile)
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    is_pvcExist=_checkKubePVCStatus(parser_args, _CoreV1Api)

    if is_pvcExist:
        if parser_args.force=="true":
            DeleteKubePVC(parser_args)
        else:
            print("Reuse Exist Persistent Volume Chaim In Kubernetes")
            exit(0)
    _createKubePVC(parser_args, _CoreV1Api)


def DeleteKubePVC(parser_args):
    if parser_args.component=="search":
        # {tenantName}-{environment}-search-master-gluster-volume
        if parser_args.envtype == "auth":
            pvc_name=parser_args.tenant+parser_args.env+"-search-master-"+"volume"
        elif parser_args.envtype == "live":
            pvc_name=parser_args.tenant+parser_args.env+"-search-repeater-"+"volume"

        # Below config boby still need refine to accept more flexible extension
        body=client.V1DeleteOptions()
        try:
             apiInstance = globalvars.get_value('KubCoreV1Api')
             if not apiInstance:
                 factory.Factory_InitKubeClient(parser_args.configtype, parser_args.configfile)
                 apiInstance = globalvars.get_value('KubCoreV1Api')
             api_response = apiInstance.delete_namespaced_persistent_volume_claim(pvc_name, parser_args.namespace, body)
             print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_persistent_volume_claim: %s\n" % e)
    else:
        print("Compoennt %s should not have any persistent volumes" %(parser_args.component))

def _createKubePVC(parser_args,CoreV1Api):
    if parser_args.component=="search":
        # {tenantName}-{environment}-search-master-gluster-volume
        if parser_args.envtype == "auth":
            _pvc_name=parser_args.tenant+parser_args.env+"-search-master-"+"volume"
        elif parser_args.envtype == "live":
            _pvc_name=parser_args.tenant+parser_args.env+"-search-repeater-"+"volume"

        # Below config boby still need refine to accept more flexible extension
        metadata = {'name': _pvc_name, 'namespace': parser_args.namespace}
        requests = {'storage': parser_args.storage_size}
        _V1ResourceRequirements=client.V1ResourceRequirements(requests=requests)
        _V1PersistentVolumeClaimSpec=client.V1PersistentVolumeClaimSpec(resources=_V1ResourceRequirements,storage_class_name=parser_args.storage_class,access_modes=['ReadWriteMany'])
        body = client.V1PersistentVolumeClaim(api_version='v1',kind='PersistentVolumeClaim', metadata=metadata,spec=_V1PersistentVolumeClaimSpec,)  # V1PersistentVolumeClaim |

        try:
             api_response = CoreV1Api.create_namespaced_persistent_volume_claim(parser_args.namespace, body)
             print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_persistent_volume_claim: %s\n" % e)
    else:
        print("Compoennt %s not need to create persistent volume chain on Kubernetes" %(parser_args.component))

def _checkKubePVCStatus(parser_args,CoreV1Api):
    if parser_args.component=="search":
        # {tenantName}-{environment}-search-master-gluster-volume
        if parser_args.envtype == "auth":
            _pvc_name=parser_args.tenant+parser_args.env+"-search-master-"+"volume"
        elif parser_args.envtype == "live":
            _pvc_name=parser_args.tenant+parser_args.env+"-search-repeater-"+"volume"

        try:
          api_response = CoreV1Api.list_namespaced_persistent_volume_claim(parser_args.namespace)

          # print(api_response)

          for item in api_response.items:
              if item.metadata.name == _pvc_name:
                  print("Find target Persisten Volume Chaim %s in Kubernetes" %(_pvc_name))
                  return True
        except ApiException as e:
          print("Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: %s\n" % e)
    return False


# Init subparser for dependence check related command
_secureSubParser = globalvars.get_value('SubCMDParser')

createPVCParser = _secureSubParser.add_parser('createpvc', help='create persistent volume chain in kubernetes')
createPVCParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
createPVCParser.add_argument('-env', type=str, default='qa', help='specify the environment name, default value is qa')
createPVCParser.add_argument('-envtype', type=str, default='auth', help='specify environment type [live | auth] for current environment, default value is auth')
createPVCParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
createPVCParser.add_argument('-component', type=str, help='specify current component which startup rely on the dependence check')
createPVCParser.add_argument('-storage_class', type=str, default='GlusterFS', help='specify')
createPVCParser.add_argument('-access_modes', type=str, default='ReadWriteMany', help='specfy expect service status check during time')
createPVCParser.add_argument('-storage_size', type=str, default='5Gi', help='specfy expect service status check during time')
createPVCParser.add_argument('-force', type=str, default='false', help='specfy create a new PVC volume, instead of using exist one, will delete exist one first')

delPVCParser = _secureSubParser.add_parser('deletepvc', help='delete persistent volume chain in kubernetes')
delPVCParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
delPVCParser.add_argument('-env', type=str, default='qa', help='specify the environment name, default value is qa')
delPVCParser.add_argument('-envtype', type=str, default='auth', help='specify environment type [live | auth] for current environment, default value is auth')
delPVCParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
delPVCParser.add_argument('-component', type=str, help='specify current component which startup rely on the dependence check')

createPVCParser.set_defaults(func=CreateKubePVC)
delPVCParser.set_defaults(func=DeleteKubePVC)

globalvars.set_value('SubCMDParser',_secureSubParser)
