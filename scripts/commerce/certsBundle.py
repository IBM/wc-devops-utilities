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
cmd_parser.add_argument("SelectedCerts")
cmd_parser.add_argument("component")

args = cmd_parser.parse_args()

vault_reader.set_requests_ca_bundle()
base_vault_path = "{}/{}/".format(args.tenant_id, args.environment_name)

client = hvac.Client(url=args.vault_url, token=args.vault_token)

res = client.read(base_vault_path + "certsBundle")
if(res == None):
    current = {
        "tsapp":"",
        "crsapp":"",
        "xcapp":"",
        "storeapp":"",
        "tsweb":""
    }
else:
    current = res["data"]["value"]
print(current)
current[args.component]=args.SelectedCerts
print(current)
#certsTemp = ''.join(current.split())
try:
    client.write(base_vault_path + "certsBundle", value=current)
    print("Successfully saved certs bundle info into vault")
except Exception as e:
    print(message="Failed to write info to vault.")
    vault_errors = "errors=:" + str(e)
    sys.exit(vault_errors)