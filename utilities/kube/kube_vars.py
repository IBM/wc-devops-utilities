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

import argparse

def _init():
    global _global_dict
    _global_dict = {}

def set_value(name, value):
    _global_dict[name] = value

def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue

_init()

Parser = argparse.ArgumentParser(add_help=True)

#This is the global parameter on the root command to specify the customized configure type [InCluster|OutCluster]
Parser.add_argument('-configtype', type=str,default='InCluster')
#This is the global parameter on the root command to specify the customized configure files path
Parser.add_argument('-config', type=str)
#This is the global parameter on the root command to specify kube config context
Parser.add_argument('-context', type=str)
#This is the global parameter on the root command to specify the api version
Parser.add_argument('-apiversion', type=str)
#This is the global parameter on the root command to specify the api version


Subparsers = Parser.add_subparsers(help='Sub Commands')

set_value("RootCMDParser", Parser)
set_value("SubCMDParser", Subparsers)