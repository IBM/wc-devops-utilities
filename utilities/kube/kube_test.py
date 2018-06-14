import kube_vars as globalvars
import kube_factory as factory
import kube_secret
import kube_servicecheck
import kube_pvc

if __name__=="__main__":
    # This is the unified interface to accept parameters
    # Python model argparse be used to parse the input parameter
    # Subparser has been defined in git_handler.py which including what subcmd and related parameters should be used
    # IF you want to extenstion more cmd please following this coding pattern

    parser=globalvars.get_value('RootCMDParser')
    args = parser.parse_args(["-configtype","OutCluster","createsecret","-tenant","demo", "-env","dev", "-envtype","live","-replace","true"])
    print(args)


    # config and group are global config used to initial gitlab object
    config,configtype,context,apiversion = None, None, None , None
    if hasattr(args, 'config'):
        config=args.config
    if hasattr(args, 'configtype'):
        configtype=args.configtype

    factory.Factory_InitKubeClient(configtype,config,context,apiversion)

    args.func(args)