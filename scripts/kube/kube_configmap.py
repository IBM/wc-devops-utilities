import kube_vars as globalvars
import os
import kube_factory as factory
import kube_logs as logs
from kubernetes import client
from kubernetes.client.rest import ApiException


#Current file path
CURDIR = os.path.abspath(os.path.dirname(__file__)) + "/"


def CreateConfigMap(parser_args):
    _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if not _CoreV1Api:
        factory.Factory_InitKubeClient(parser_args.configtype, parser_args.configfile)
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if listConfigMap(parser_args, _CoreV1Api):
        print("find target config map %s" % (parser_args.tenant+parser_args.env+parser_args.envtype+"-"+parser_args.name))
        if parser_args.forcecreate == "true":
                deleteConfigMap(parser_args,_CoreV1Api)
                createConfigMap(parser_args,_CoreV1Api)
        else:
                patchConfigMap(parser_args,_CoreV1Api)
    else:
        print("create new config map %s" % (parser_args.name))
        createConfigMap(parser_args, _CoreV1Api)

#Create new configMap ( key-value or file ? )
def createConfigMap(parser_args,CorV1Client):
    data={}
    if parser_args.rawconfig !=None :
       keyvaluePaires=parser_args.rawconfig.split(";")
       for keyvalue in keyvaluePaires:
           _keyvalue=keyvalue.split("::")
           print(_keyvalue)
           data.update({_keyvalue[0]:_keyvalue[1]})
    else:
       configMap=readFileForConfigMap(parser_args)
       data.update(configMap)

    print("data is %s" % data)
    objectMeta=client.V1ObjectMeta(name=parser_args.tenant+parser_args.env+parser_args.envtype+"-"+parser_args.name,namespace=parser_args.namespace)
    body = client.V1ConfigMap(kind='ConfigMap',metadata=objectMeta,data=data)  # V1ConfigMap
    pretty = 'pretty_example'  # str | If 'true', then the output is pretty printed. (optional)
    try:
        api_response = CorV1Client.create_namespaced_config_map(parser_args.namespace, body, pretty=pretty)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)

def readFileForConfigMap(parser_args):
    #解析filepath 通过;号
    _configMap = {}
    if parser_args.configfiles != None:
       fileList=(parser_args.configfiles).split(";")
       print(fileList)
       for file in fileList:
           print("start to handle files %s" % file)
           if os.path.exists(file):
              if parser_args.configmaptype == "fromfile":
                  with open(file, 'r') as f:
                       content = ""
                       for line in f.readlines():
                           content += line
                       filename=os.path.basename(file)
                       _configMap.update({filename:content})
              elif parser_args.configmaptype == "fromenvfile":
                  with open(file, 'r') as f:
                       for line in f.readlines():
                           key,value=line.strip().split("=")
                           _configMap.update({file:value})
              else:
                  print("config map type not support!")
                  exit(1)
           else:
                  print("can not find %s" % file)
       print(_configMap)
       return _configMap
    else:
        print("can not find input parameters")
        exit(1)

# Delete configMap
def deleteConfigMap(parser_args,CorV1Client):
        print("delete config map")
        if listConfigMap(parser_args,CorV1Client):
            # create an instance of the API class
            name = parser_args.name  # str | name of the ConfigMap
            namespace = parser_args.namespace  # str | object name and auth scope, such as for teams and projects
            body = client.V1DeleteOptions()  # V1DeleteOptions |
            pretty = 'pretty_example'  # str | If 'true', then the output is pretty printed. (optional)

            try:
                api_response = CorV1Client.delete_namespaced_config_map(name, namespace, body, pretty=pretty)
                print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->delete_namespaced_config_map: %s\n" % e)
        else:
            print("Not Found target cofigMap ojbect %s exist" % parser_args.name)

#Delete configMap
def DeleteConfigMap(parser_args):
    _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if not _CoreV1Api:
        factory.Factory_InitKubeClient(parser_args.configtype, parser_args.configfile)
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    print("delete config map")
    if listConfigMap(parser_args, _CoreV1Api):
       # create an instance of the API class
       name = parser_args.name  # str | name of the ConfigMap
       namespace = parser_args.namespace  # str | object name and auth scope, such as for teams and projects
       body = client.V1DeleteOptions()  # V1DeleteOptions |
       pretty = 'pretty_example'  # str | If 'true', then the output is pretty printed. (optional)

       try:
          api_response = _CoreV1Api.delete_namespaced_config_map(parser_args.tenant+parser_args.env+parser_args.envtype+"-"+name, namespace, body, pretty=pretty)
          print(api_response)
       except ApiException as e:
          print("Exception when calling CoreV1Api->delete_namespaced_config_map: %s\n" % e)
    else:
       print("Not Found target cofigMap ojbect %s exist" % parser_args.name)

#DetectExistConfigMap
def listConfigMap(parser_args,CorV1Client):
    #print("list config map")
    try:
        api_response = CorV1Client.list_namespaced_config_map(parser_args.namespace)
        #print(api_response)
        config_map_items=api_response.items
        for config_map in config_map_items:
            if config_map.metadata.name == parser_args.tenant+parser_args.env+parser_args.envtype+"-"+parser_args.name:
                return True
        return False
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_config_map: %s\n" % e)

def patchConfigMap(parser_args,CorV1Client):
    print("patch config map")
    data = {}
    if parser_args.rawconfig != None:
        keyvaluePaires = parser_args.rawconfig.split(";")
        for keyvalue in keyvaluePaires:
            print("keyvalue is %s" % keyvalue)
            _keyvalue = keyvalue.split("::")
            print(_keyvalue)
            data.update({_keyvalue[0]: _keyvalue[1]})
    else:
       configMap=readFileForConfigMap(parser_args)
       data.update(configMap)
    objectMeta = client.V1ObjectMeta(name=parser_args.tenant+parser_args.env+parser_args.envtype+"-"+parser_args.name, namespace=parser_args.namespace)
    body = client.V1ConfigMap(kind='ConfigMap', metadata=objectMeta, data=data)
    pretty = 'pretty_example'  # str | If 'true', then the output is pretty printed. (optional)

    try:
        api_response = CorV1Client.patch_namespaced_config_map(parser_args.tenant+parser_args.env+parser_args.envtype+"-"+parser_args.name, parser_args.namespace, body, pretty=pretty)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->patch_namespaced_config_map: %s\n" % e)

def FetchConfigMap(parser_args):
    _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if not _CoreV1Api:
        factory.Factory_InitKubeClient(parser_args.configtype, parser_args.configfile)
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    #print("Fetch config map %s" % parser_args.name)
    try:
        api_response = _CoreV1Api.list_namespaced_config_map(parser_args.namespace)
        #print(api_response)
        config_map_items = api_response.items
        for config_map in config_map_items:
            #print("check config_map %s and compare with %s" % (config_map.metadata.name,parser_args.tenant+parser_args.env+parser_args.envtype+"-"+parser_args.name))
            if (config_map.metadata.name == parser_args.tenant + parser_args.env + parser_args.envtype + "-" + parser_args.name) or (config_map.metadata.name == parser_args.name):
                    _output=""
                    for key in config_map.data.keys():
                        if key.find('properties') == -1 and key.find('xml') == -1 and key.find('Dockerfile') == -1 and key.find('yaml') == -1:
                            _output = _output + key + "=" + config_map.data[key] + "\n"
                        else:
                            _output = _output + config_map.data[key]
                    print(_output)
                    return _output
        return ''
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_config_map: %s\n" % e)

# Add this command just satify ICP catalog UI to quick deploy a sample environment
def CreateSampleConf(parser_args):
    _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if not _CoreV1Api:
        factory.Factory_InitKubeClient(parser_args.configtype, parser_args.configfile)
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')

    _configMapKV={}
    try:
        print("Call kube_log to get Vault Token")
        _ , _vaultToken = logs.CheckContainerLog(_CoreV1Api, "vault.consul", "vault", parser_args.namespace, "^(.*)(\S{8}-\S{4}-\S{4}-\S{4}-\S{12})(.*)$",2)
        _configMapKV["VAULT_TOKEN"] =_vaultToken

        _configMapKV["DBHOST"] = parser_args.dbhost
        _configMapKV["DBNAME"] = parser_args.dbname
        _configMapKV["DBPASS"] = parser_args.dbpass
        _configMapKV["DBPORT"] = parser_args.dbport
        _configMapKV["DBTYPE"] = parser_args.dbtype
        _configMapKV["DBUSER"] = parser_args.dbuser
        _configMapKV["DBAUSER"] = parser_args.dbauser
        _configMapKV["DBAPASSENCRYPT"] = parser_args.dbapwdencrypt
        _configMapKV["DBPASSENCRYPT"] = parser_args.dbpwdencrypt

        # print(_configMapKV)
        # print("Create config.properties file for key-value")
        createPropertiesFile(parser_args.configfiles, _configMapKV)
        # print("Call kube_configmap to create ConfigMap")
        CreateConfigMap(parser_args)

    except ApiException as e:
        print("Exception when calling create sample configmap for quick deploy: %s\n" % e)

    print("Create ConfigMap %s for sample deploy on namespace %s success" % (parser_args.tenant+parser_args.env+parser_args.envtype+"-config.properties",parser_args.namespace))

def createPropertiesFile(filePath,keyvalues):
    content=""
    for key in keyvalues.keys():
        content=content+key+"="+keyvalues[key]+"\n"
    print(content)
    file_object = open(filePath, 'w')
    file_object.writelines(content)
    file_object.close()
    return True


# Init subparser for secret related command
_secureSubParser=globalvars.get_value('SubCMDParser')

configmapParser = _secureSubParser.add_parser('createconfmap', help='create config map based on the input enviroment parameters')
configmapParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
configmapParser.add_argument('-env', type=str, default='', help='specify the environment name, default value is qa')
configmapParser.add_argument('-envtype', type=str, default='', help='specify environment type [live | auth] for current environment, default value is auth')
configmapParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
configmapParser.add_argument('-name',type=str,help='specify config map name')
configmapParser.add_argument('-forcecreate', type=str, default='false', help='specify if need to force create a new config map record if it exist, default value is false')
configmapParser.add_argument('-configmaptype', type=str, default='fromenvfile', help='specify what config type of config map [fromenvfile|fromfile]')
configmapParser.add_argument('-configfiles', type=str, default='',help='specify config files which used for input')
configmapParser.add_argument('-rawconfig', type=str, help='specify the raw config for config map')
configmapParser.set_defaults(func=CreateConfigMap)

# Add this command just satify ICP catalog UI to quick deploy a sample environment
sampleconfParser = _secureSubParser.add_parser('createsampleconf', help='create config map for demo deploy')
sampleconfParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
sampleconfParser.add_argument('-env', type=str, default='', help='specify the environment name, default value is qa')
sampleconfParser.add_argument('-envtype', type=str, default='', help='specify environment type [live | auth] for current environment, default value is auth')
sampleconfParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
sampleconfParser.add_argument('-name',type=str,help='specify config map name')
sampleconfParser.add_argument('-forcecreate', type=str, default='false', help='specify if need to force create a new config map record if it exist, default value is false')
sampleconfParser.add_argument('-vaulttoken', type=str, help='specify if need to force create a new config map record if it exist, default value is false')
sampleconfParser.add_argument('-dbhost', type=str, help='specify target database host name')
sampleconfParser.add_argument('-dbname', type=str, help='specify target database name')
sampleconfParser.add_argument('-dbpass', type=str, help='specify target database instance user password')
sampleconfParser.add_argument('-dbport', type=str, help='specify target database port')
sampleconfParser.add_argument('-dbtype', type=str, default='db2',help='specify target database type')
sampleconfParser.add_argument('-dbuser', type=str,help='specify target database instance user name')
sampleconfParser.add_argument('-dbauser', type=str,help='optional. specify target database admin user name')
sampleconfParser.add_argument('-dbapwdencrypt', type=str,help='optional. specify target database admin user encrypted password')
sampleconfParser.add_argument('-dbpwdencrypt', type=str,help='optional. specify target database admin user encrypted password')
sampleconfParser.add_argument('-configfiles', type=str, default='/tmp/config.properties',help='specify default location for config.properties')
sampleconfParser.add_argument('-configmaptype', type=str, default='fromfile', help='specify what config type of config map')
sampleconfParser.add_argument('-rawconfig', type=str, help='specify the raw config for config map')
sampleconfParser.set_defaults(func=CreateSampleConf)

fetchconfigmapParser = _secureSubParser.add_parser('fetchconfmap', help='fetch config map based on the input enviroment parameters')
fetchconfigmapParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
fetchconfigmapParser.add_argument('-env', type=str, default='qa', help='specify the environment name, default value is qa')
fetchconfigmapParser.add_argument('-envtype', type=str, default='', help='specify environment type [live | auth] for current environment, default value is auth')
fetchconfigmapParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
fetchconfigmapParser.add_argument('-name',type=str,help='specify config map name')
fetchconfigmapParser.set_defaults(func=FetchConfigMap)

deleteconfigmapParser = _secureSubParser.add_parser('deleteconfmap', help='delete config map based on the input environment parameters')
deleteconfigmapParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
deleteconfigmapParser.add_argument('-env', type=str, default='qa', help='specify the environment name, default value is qa')
deleteconfigmapParser.add_argument('-envtype', type=str, default='', help='specify environment type [live | auth] for current environment, default value is auth')
deleteconfigmapParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
deleteconfigmapParser.add_argument('-name',type=str,help='specify config map name')
deleteconfigmapParser.set_defaults(func=DeleteConfigMap)


globalvars.set_value('SubCMDParser',_secureSubParser)

