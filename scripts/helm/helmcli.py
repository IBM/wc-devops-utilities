import datetime
import subprocess
import os
import argparse
import threading

DeploymentFlag="==> v1beta1/Deployment\n"
# DeploymentColume=['NAME','DESIRED','CURRENT','UP-TO-DATE','AVAILABLE','AGE']
# SecretFlag="==> v1/Secret\n"
# SecretColume=[]
# IngressFlag="==> v1beta1/Ingress\n"
# IngressColume=[]
# ServiceFlag="==> v1/Service\n"
# ServiceColume=['NAME','CLUSTER-IP','EXTERNAL-IP','PORT(S)','AGE']

class Deployment:
    def __init__(self, args):
        self.name = args[0]
        self.desired = args[1]
        self.current = args[2]
        self.uptodate = args[3]
        self.avaliable = args[4]
        self.age = args[5]
        self.done = False

    def UpdateStatus(self,args):
        self.name = args[0]
        self.desired = args[1]
        self.current = args[2]
        self.uptodate = args[3]
        self.avaliable = args[4]
        self.age = args[5]
        self.SuccessCheck()

    def SuccessCheck(self):
        if self.desired == self.avaliable:
                self.done = True

class DeploymentCollect:
    def __init__(self):
        self.deployments={}
        self.deploystatus=False

    def AddDeployment(self,deployment):
        self.deployments[deployment.name]=deployment

    def CheckDeployentsStatus(self):
        _ongoing=False

        for keyname in self.deployments.keys():

            if not self.deployments[keyname].done:
                _ongoing=True
                break
        if not _ongoing:
            self.deploystatus=True
            return True
        return False

    def GetDeployment(self,recordName):
        if recordName in self.deployments:
            return self.deployments[recordName]
        else:
            return None

    def DisplayRecode(self):
        print("name desired current uptodate avaliable age done?")
        for keyname in self.deployments.keys():
            print("%s %s %s %s %s %s %r" % (self.deployments[keyname].name, self.deployments[keyname].desired, self.deployments[keyname].current,self.deployments[keyname].uptodate,self.deployments[keyname].avaliable,self.deployments[keyname].age,self.deployments[keyname].done))


def execHelmWithOutput(cmd,*args):
    _cmdline="helm "+cmd+" "+" ".join(args)
    print("run command: %s" % _cmdline)
    return os.popen(_cmdline).readlines()

def execHelmWithStateCode(cmd,*args):
    _cmdline = "helm " + cmd +" "+ " ".join(args)
    statecode = os.system(_cmdline)
    return statecode

# Helm list
def helmList(parser_args):

    #Considering if helm enabled tls, we must add additional tls parameter for helm client command
    if parser_args.tls == "true":
        _output = execHelmWithOutput("list",parser_args.releasename,"--tls")
    else:
        _output = execHelmWithOutput("list", parser_args.releasename)
    if len(_output) == 0:
        print("Not Found Existed Release %s" % parser_args.releasename)
    else:
        if parser_args.forcecreate=="true":
           print("Force Delete Exist Release %s" % parser_args.releasename)
           helmDelete(parser_args,False)
        else:
           print("Error: Found Release %s Exist !" % parser_args.releasename)
           exit(1)

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

# Helm status
def HelmStatus(parser_args):
    #check deployment status
    if parser_args.tls == "true":
        _output=execHelmWithOutput("status",parser_args.releasename,"--tls")
    else:
        _output = execHelmWithOutput("status", parser_args.releasename)
    #print(_output)
    _parsedOutPut=parseHelmOutPut(DeploymentFlag, _output)

    _deploymentCollects = DeploymentCollect()

    for deployment_record in _parsedOutPut:
        _deployment = Deployment(deployment_record)
        _deploymentCollects.AddDeployment(_deployment)
    start_time = datetime.datetime.now()

    timer = threading.Timer(int(args.interval),helmStatus,(parser_args,_deploymentCollects,start_time))
    timer.start()

def helmStatus(parser_args,deploycollects,starttime):
    timeAccount(starttime, int(parser_args.timeout), int(parser_args.interval))

    if deploycollects.CheckDeployentsStatus():
        print("Helm Deploy Success!")
        exit(0)

    deploycollects.DisplayRecode()

    if parser_args.tls == "true":
        _output = execHelmWithOutput("status", parser_args.releasename,"--tls")
    else:
        _output = execHelmWithOutput("status", parser_args.releasename)
    _parsedOutPut = parseHelmOutPut(DeploymentFlag, _output)
    for deployment_record in _parsedOutPut:
        _deployment=deploycollects.GetDeployment(deployment_record[0])
        if _deployment !=None:
            _deployment.UpdateStatus(deployment_record)

    deploycollects.CheckDeployentsStatus()

    timer = threading.Timer(int(args.interval),helmStatus, (parser_args, deploycollects, starttime))
    timer.start()

def parseHelmOutPut(objectFlag,content):
    #parse helm cmd output
    _startIndex=content.index(objectFlag)
    i = _startIndex + 2
    recordArray=[]
    while i < len(content):
        if content[i] != "\n":
           _reocrd=content[i].strip().split()
           recordArray.append(_reocrd)
        else:
            break
        i = i + 1
    return recordArray

# Helm install
def HelmInstall(parser_args):
    helmList(parser_args)

    #Considering is enabled the tls for helm client
    if parser_args.tls == "true":
        enableTLS="--tls"
    else:
        enableTLS=""

    stateCode=execHelmWithStateCode('install', '--name', parser_args.releasename, parser_args.helmchart, '--values', parser_args.valuefile, '--namespace', parser_args.namespace, enableTLS)
    if stateCode == 0:
        HelmStatus(parser_args)
    else:
       print("Helm Install Failed")
       exit(1)
    exit(0)

# Helm update
def HelmUpgrade(parser_args):
    # Considering is enabled the tls for helm client
    if parser_args.tls == "true":
        enableTLS = "--tls"
    else:
        enableTLS = ""

    if parser_args.reusevalues=="true":
       stateCode = execHelmWithStateCode('upgrade', parser_args.releasename, parser_args.helmchart, '--values',parser_args.valuefile,'--reuse-values', enableTLS)
    else:
        stateCode = execHelmWithStateCode('upgrade', parser_args.releasename, parser_args.helmchart, '-f',parser_args.valuefile, enableTLS)

    if stateCode == 0:
        HelmStatus(parser_args)
    else:
        exit(1)


# helm delete
def HelmDelete(parser_args):
    # Considering is enabled the tls for helm client
    if parser_args.tls == "true":
        enableTLS = "--tls"
    else:
        enableTLS = ""

    stateCode = execHelmWithStateCode("delete", "--purge", parser_args.releasename,enableTLS)
    if stateCode == 0:
        print("Delete Release %s Success" % parser_args.releasename)
        exit(0)
    else:
        print("Delete Release %s Failed" % parser_args.releasename)
        exit(1)

# This method used for internal
def helmDelete(parser_args,Exit=True):
    # Considering is enabled the tls for helm client
    if parser_args.tls == "true":
        enableTLS = "--tls"
    else:
        enableTLS = ""

    stateCode = execHelmWithStateCode("delete", "--purge", parser_args.releasename,enableTLS)
    if stateCode == 0:
        print("Delete Release %s Success" % parser_args.releasename)
        if Exit:
          exit(0)
    else:
        print("Delete Release %s Failed" % parser_args.releasename)
        exit(1)


# This method use for invoke by other module
def HelmCli(*args):
    args = Parser.parse_args(args)
    args.func(args)

Parser = argparse.ArgumentParser(add_help=True)
Subparsers = Parser.add_subparsers(help='Sub Commands')
HelmInstallParser = Subparsers.add_parser('helminstall', help='helm install')
HelmInstallParser.add_argument('-releasename', type=str, default='demo', help="specify release name, suggest with this <tenant><env>")
HelmInstallParser.add_argument('-helmchart', type=str, default='', help="specify helm chart which used to do deploy")
HelmInstallParser.add_argument('-valuefile', type=str, default='', help="specify valuefile location")
HelmInstallParser.add_argument('-namespace', type=str, default='default', help="specify target namespace this release will deploy on")
HelmInstallParser.add_argument('-timeout', type=str, default='600', help="specify time out value for helm command execute")
HelmInstallParser.add_argument('-interval', type=str, default='10', help="specify interval time for check status")
HelmInstallParser.add_argument('-forcecreate', type=str, default='false', help="specify force install if there have release exist, should delete it first")
HelmInstallParser.add_argument('-tls', type=str, default='false', help="specify if helm client enabled tls")
HelmInstallParser.set_defaults(func=HelmInstall)

# HelmStatusParser = Parser.add_parser('helmstatus', help='helm status')
# HelmStatusParser.set_defaults(func=HelmStatus)

HelmUpgradeParser = Subparsers.add_parser('helmupgrade', help='helm upgrade')
HelmUpgradeParser.add_argument('-releasename', type=str, default='demo', help="specify release name, suggest with this <tenant><env>")
HelmUpgradeParser.add_argument('-helmchart', type=str, default='', help="specify helm chart which used to do deploy")
HelmUpgradeParser.add_argument('-valuefile', type=str, default='', help="specify valuefile location")
HelmUpgradeParser.add_argument('-reusevalues', type=str, default='true', help="specify if reuse latest release values")
HelmUpgradeParser.add_argument('-timeout', type=str, default='600', help="specify time out value for helm command execute")
HelmUpgradeParser.add_argument('-interval', type=str, default='10', help="specify interval time for check status")
HelmUpgradeParser.add_argument('-tls', type=str, default='false', help="specify if helm client enabled tls")
HelmUpgradeParser.set_defaults(func=HelmUpgrade)

HelmDeleteParser = Subparsers.add_parser('helmdelete', help='helm upgrade')
HelmDeleteParser.add_argument('-releasename', type=str, default='demo', help="specify release name, suggest with this <tenant><env>")
HelmDeleteParser.add_argument('-tls', type=str, default='false', help="specify if helm client enabled tls")
HelmDeleteParser.set_defaults(func=HelmDelete)


if __name__=="__main__":
  args = Parser.parse_args()
  args.func(args)