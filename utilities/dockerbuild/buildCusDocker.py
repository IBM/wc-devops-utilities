#!/usr/bin/env python3.6

import json
import argparse
import requests
import docker
import sys
import ast
import os
import datetime
import urllib.request
import zipfile
import shutil
import re
import socket
from jinja2 import Environment, FileSystemLoader
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from os.path import dirname, realpath

sys.path.append(dirname(dirname(realpath(__file__))))
from kube import kube_configmap


class DockerFileInfo:
    def __init__(self, tenant, envName, namespace, envType, dockerfileName, configType, configFile):
        self.tenant = tenant
        self.env = envName
        self.envtype = envType
        self.namespace = namespace
        if dockerfileName == "":
            self.name = "dockerfile"
        else:
            self.name = dockerfileName
        self.configtype = configType
        self.configfile = configFile


# append to path to import common library



buildDir = "/tmp/commerceBuild"
cusFolder = "CusDeploy"
build_target = ['ts-app', 'search-app', 'crs-app']


def validateUrl(url):
    validate = True
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    match = pattern.match(url)
    if match:
        print("============ The %s is a correct internet address." % (url))
    else:
        print("============ The %s is not a internet address." % (url))
        validate = False
    return validate


def validateBuldInfo(buildInfo):
    print("============buildCusDocker_CMD-->validateBuldInfo")
    return True


def generateTargetList(buildInfo):
    print("============buildCusDocker_CMD-->generateTargetList")
    target = []
    for image in buildInfo.get('images'):
        if (image['name'] in build_target) and (image['base'] != '') and (image['bundle'] != ''):
            target.append(image)
    return target


def generateBuildFolder():
    print("============buildCusDocker_CMD-->generateBuildFolder")
    if os.path.exists(buildDir):
        print("find build dir exist, delete it before start build!")
        shutil.rmtree(buildDir)

    print("create a new build dir!")
    os.makedirs(buildDir + "/" + cusFolder + "/test")
    return


def unzip(zip_file, to_dir):
    """
    Generic unzip function for extracting zip files

    @param zip_file	the zip file to be extracted
    @param to_dir	the destination directory to extract the zip file to
    """
    print("============buildCusDocker_CMD-->unzip")
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(to_dir)
        zip_ref.close()


def fetchBundleAsset(image, bundleRepo, group, isunzip=True):
    bundleValue = image.get('bundle')
    if validateUrl(bundleValue):
        bundleURL = bundleValue
        print("1============buildCusDocker_CMD-->download asset Url address: %s" % (bundleURL))
    else:
        bundleURL = bundleRepo + "/" + group + "/" + image.get('name') + "/" + image.get('bundle') + "/" + image.get(
            'name') + "-" + image.get('bundle') + ".zip"
        print("2============buildCusDocker_CMD-->download asset Url address: %s" % (bundleURL))
    print("3============buildCusDocker_CMD-->download asset Url address: %s" % (bundleURL))
    # bundleURL="http://9.110.182.156:8081/nexus/content/repositories/snapshots/com/ibm/commerce/transaction/ts/1.0-SNAPSHOT/ts-1.0-20170602.031118-1.ear"

    downloadFile = buildDir + "/" + bundleURL[bundleURL.rfind("/") + 1:]
    try:
        urllib.request.urlretrieve(bundleURL, downloadFile)
    except:
        count = 1
        while count <= 5:
            try:
                urllib.request.urlretrieve(bundleURL, downloadFile)
            except:
                err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                print(err_info)
                count += 1
        if count > 5:
            print("Downloading artifact failed!")
    if isunzip:
        unzip(downloadFile, buildDir + "/CusDeploy")


def generateDockerfile(image, dockerRepo, dockerRepoLib, group_id):
    print("============buildCusDocker_CMD-->generateDockerfile")

    templatePath = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_ENVIRONMENT = Environment(
        autoescape=False,
        loader=FileSystemLoader(os.path.join(templatePath, 'templates')),
        trim_blocks=False)

    templateVars = {
        "docker_repo_url": dockerRepo,
        "docker_repo_lib": dockerRepoLib,
        "tenant": group_id,
        "base_app": image.get('name'),
        "base_app_tag": image.get('base')
    }

    Dockerfile = TEMPLATE_ENVIRONMENT.get_template("Dockerfile").render(templateVars)

    if os.path.exists(buildDir + "/Dockerfile"):
        os.remove(buildDir + "/Dockerfile")

    DockerFile = open(buildDir + "/Dockerfile", "w")
    DockerFile.write(Dockerfile)
    DockerFile.flush()
    DockerFile.close()


def generateDockerfileNew(image, env, namespace, dockerRepo, dockerRepoLib, group_id, envType, configType, configFile):
    print("============buildCusDocker_CMD-->generateDockerfile")
    templatePath = buildDir + "/Dockerfile.template"
    dockerfileName = image.get("dockerfile")
    componentName = image.get("name")
    if dockerfileName:
        dockerfileInfo = DockerFileInfo(group_id, env, namespace, envType, dockerfileName, configType, configFile)
        dockerfileContent = kube_configmap.FetchConfigMap(dockerfileInfo)
    else:
        dockerfileName = group_id + env + "-" + componentName + "-dockerfile"
        dockerfileInfo = DockerFileInfo(group_id, env, namespace, envType, dockerfileName, configType, configFile)
        dockerfileContent = kube_configmap.FetchConfigMap(dockerfileInfo)
        if dockerfileContent == "":
            dockerfileInfo = DockerFileInfo(group_id, env, namespace, "", "", configType, configFile)
            dockerfileContent = kube_configmap.FetchConfigMap(dockerfileInfo)
            if envType:
                dockerfileInfo = DockerFileInfo(group_id, env, namespace, envType, "", configType, configFile)
                dockerfileContentSeparate = kube_configmap.FetchConfigMap(dockerfileInfo)
                if not dockerfileContentSeparate:
                    dockerfileContent = dockerfileContentSeparate
    if dockerfileContent == "":
        print("can't find the docker file for this image: %s" % (componentName))

    else:
        print("Get the docker file :%s" % (dockerfileContent))
        writeDockerFile(templatePath, dockerfileContent)

    TEMPLATE_ENVIRONMENT = Environment(
        autoescape=False,
        loader=FileSystemLoader(buildDir),
        trim_blocks=False)

    templateVars = {
        "docker_repo_url": dockerRepo,
        "docker_repo_lib": dockerRepoLib,
        "tenant": group_id,
        "base_app": image.get('name'),
        "base_app_tag": image.get('base')
    }

    Dockerfile = TEMPLATE_ENVIRONMENT.get_template("Dockerfile.template").render(templateVars)

    writeDockerFile(buildDir + "/Dockerfile", Dockerfile)


def writeDockerFile(filePath, fileContent):
    if os.path.exists(filePath):
        os.remove(filePath)

    DockerFile = open(filePath, "w")
    DockerFile.write(fileContent)
    DockerFile.flush()
    DockerFile.close()


def buildDockerImage(image, group, env, dockerRepo, dockerRepoUser, dockerRepoPwd, doPull=False, doPush=False):
    print("============buildCusDocker_CMD-->buildDockerImage")

    bundleImageTag = image.get('version')

    if env != '' or env != None:
        bundleImageTag = bundleImageTag + env

    tenant_bundle_path = dockerRepo + "/" + group + "/" + image.get('name') + "-cus"

    dClient = docker.from_env()
    dClient.login(username=dockerRepoUser, password=dockerRepoPwd, registry=dockerRepo)
    print('Build Docker Image START: {}'.format(datetime.datetime.now()))
    dClient.images.build(path=buildDir, pull=doPull, tag=tenant_bundle_path + ':' + bundleImageTag, rm=True)
    # response_build = [line for line in dClient.images.build(path=buildDir, pull=True,tag=tenant_bundle_path+':'+bundleImageTag,rm=True)]
    # sys.stdout.write(''.join([l.decode() for l in response_build]))
    print('Build Docker Image END: {}'.format(datetime.datetime.now()))

    if doPush:
        # for line in dClient.images.push(tenant_bundle_path+':'+bundleImageTag, stream=True):
        #     print(line)
        print("============buildCusDocker_CMD-->buildDockerImage->push docker image to reposiroty")
        output = os.popen(
            'docker push {tenant_bundle_path}:{bundleImageTag}'.format(tenant_bundle_path=tenant_bundle_path,
                                                                       bundleImageTag=bundleImageTag))
        print(output.read())
        print("============buildCusDocker_CMD-->buildDockerImage->remove docker image on build server ")
        #dClient.images.remove(image=tenant_bundle_path + ':' + bundleImageTag, force=True)


def main():
    buildInfo = '''
      {
     "group": "test",
     "env": "env",
     "dockerRepo": "bxv8v141.cn.ibm.com",
     "bundleRepo": "http://9.110.182.156:8081/nexus/content/repositories/releases/commerce",
     "images": [
           {
                "name":"ts-app",
                "base":"v23",
                "bundle": "1.1",
                "version": "v1"
           }
     ]
}

    '''

    parser = argparse.ArgumentParser(description='Fetch information for build custom docker image.')
    parser.add_argument('-vu', '--vaultUrl', type=str, required=True,
                        help="the vault url, example: http://<vault server>:8200/v1/secret")
    parser.add_argument('-vt', '--vaultToken', type=str, required=True, help="the tenant's vault token")
    parser.add_argument('-ru', '--dockerRepoUser', type=str, required=True, help="the docker registory user")
    parser.add_argument('-ns', '--namesapce', type=str, required=True, default="default",
                        help="specify the namespace in kubernetes for current environment, default value is default")
    parser.add_argument('-rp', '--dockerRepoPwd', type=str, required=True, help="the docker registory user pwd")
    parser.add_argument('-rl', '--dockerRepoLib', type=str, required=False, default="commerce",
                        help="specify docker registory repository library")
    parser.add_argument('-fpl', '--forcePull', type=str, required=False, default="True",
                        help="define if need to force pull base docker image")
    parser.add_argument('-fph', '--forcePush', type=str, required=False, default="True",
                        help="define if need to force push new docker image to regisery")
    parser.add_argument('-i', '--build_info', metavar='build_info', required=True, help='Image Build_info', type=str)
    parser.add_argument('-ct', '--configtype', type=str, default='InCluster', required=False,
                        help="to speficy run in cluster or not")
    parser.add_argument('-cf', '--configfile', type=str, required=False, help="to speficy kubenetes configuration file")

    args = parser.parse_args()
    vault_url = args.vaultUrl
    vault_token = args.vaultToken
    buildinfo = args.build_info
    dockerRepoUser = args.dockerRepoUser
    dockerRepoPwd = args.dockerRepoPwd
    namespace = args.namesapce
    configFile = args.configfile
    configType = args.configtype
    forcePull = False
    forcePush = False
    dockerRepoLib = args.dockerRepoLib

    if args.forcePull == "True":
        forcePull = True
    if args.forcePush == "True":
        forcePush = True

    # Initial build info as json object
    # build_InfoJson = json.loads(buildInfo)
    build_InfoJson = json.loads(buildinfo)

    print(build_InfoJson)

    # Initial commone variable for build docker image
    dockerRepo = build_InfoJson.get('dockerRepo')  # docker repository url
    bundleRepo = build_InfoJson.get('bundleRepo')  # bundle repository url
    group_id = build_InfoJson.get('group')  # current group name which will be the library name
    env = build_InfoJson.get('env')
    envType = build_InfoJson.get(
        'envType')  # if environment not empty, env will be add into tag to make the docker build as a special docker image for current environment

    # 4. verify input image info list and generate build list
    if (not validateBuldInfo(build_InfoJson)):
        print("buld info is not validate!")
        exit(1)

    # 5. find out validate target image to build
    targetImages = generateTargetList(build_InfoJson)
    if len(targetImages) == 0:
        print("can not find validate target image to build!")
        exit(0)

    print("target Image list is {targetImages}".format(targetImages=targetImages))

    for image in targetImages:

        generateBuildFolder()

        fetchBundleAsset(image, bundleRepo, group_id)

        if envType:
            generateDockerfileNew(image, env, namespace, dockerRepo, dockerRepoLib, group_id, envType, configType,
                                  configFile)
        else:
            generateDockerfileNew(image, env, namespace, dockerRepo, dockerRepoLib, group_id, "", configType,
                                  configFile)

        buildDockerImage(image, group_id, env, dockerRepo, dockerRepoUser, dockerRepoPwd, forcePull, forcePush)


if __name__ == '__main__':
    main()
