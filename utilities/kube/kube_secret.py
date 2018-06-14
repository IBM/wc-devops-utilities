import kube_vars as globalvars
import subprocess
import os
import kube_factory as factory
from kubernetes import client
from kubernetes.client.rest import ApiException

#For testing
# import argparse
# from os.path import dirname


#Bin CMD Location
OPENSSL = '/usr/bin/openssl'
BASE64 = '/usr/bin/base64'

#Current file path
CURDIR = os.path.abspath(os.path.dirname(__file__)) + "/"

#Certification Config
KEY_SIZE = '2048'
DAYS = '5000'
CA_CERT = 'tls.crt'
CA_KEY = 'tls.key'
CA_PUBLISH_KEY = 'tls_public_key.pem'


def DeleteSecret(parser_args):
    _targetCertName = parser_args.tenant + parser_args.env + parser_args.envtype + "-certificate"
    _targetPublicKeyName = parser_args.tenant + parser_args.env + parser_args.envtype + "-dhparam"

    _targetSecretList=[_targetCertName,_targetPublicKeyName]

    _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if not _CoreV1Api:
        factory.Factory_InitKubeClient(parser_args.configtype, parser_args.configfile)
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if parser_args.namespace !=None and parser_args.namespace !="":
        namespace=parser_args.namespace
    else:
        namespace='default'

    api_response = _CoreV1Api.list_namespaced_secret(namespace=namespace, pretty=True, watch=False)

    for item in api_response.items:
        if item.metadata.name in _targetSecretList:
            _deleteSecrete(item.metadata.name, _CoreV1Api, namespace)



def CheckAndCreate(parser_args):

    # Core Logic For Quick Testing
    # _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    # _createRawCerts(args)
    # _createKubeSecret(args, _CoreV1Api)

    _targetCertName=parser_args.tenant+parser_args.env+parser_args.envtype+"-certificate"
    _targetPublicKeyName=parser_args.tenant+parser_args.env+parser_args.envtype+"-dhparam"

    _targetCertExist = False
    _targetPublicKeyExist = False

    _secretCheckPass=False

    if parser_args.namespace !=None and parser_args.namespace !="":
        namespace=parser_args.namespace
    else:
        namespace='default'

    _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if not _CoreV1Api:
        factory.Factory_InitKubeClient(parser_args.configtype, parser_args.configfile)
        _CoreV1Api = globalvars.get_value('KubCoreV1Api')
    if _CoreV1Api:
     try:
        api_response = _CoreV1Api.list_namespaced_secret(namespace=namespace,pretty=True,watch=False)

        print("try to find certification %s and publickey %s" %(_targetCertName,_targetPublicKeyName))
        for item in api_response.items:
           if _targetCertExist and _targetPublicKeyExist:
              _secretCheckPass = True
              break
           if item.metadata.name == _targetCertName:
              if parser_args.replace == "true":
                _deleteSecrete(_targetCertName,_CoreV1Api,parser_args.namespace)
                continue
              _targetCertExist = True
           elif item.metadata.name == _targetPublicKeyName:
               if parser_args.replace == "true":
                   _deleteSecrete(_targetPublicKeyName,_CoreV1Api,parser_args.namespace)
                   continue
               _targetPublicKeyExist = True
           else:
               print("secret %s is no match" %(item.metadata.name))
               continue

        if not _secretCheckPass:
           print("need to create secret")
           _createRawCerts(parser_args)
           _createKubeSecret(parser_args, _CoreV1Api)
        else:
           print("secret check pass !")

     except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_secret: %s\n" % e)


def _createRawCerts(args):
    #1 tls*.crt  tls*.key tls_public_key.pem  #2.Remove Old File
    for file in ["*tls.crt", "*tls.key","*tls_public_key.pem"]:
        shellCMD('rm', '-f', CURDIR+file)

    #2.Create Certs fiels ( three files )
    gencert(args.tenant,args.env,args.envtype,args.domain)


def _createKubeSecret(args,CorV1Client=None):
    print("create Secret for current environment")

    # Create Certificate
    print("Create Certificate")
    metadata = {'name': args.tenant+args.env+args.envtype+'-certificate', 'namespace': args.namespace}
    #data=  {'tls.crt': '###BASE64 encoded crt###', 'tls.key': '###BASE64 encoded Key###'}
    tls_crt_encrypt=base64EncryptCerts(CURDIR+CA_CERT)
    print('tls_crt_encrypt is %s' %(tls_crt_encrypt))
    tls_key_encrypt=base64EncryptCerts(CURDIR+CA_KEY)
    print('tls_key_encrypt is %s' % (tls_key_encrypt))
    data = {'tls.crt': tls_crt_encrypt, 'tls.key': tls_key_encrypt}
    api_version = "v1"
    kind = 'Secret'
    body = client.V1Secret(api_version, data, kind, metadata,type='kubernetes.io/tls')
    api_response = CorV1Client.create_namespaced_secret(args.namespace, body)
    print(api_response)

    # Create Certificate Public Key
    print("Create Certificate Public Key")
    metadata = {'name': args.tenant + args.env + args.envtype + '-dhparam', 'namespace': args.namespace}
    # data=  {'tls.crt': '###BASE64 encoded crt###', 'tls.key': '###BASE64 encoded Key###'}
    publickey_encrypt = base64EncryptCerts(CURDIR + CA_PUBLISH_KEY)
    print('publickey_encrypt is %s' %(publickey_encrypt))
    data = {'tls_public_key.pem': publickey_encrypt}
    api_version = "v1"
    kind = 'Secret'
    body = client.V1Secret(api_version, data, kind, metadata, type='Opaque')
    api_response = CorV1Client.create_namespaced_secret(args.namespace, body)
    print(api_response)


def _deleteSecrete(secretName,CorV1Client=None,namespace="default"):
    print("delete Secret for current environment")
    body = client.V1DeleteOptions()  # V1DeleteOptions |
    pretty = 'pretty_example'  # str | If 'true', then the output is pretty printed. (optional)
    grace_period_seconds = 0  # int | The duration in seconds before the object should be deleted. Value must be non-negative integer. The value zero indicates delete immediately. If this value is nil, the default grace period for the specified type will be used. Defaults to a per object value if not specified. zero means delete immediately. (optional)
    orphan_dependents = True  # bool | Deprecated: please use the PropagationPolicy, this field will be deprecated in 1.7. Should the dependent objects be orphaned. If true/false, the \"orphan\" finalizer will be added to/removed from the object's finalizers list. Either this field or PropagationPolicy may be set, but not both. (optional)
    propagation_policy = 'propagation_policy_example'  # str | Whether and how garbage collection will be performed. Either this field or OrphanDependents may be set, but not both. The default policy is decided by the existing finalizer set in the metadata.finalizers and the resource-specific default policy. Acceptable values are: 'Orphan' - orphan the dependents; 'Background' - allow the garbage collector to delete the dependents in the background; 'Foreground' - a cascading policy that deletes all dependents in the foreground. (optional)

    try:
        api_response = CorV1Client.delete_namespaced_secret(secretName, namespace, body, pretty=pretty,
                                                             grace_period_seconds=grace_period_seconds,
                                                             orphan_dependents=orphan_dependents,
                                                             propagation_policy=propagation_policy)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_secret: %s\n" % e)

def shellCMD(binCmd,*args):
    cmdline = [binCmd] + list(args)
    print("cmdline is %s" % (cmdline))
    subprocess.check_call(cmdline)

def gencert(tenant,env,envtype,domain):

    common_name="*."+tenant+env+envtype+domain

    #Create Private key
    shellCMD(OPENSSL,'genrsa','-out', CURDIR+CA_KEY, KEY_SIZE)
    #Create Certification
    shellCMD(OPENSSL,'req', '-x509', '-new', '-nodes', '-key', CURDIR+CA_KEY, '-subj', '/CN='+common_name, '-days', DAYS, '-out', CURDIR+CA_CERT)
    #Create Public Key
    shellCMD(OPENSSL,'rsa', '-in', CURDIR+CA_KEY, '-pubout', '-out', CURDIR+CA_PUBLISH_KEY)

def base64EncryptCerts(file):
    _encrypteFile=os.path.dirname(file)+'/encrypte_'+os.path.basename(file)
    _encryptCMD='cat '+file+' | base64 > '+_encrypteFile
    _returnCode=subprocess.check_call(_encryptCMD, shell=True)

    if os.path.exists(_encrypteFile):
        _encryptStr = ""
        with open(_encrypteFile, 'r') as f:
            for line in f.readlines():
                _encryptStr = _encryptStr + line.strip('\n')
        return _encryptStr


# This method used to read file and remove the return character
def readCertFile(file):
    certStr = ""
    with open(file, 'r') as f:
        for line in f.readlines():
            certStr += certStr
    return certStr

# Init subparser for secret related command
_secureSubParser=globalvars.get_value('SubCMDParser')

createsecureParser = _secureSubParser.add_parser('createsecret', help='create secret object based on the input enviroment parameters')
createsecureParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
createsecureParser.add_argument('-env', type=str, default='qa', help='specify the environment name, default value is qa')
createsecureParser.add_argument('-envtype', type=str, default='auth', help='specify environment type [live | auth] for current environment, default value is auth')
createsecureParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
createsecureParser.add_argument('-domain', type=str, default='.ibm.com', help='specify the domain name which be exposed on ingress e.g .ibm.com')
createsecureParser.add_argument('-replace', type=str, default='false', help='specify if need to replace the secret record if it exist, default value is false')
createsecureParser.set_defaults(func=CheckAndCreate)

deletesecureParser = _secureSubParser.add_parser('deletesecret', help='delete secret object based on the input environment parameters')
deletesecureParser.add_argument('-tenant', type=str, default='demo', help='specify the tenant name for current environment, default value is demo')
deletesecureParser.add_argument('-env', type=str, default='qa', help='specify the environment name, default value is qa')
deletesecureParser.add_argument('-envtype', type=str, default='auth', help='specify environment type [live | auth] for current environment, default value is auth')
deletesecureParser.add_argument('-namespace', type=str, default='default', help='specify the namespace in kubernetes for current environment, default value is default')
deletesecureParser.set_defaults(func=DeleteSecret)

globalvars.set_value('SubCMDParser',_secureSubParser)


# # Below is the test case
# if __name__=="__main__":
#
#
#     _createRawCerts(args)
#
#     # configfile = dirname(os.path.realpath(__file__)) + os.sep + "kube_config.yml"
#     # config.load_kube_config(config_file=configfile)
#     #
#     # CoreV1Api = client.CoreV1Api()
#     #
#     # CoreV1Api.list_namespaced_secret(namespace=args.namespace, pretty=True, watch=False)
#     #
#     # _createKubeSecret(args, CoreV1Api)


# if __name__=="__main__":
#     print(base64EncryptCerts("tls.crt"))
#     print(base64EncryptCerts("tls.key"))
#     print(base64EncryptCerts("tls_public_key.pem"))
