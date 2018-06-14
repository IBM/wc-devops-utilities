#!/usr/bin/env python

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

from kubernetes import client, config
import kube_vars as globalvars
import os
from os.path import dirname

def Factory_InitKubeClientTest(args):
     print(args)

def Factory_InitKubeClient(configtype=None,configfile=None,context=None,apiversion=None):

    if configtype == "InCluster" :
        config.load_incluster_config()
    elif configtype == "OutCluster":
       if configfile == None:
           configfile = dirname(os.path.realpath(__file__)) + os.sep + "kube_config.yml"
       config.load_kube_config(config_file=configfile,context=context)
    else:
       print("Input cofigtype not support!")
       exit(1)

    CoreV1Api = client.CoreV1Api()
    #Store CoreV1Api Client in global module
    globalvars.set_value('KubCoreV1Api', CoreV1Api)





