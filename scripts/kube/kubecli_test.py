import kube_vars as globalvars
import kube_factory as factory
import kube_secret
import kube_servicecheck
import kube_pvc
import kube_configmap
import kube_pod
import os

#Current file path
CURDIR = os.path.abspath(os.path.dirname(__file__)) + "/"

if __name__ == "__main__":
    # This is the unified interface to accept parameters
    # Python model argparse be used to parse the input parameter
    # Subparser has been defined in git_handler.py which including what subcmd and related parameters should be used
    # IF you want to extenstion more cmd please following this coding pattern

    parser = globalvars.get_value('RootCMDParser')
    # for quick testing input prameter can use this:
    # args = parser.parse_args(["-configtype","OutCluster","createsecret","-tenant","demo4", "-env","ky", "-envtype","auth","-replace","true","-namespace","demo4"])
    # args = parser.parse_args(["-configtype", "OutCluster", "deletesecret", "-tenant", "demo4", "-env", "ky", "-envtype", "auth","-namespace", "demo4"])
    # args = parser.parse_args(["-configtype", "OutCluster", "depcheck", "-tenant", "demo", "-env", "qa", "-envtype", "auth","-namespace","default","-component","transaction","-interval_time","5","-expect_during_time","180"])
    # args = parser.parse_args(["-configtype", "OutCluster", "listpods_by_label", "-namespace_name", "default","-field_selector","status.phase=Running"])
    # args = parser.parse_args(["-configtype", "OutCluster", "createpvc", "-tenant", "demo", "-env", "dev", "-envtype", "live","-component","search","-storage_class","glusterfs"])

    configMapData = '''FROM test:latest
RUN cat
RUN cd .test && \
    yum install test&& && \
    clean
COPY ./test .
COPY ./test /root
COPY ./test kongyi
'''
    #args = parser.parse_args(["-configtype", "OutCluster", "createconfmap", "-tenant", "demo", "-name","test-dockerfile","-namespace","demo5","-rawconfig","Dockerfile::"+configMapData])


    # testProperties = CURDIR+'test.properties'
    # with open(testProperties, 'w') as f:
    #     f.write("test1=value1\n")
    #     f.write("test2=value2\n")
    #     f.write("test3=sdfafe!@_#@!$!$#99sdf\n")
    #     f.write("test4=9.110.182.110\n")
    #
    #args = parser.parse_args(["-configtype", "OutCluster", "createconfmap", "-tenant", "demo", "-env", "qa", "-envtype", "auth","-name","helmchart-values", "-namespace", "demo", "-configmaptype", "fromfile","-configfiles","values-auth.yaml"])
    #args = parser.parse_args(["-configtype", "OutCluster", "fetchconfmap", "-tenant", "demo4", "-env", "qa", "-name",'test.properties', "-namespace", "demo4"])
    #args = parser.parse_args(["-configtype", "OutCluster", "fetchconfmap", "-tenant", "demo4", "-env", "qa", "-name",'dockerfile', "-namespace", "demo4"])
    # args = parser.parse_args()
    print(args)

    # config and group are global config used to initial gitlab object
    config, configtype, context, apiversion = None, None, None, None
    if hasattr(args, 'config'):
        config = args.config
    if hasattr(args, 'configtype'):
        configtype = args.configtype

    # based on input parameter to initial the kubernetes api object
    factory.Factory_InitKubeClient(configtype, config, context, apiversion)

    # args will based on the function which bind on command to launch that function
    args.func(args)