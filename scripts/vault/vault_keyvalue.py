import os
import hvac
import sys
import json
import argparse
from os.path import dirname, realpath
sys.path.append(dirname(dirname(realpath(__file__))))
from common_lib import vault_reader

# This modul used to handle action on the key-value through Vault
# Vault is a third-party tool which can used to encrypt value to make the data security.
# For support vault key-value action, we need to provide command to insert key-value , delete key-value , update key-value.

def InsertKV(parser_args):
  print("Insert Key-Value")
  # Set the REQUESTS_CA_BUNDLE environment variable
  vault_reader.set_requests_ca_bundle()
  base_vault_path = "{}/{}/".format(parser_args.tenant, parser_args.env)
  # Set Vault connection
  client = hvac.Client(url=args.vault_url, token=args.vault_token)
  exist_keys=[]

  # Get Exist Keys
  keyvalues=listKeyPaths(client,base_vault_path)
  if keyvalues != None:
    keyvalues=keyvalues.replace(("{}/{}/".format(parser_args.tenant, parser_args.env)),"")
    keyvalueList=keyvalues.split()
    for kv in keyvalueList:
      if kv!='':
          splitindex=kv.index("=") 
          k=kv[:splitindex]
          exist_keys.append(k)
      #print(list_keys)

  # Insert Key-Value into Vault KV
  try:
    if parser_args.keyvalues != None or parser_args.keyvalues != '':
          newInsertKeys=[]
          _kvpairs= parser_args.keyvalues.split(parser_args.separater)
          print(_kvpairs)
          for kv in _kvpairs:
              if kv.strip() != '':
                  _splitindex=kv.index("=")
                  key = kv[:_splitindex]
                  newInsertKeys.append(key)
                  value = kv[_splitindex+1:]
                  client.write(base_vault_path+key, value=value)
                  print("insert key: {key} with value: {value}".format(key=key, value=value))
          for key in exist_keys:
              if key not in newInsertKeys:
                  client.delete(base_vault_path+key)
    else:
        print("Target key-value is empty!")
  except Exception as e:
    print("message=Failed to write key-value pairs info to vault.")
    vault_errors = "errors=:" + str(e)
    sys.exit(vault_errors)

def FetchKV(parser_args):
   # print("Fetch Key-Value pairs from Vault")
   # Set the REQUESTS_CA_BUNDLE environment variable
   vault_reader.set_requests_ca_bundle()
   # Set basic path
   base_vault_path = "{}/{}/".format(parser_args.tenant, parser_args.env)

   # Set Vault connection
   client = hvac.Client(url=parser_args.vault_url, token=parser_args.vault_token)

   result=listKeyPaths(client,base_vault_path+parser_args.rootpath)
   if result != None:
       print(result.replace(("{}/{}/".format(parser_args.tenant, parser_args.env)), "").strip())
   else:
       print("None")


def listKeyPaths(client,path):
    key_path_dict = client.list(path)
    result=""
    #print(key_path_dict)
    if key_path_dict != None:
        if key_path_dict['data']['keys'] != None:
           for _path in key_path_dict['data']['keys']:
               if _path.endswith("/"):
                   _result=listKeyPaths(client, path+_path)
                   result=result+_result
               else:
                   # hiden any certs related record in vault
                   if not "certs" in path+_path:
                     value = readValue(client, path+_path)
                     if value != None:
                       #print(value)
                       result = result + path+_path + "=" + value + "\n"
           return result

def readValue(client,path):
     value = client.read(path)
     #print(value)
     if value != None and value["data"]["value"] !=None:
         if isinstance(value,str):
           return value["data"]["value"]
         else:
           return str(value["data"]["value"])
     return None


Parser = argparse.ArgumentParser(add_help=True)
Subparsers = Parser.add_subparsers(help='Sub Commands')
InsertKVParser = Subparsers.add_parser('insertkv', help='This command used to insert key value on target backend')
InsertKVParser.add_argument('-tenant', type=str, default='', help="specify target tenant name, each tenant represent a security backend")
InsertKVParser.add_argument('-env', type=str, default='', help="specify target environment which those key-value belongs to ")
InsertKVParser.add_argument('-separater', type=str, default='\n', help="specify separator for the kv pairs")
InsertKVParser.add_argument('-keyvalues', type=str, default='', help="target kv pair which will insert to Vault KV")
InsertKVParser.add_argument('-vault_url', type=str, default='', help="specify target vault url")
InsertKVParser.add_argument('-vault_token', type=str, default='', help="target kv pair which will insert to Vault KV")
InsertKVParser.set_defaults(func=InsertKV)

FetchKVParser = Subparsers.add_parser('fetchkv', help='This command used to fetch key value on target backend')
FetchKVParser.add_argument('-tenant', type=str, default='', help="specify target tenant name, each tenant represent a security backend")
FetchKVParser.add_argument('-env', type=str, default='', help="specify target environment which those key-value belongs to ")
FetchKVParser.add_argument('-rootpath', type=str, default='', help="specify target enviornment type [auth | live]")
FetchKVParser.add_argument('-vault_url', type=str, default='', help="specify target vault url")
FetchKVParser.add_argument('-vault_token', type=str, default='', help="target kv pair which will insert to Vault KV")
FetchKVParser.set_defaults(func=FetchKV)

# Testing Case
# keyvalues='''
# demo4/qa/test/dbHost=9.111.221.230
# demo4/qa/test/dbName=mall
# demo4/qa/test/dbPassword=wcs1
# demo4/qa/test/dbPort=50000
# demo4/qa/test/dbUser=wcs
# demo4/qa/test/dict={'certificate': 'asdfad', 'destination_host': 'adsfdasfadsf', 'issuing_ca': 'adsfads', 'keystorepass': 'asdfasdfasd', 'private_key': 'adfasd'}
# '''
#args = Parser.parse_args(["insertkv", "-vault_url", "http://9.112.245.194:30552/v1", "-vault_token", "5b895739-ad95-87d4-9f5a-92bfff799cd0", "-tenant", "demo4", "-env",'qa','-keyvalues',keyvalues,'-separater','\n'])
#args = Parser.parse_args(["fetchkv", "-vault_url", "http://9.112.245.194:30552/v1", "-vault_token", "5b895739-ad95-87d4-9f5a-92bfff799cd0", "-tenant", "demo4", "-env",'qa'])
#args.func(args)

if __name__=="__main__":
  args = Parser.parse_args()
  args.func(args)




