import hvac
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("group_id")
cmd_parser.add_argument("vault_url")
cmd_parser.add_argument("vault_token")
cmd_parser.add_argument("environment_name")
args = cmd_parser.parse_args()
client = hvac.Client(url=args.vault_url, token=args.vault_token)
result = client.read("/"+args.group_id+"/"+args.environment_name+"/certs/?list=true")
list = result["data"]["keys"]
#newlist = [i.encode('raw_unicode_escape') for i in list]
print(",".join(list))


