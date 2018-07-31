from kubernetes import client, config
import argparse
import sys

def NS_list(parser_args):
    if (parser_args.mode == "inCluster") :
        config.load_incluster_config()
    elif (parser_args.mode == "outCluster"):
        config.load_kube_config()
    else:
        print("error mode configuration")
        sys.exit(1)
    v1 = client.CoreV1Api()

    namespace_list = v1.list_namespace()
    for i in namespace_list.items:
        print(i.metadata.name + ",")

Parser = argparse.ArgumentParser(add_help=True)
SubParsers = Parser.add_subparsers(help='Sub Commands')
NS_Parser = SubParsers.add_parser('namespace', help='this command used to list all namespaces')
NS_Parser.add_argument('-mode',type=str,default='outCluster',help='choose inCluster or outCluster')
NS_Parser.set_defaults(func=NS_list)