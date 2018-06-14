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

"""
Module to store all constants used for vault interaction

Objects:
    data dict key
    data value key
    bundle type names
    bundle type count
    bundle deployment keys
    bundle deployment count
    bundle deployment init version
"""

# the key string under which the key-value pair for a given parameter is stored
DATA_DICT_KEY = "data"

# the key associated with the value for a given paramater
DATA_VALUE_KEY = "value"

# bundle type names to be used as paths in vault
BUNDLE_TYPE_NAMES = ["store", "search", "tx", "xc"]

# number of bundle types
BUNDLE_TYPE_COUNT = len(BUNDLE_TYPE_NAMES)

# the keys to store the bundle deployment versions where "one" is for latest
BUNDLE_DEPLOYMENT_KEYS = ["one", "two", "three"]

# number of deployment versions being tracked
BUNDLE_DEPLOYMENT_COUNT = len(BUNDLE_DEPLOYMENT_KEYS)

# initialization value of the tenant bundle deployment version
BUNDLE_DEPLOYMENT_INIT_VERSION = "none"
