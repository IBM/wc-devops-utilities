import hvac
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("group_id")
cmd_parser.add_argument("vault_url")
cmd_parser.add_argument("vault_token")
cmd_parser.add_argument("environment_name")
cmd_parser.add_argument("component", help="The componant you want to find")
args = cmd_parser.parse_args()

client = hvac.Client(url=args.vault_url, token=args.vault_token)
result = client.read("/"+args.group_id +"/"+args.environment_name+"/certsBundle")

if(result != None):
  print(result["data"]["value"][args.component])
else:
  print("")
