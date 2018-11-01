import kube_vars as globalvars
import kube_logs as kubelog
import requests
from requests import Request, Session
import json
import threading
import datetime
import yaml
import os
from os.path import dirname

KUBE_SERVIE_DOMIAN=".svc.cluster.local"

def CheckDependence(parser_args):
    '''
    IF envtype is live
        IF component is crs
             check search slave service status
        ELSE
             check live transaction service status
    IF envtype is auth
        IF component is crs
              check search master service status
        ElSE
              check auth transaction service status
    '''

    global serviceDepArray
    global_serviceDepArray=loadServiceDep(parser_args.component,None)

    start_time = datetime.datetime.now()
    timer = threading.Timer(int(parser_args.interval_time), checkServiceStatus, (parser_args, start_time,global_serviceDepArray))
    timer.start()

def checkServiceStatus(parser_args,start_time,serviceDepArray):
    timeAccount(start_time, int(parser_args.expect_during_time), int(parser_args.interval_time))

    print("check service status for %s " %(parser_args.component))

    loadServiceDep(parser_args.component,serviceDepArray)

    print(serviceDepArray)

    for index_of_dep_component_name in range(len(serviceDepArray)):
       _component_name=serviceDepArray[index_of_dep_component_name]
       if _checkServiceStatus(parser_args, serviceDepArray[index_of_dep_component_name]):
           print("Dependence service %s status check Pass" %(_component_name))
           serviceDepArray[index_of_dep_component_name]="Pass"

    timer = threading.Timer(int(parser_args.interval_time), checkServiceStatus, (parser_args, start_time,serviceDepArray))
    timer.start()

def loadServiceDep(component_name,serviceDepArray):

    if serviceDepArray == None :
        if serviceCheckConfig['ServiceDepMap']:
            if serviceCheckConfig['ServiceDepMap'][component_name]:
                print('Find component %s in ServiceDepMap List' %(component_name))
                serviceDepArray = serviceCheckConfig['ServiceDepMap'][component_name]
                return serviceDepArray
            else:
                print("Can not find the dependence definition, ignore dependence check!")
                exit(0)
        else:
            print("Can not find the dependence definition, ignore dependence check!")
            exit(0)
    else:
        serviceDepArray = [elem for elem in serviceDepArray if elem != "Pass"]

        if len(serviceDepArray) == 0:
            print("All dependence service are success status !")
            exit(0)

def timeAccount(start_time, expect_during_time, interval_time):

    if expect_during_time < interval_time:
        print("during time samller then the interval time")
        exit(1)

    end_time = datetime.datetime.now()
    real_during_time = (end_time - start_time).seconds
    print("real during time is %d second" % (real_during_time))
    if real_during_time > expect_during_time:
        print("check service status time out !")
        exit(1)

def _checkServiceStatus(parser_args,dep_component_name):

       #Add database status check
       if dep_component_name == "database":
           if serviceCheckConfig['Others'][dep_component_name]:
               checkMethod = serviceCheckConfig['Others'][dep_component_name].split("@")
               if checkMethod[0] == "checklog":
                  try:
                     isMatch , _ = kubelog.CheckContainerLog(None,parser_args.tenant+parser_args.env+parser_args.envtype+"db",None,parser_args.namespace,checkMethod[1])
                     return isMatch
                  except Exception as error:
                     print("catch database health check expection! %s" %(repr(error)))
                     return False
               else:
                   print("unsupport check method %s"  %(checkMethod[0]))
                   exit(1)
           else:
               print("Can not find check method for %s" % (dep_component_name))
               exit(1)
       else:
          request = requests.Session()
          headers = {"Authorization": "Basic " + parser_args.spiuser_pwd_encrypte}
          try:
            response = request.get(serviceURL(parser_args,dep_component_name), verify=False, headers=headers,timeout=int(parser_args.timeout))
            print(response.status_code)
            if response.status_code == 200:
              print("Dependent service response 200!")
              return True
          except Exception as error:
            # In case the service not ready
            print("catch health check request expection! %s " %(repr(error)))
            return False
       return False

def loadServiceCheck():
    _serviceCheckConfigFile = open(dirname(os.path.realpath(__file__)) + os.sep + "service_dependence_map.yml")
    _serviceCheckConfig = yaml.load(_serviceCheckConfigFile)
    return _serviceCheckConfig


def serviceURL(parser_args,dep_component_name):
    _serviceULR=None

    if dep_component_name == "search":
         if parser_args.envtype == "live":
             _componentName="search-app-slave"
         elif parser_args.envtype == "auth":
             _componentName = "search-app-master"
         else:
            print("enviornment typy not support !")
            exit(1)
    elif dep_component_name == "transaction":
        _componentName = "ts-app"
    elif dep_component_name == "store":
        _componentName = "crs-app"
    elif dep_component_name == "transaction-web":
        _componentName = "ts-web"
    elif dep_component_name == "userextenion":
        _componentName = "xc-app"
    else:
        print("component {dep_compont} is not support".format(dep_compont=dep_component_name))
        exit(1)
    _serviceName=parser_args.tenant+parser_args.env+parser_args.envtype+_componentName+"."+parser_args.namespace+KUBE_SERVIE_DOMIAN
    print("server name is %s" %(_serviceName))

    #For local testing to hardcode the return to localhost
    # _serviceName='localhost'

    if serviceCheckConfig['ServiceURL'][dep_component_name]:
        _serviceULR=serviceCheckConfig['ServiceURL'][dep_component_name].format(service_name=_serviceName)
    else:
        print("Can not find URL for specify service %s" %(dep_component_name))
        exit(1)
    print("Service name is %s" %(_serviceName))

    if _serviceULR == None:
        print("Can not generate service URL !")
        exit(1)
    return _serviceULR

# Init subparser for dependence check related command
_secureSubParser=globalvars.get_value('SubCMDParser')

depcheckParser = _secureSubParser.add_parser('depcheck', help='check status of dependence service for component when container startup')
depcheckParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
depcheckParser.add_argument('-env', type=str, default='qa', help='specify the environment name, default value is qa')
depcheckParser.add_argument('-envtype', type=str, default='auth', help='specify environment type [live | auth] for current environment, default value is auth')
depcheckParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
depcheckParser.add_argument('-component', type=str, help='specify current component which startup rely on the dependence check')
depcheckParser.add_argument('-interval_time', type=str, default='10', help='specfy interval time for status check')
depcheckParser.add_argument('-timeout', type=str, default='10', help='specfy timeout for the healthcheck request')
depcheckParser.add_argument('-expect_during_time', type=str, default='180', help='specfy expect service status check during time')
depcheckParser.add_argument('-spiuser_pwd_encrypte', type=str, default='c3BpdXNlcjpwYXNzdzByZA==', help='specfy encrypted spiuser password str by command: echo -n "spiuser:password" | base64')


depcheckParser.set_defaults(func=CheckDependence)
globalvars.set_value('SubCMDParser',_secureSubParser)

# pre-load service check configuration
serviceCheckConfig=loadServiceCheck()



