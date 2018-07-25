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


import hvac
import sys
import argparse

from os.path import dirname,realpath
sys.path.append(dirname(dirname(realpath(__file__))))
from common_lib import vault_reader

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("tenant_id", help="The tenant's unique identifier")
cmd_parser.add_argument("vault_url", help="The URL used to communicate to vault")
cmd_parser.add_argument("vault_token", help="The token used to write parameters to vault")
cmd_parser.add_argument("environment_name", help="The environment name, e.g product, qa, dev, etc.")
cmd_parser.add_argument("certName", help="The cert's unique identifier")
cmd_parser.add_argument("certificate", help="The cert's certificate")
cmd_parser.add_argument("private_key", help="The private_key")
cmd_parser.add_argument("issuing_ca", help="The issuing_ca")
cmd_parser.add_argument("keystorepass", help="the keysotrepass")
cmd_parser.add_argument("destination_host", help="the destination_host")

args = cmd_parser.parse_args()

vault_reader.set_requests_ca_bundle()
base_vault_path = "{}/{}/".format(args.tenant_id, args.environment_name)

client = hvac.Client(url=args.vault_url, token=args.vault_token)

certTemp = {
        "certificate": args.certificate,
        "private_key": args.private_key,
        "issuing_ca": args.issuing_ca,
        "keystorepass": args.keystorepass,
        "destination_host": args.destination_host
    }
try:
    client.write(base_vault_path + "certs/"+args.certName, value=certTemp)
    print("Successfully saved certs info into vault")
except Exception as e:
    print(message="Failed to write info to vault.")
    vault_errors = "errors=:" + str(e)
    sys.exit(vault_errors)