#!/usr/bin/env python3.6

#-----------------------------------------------------------------
# Licensed Materials - Property of IBM
#
# WebSphere Commerce
#
# (C) Copyright IBM Corp. 2017 All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with
# IBM Corp.
#-----------------------------------------------------------------

import jenkins
import os
import sys
import json
import argparse
import tempfile
from jinja2 import Environment, FileSystemLoader
#from jenkinsapi.jenkins import Jenkins
#input tenant_id to complete creation

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("tenant_id", help="The tenant_id is used to create a unique group and two Jobs")
cmd_parser.add_argument("username", help="The user used to login")
cmd_parser.add_argument("password", help="The password of user")
cmd_parser.add_argument("jenkins_server",help="The current jenkins server ip")

args = cmd_parser.parse_args()

#connecting jenkins server

server = jenkins.Jenkins(args.jenkins_server, username=args.username, password=args.password)
print("Jenkis server " + server.server + " is connected")
#print(server.version)

#Copy Jobs "PrepareEnv" and "CreateWCSCloud"
ManageConfigMapName = "ManageConfigMap_" + args.tenant_id
DeployWCSCloudName = "DeployWCSCloud_" + args.tenant_id
BuildDockerImageName = "BuildDockerImage_" + args.tenant_id
TriggerBuildIndexName = "TriggerBuildIndex_" + args.tenant_id
ManageDockerfilName = "ManageDockerfile_" + args.tenant_id
TriggerIndexReplicaName = "TriggerIndexReplica_" + args.tenant_id
BundleCertName = "BundleCert_" + args.tenant_id
AddCertName = "AddCert_" + args.tenant_id
ManageVaultConfigName = "ManageVaultConfig_" + args.tenant_id
UtilsVersionInfoName = "Utilities_VersionInfo_" + args.tenant_id
UtilsUpdateDBName = "Utilities_UpdateDB_" + args.tenant_id

server.copy_job('ManageConfigMap_Base', ManageConfigMapName)
server.copy_job('DeployWCSCloud_Base', DeployWCSCloudName)
server.copy_job('BuildDockerImage_Base', BuildDockerImageName)
server.copy_job('TriggerBuildIndex_Base', TriggerBuildIndexName)
server.copy_job('ManageDockerfile_Base', ManageDockerfilName)
server.copy_job('TriggerIndexReplica_Base', TriggerIndexReplicaName)
server.copy_job('ManageVaultConfig_Base', ManageVaultConfigName)
server.copy_job('AddCert_Base', AddCertName)
server.copy_job('BundleCert_Base', BundleCertName)
server.copy_job('Utilities_UpdateDB_Base', UtilsUpdateDBName)
server.copy_job('Utilities_VersionInfo_Base', UtilsVersionInfoName)

#Create a unique group for the tenant_id.
templateVars = {
    "ManageConfigMap" : ManageConfigMapName,
    "DeployWCSCloud" : DeployWCSCloudName,
    "BuildDockerImage": BuildDockerImageName,
    "TriggerIndex": TriggerBuildIndexName,
    "ManageDockerfile": ManageDockerfilName,
    "TriggerIndexRep": TriggerIndexReplicaName,
    "AddCert" : AddCertName,
    "BundleCert": BundleCertName,
    "ManageVaultConfig": ManageVaultConfigName,
    "UtilsUpdateDB": UtilsUpdateDBName,
    "UtilsVersinInfo": UtilsVersionInfoName,
    "name" : args.tenant_id
}
print(templateVars)
templatePaht = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape = False,
    loader = FileSystemLoader(os.path.join(templatePaht,)),
    trim_blocks = False
)
appXmlStr = TEMPLATE_ENVIRONMENT.get_template("viewTemplate.xml").render(templateVars)
print(appXmlStr)
# server.views.create(args.tenant_id, appXmlStr)

server.create_view(args.tenant_id, appXmlStr)
server.reconfig_view(args.tenant_id, appXmlStr)

