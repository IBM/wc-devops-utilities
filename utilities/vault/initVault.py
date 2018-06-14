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
This script is to initialize Vault and create namespace per tenant.

Input:
  tenant_id
  vault_url
  vault_token

Output:
  A read only token for the created new tenant
    or
  error message when exception occurred
"""

import os
import hvac
import sys
import json
import argparse
from os.path import dirname, realpath
sys.path.append(dirname(dirname(realpath(__file__))))
from common_lib import vault_reader

TEN_YEARS = '87600h'

# Read inputs to set initial tenant id, vault url and token
cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("tenant_id", help="The tenant's unique identifier")
cmd_parser.add_argument("vault_url", help="The URL used to communicate to Vault")
cmd_parser.add_argument("vault_token", help="The token used to write parameters to Vault")

args = cmd_parser.parse_args()

# Set the REQUESTS_CA_BUNDLE environment variable
vault_reader.set_requests_ca_bundle()

client = hvac.Client(url=args.vault_url,token=args.vault_token)

# Mount new backends
try:
  client.enable_secret_backend('generic',mount_point=str(args.tenant_id),config={'max_lease_ttl':TEN_YEARS})
except Exception as e:
  vault_errors = "errors=" + str(e) + ". At mounting backend during initVault."
  sys.exit(vault_errors)

# Create and set policy
a_policy = """
  path "{0}/*" {{
    policy = "read"
  }}
  path "selfserve/zooKeeperServers" {{
    policy = "read"
  }}
  path "selfserve/kafkaServers" {{
    policy = "read"
  }}
  path "selfserve_production_pki/issue/generate-cert" {{
    policy = "write"
  }}
""".format(str(args.tenant_id))
policy_name = str(args.tenant_id) + '_policy'

try:
  client.set_policy(policy_name,a_policy)
except Exception as e:
  vault_errors = "errors=" + str(e) + ". At creating policy during initVault."
  sys.exit(vault_errors)

# Create token with policy
try:
  client_token = client.create_token(policies=[policy_name], ttl=TEN_YEARS)
  print("clientReadReturnToken=" + client_token['auth']['client_token'])
except Exception as e:
  vault_errors = "errors=" + str(e) + ". At creating and parsing token during initVault."
  sys.exit(vault_errors)
