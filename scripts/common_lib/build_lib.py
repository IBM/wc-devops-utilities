#!/usr/bin/env python3.6

import os
import subprocess
import json
import argparse
import zipfile
import shutil
import requests
import datetime
import re
import operator
import unicodedata

# global list of error messages to keep track of all error msgs
errorMessages = []

"""
Collection of Common Functions used by Build Scripts

A collection of common functions shared by each individual build scripts.
"""

def get(url, usr, pwd):
    """
    HTTP/HTTPS GET requests using external Python module requests

    @param url the url of the REST call
    @param usr the functional username for the docker registry
    @param pwd the password for the docker registry functional user
    @return a JSON response
    """

    headers = {
        'Accept': 'application/vnd.docker.distribution.manifest.v1+json',
    }
    # TEMP: Remove the suppressed verification once the docker cert location
    # is figured out and we specify it in REQUESTS_CA_BUNDLE
    return requests.get(url, auth=(usr, pwd), headers=headers, verify=False)


def get_latest_tag(registry_path, usr, pwd):
    """
    Retrieve the latest version of an image based on its tags: vX-YYYYMMDD-HHmm.
    The latest, by definition, is defined to be the one with the highest version
    number (vX) and the latest timestamp (YYYYMMDD-HHmm).

    @param registry_path    docker registry path
    @param usr the functional username for the docker registry
    @param pwd the password for the docker registry functional user
    @return the latest image tag
    """

    tag_list_url = registry_path + '/tags/list'
    request = get(tag_list_url, usr, pwd)
    tag_list = json.loads(request.text)

    for tag in tag_list['tags']:
        if '-' not in tag:
            continue

        str_version, str_dash, str_timestamp = tag.partition('-')
        tag_format="%Y%m%d-%H%M"

        try:
            dt_timestamp = datetime.datetime.strptime(str_timestamp, tag_format)
        except ValueError:
            continue

        try:
            latest_version
            latest_timestamp
            latest_tag
        except NameError:
            latest_version = str_version
            latest_timestamp = dt_timestamp
            latest_tag = tag
        else:
            if latest_version > str_version:
                continue
            elif latest_version < str_version:
                latest_version = str_version
                latest_timestamp = dt_timestamp
                latest_tag = tag
            else:
                if latest_timestamp < dt_timestamp:
                    latest_timestamp = dt_timestamp
                    latest_tag = tag

    return latest_tag


def unzip(zip_file, to_dir):
    """
    Generic unzip function for extracting zip files

    @param zip_file	the zip file to be extracted
    @param to_dir	the destination directory to extract the zip file to
    """
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(to_dir)
        zip_ref.close()


def create_dockerfile(dockerfile_parent_dir, docker_url, image_namespace, image_name, image_tag_latest):
    """
    Creates a dockerfile using the correct docker registry URL associated
    with the datacenter this script is being run on

    :param str dockerfile_parent_dir: path to the parent directory for the Dockerfile
    :param str docker_url: the docker registry VIP accessible from the mesos slaves
    :param str image_namespace: the name of the image
    :param str image_name: the name of the image
    :param str image_tag_latest: the latest version tag of the base image
    :returns: None
    """
    # Form the path for the Dockerfile based on the parent of the caller script
    dockerfile_path = os.path.join(dockerfile_parent_dir, "Dockerfile")

    # Create the Dockerfile
    dockerfile = open(dockerfile_path, "w+")

    # Format the FROM command
    dockerfile_from_cmd = "FROM " + docker_url + image_namespace + "/" + image_name + ":" + image_tag_latest
    # Write the FROM command string to the Dockerfile
    dockerfile.write(dockerfile_from_cmd)

    # Close the open file instance
    dockerfile.close()

def set_docker_client_timeout():
    """
    Sets the DOCKER_CLIENT_TIMEOUT environment variable to 300
    """
    os.environ['DOCKER_CLIENT_TIMEOUT'] = '300'
    print("The timeout set for docker client: " + os.environ['DOCKER_CLIENT_TIMEOUT'] + " seconds")
    
    
# ======================= verify bundle Structure ===============================================

def openJSONfile(jsonFile):
    """
    Function to open a JSON file
    
    @param jsonFile    path to the JSON file
    
    @return the loaded JSON file
    """
    try:
        with open(jsonFile) as json_data_file:
            data = json.load(json_data_file)
    except:
        addToErrorMessages("The specified JSON file is not valid: " + jsonFile)
        raise
    return data



def directoryToJSON(directory):
    """
    Function to convert objects in a given directory into JSON form.
    The parent object is always a dict, it may contain children if type=directory. 
    A directory is composed of a list and may contain files and/or directories.
    
    @param directory    directory to convert
    
    @return JSON representation of a directory
    """
    d = {'name': os.path.basename(directory)} # the parent object is dict
    if os.path.isdir(directory):
        d['type'] = "directory" 
        
        # directory may have children
        # the children in a directory is a list composed of more files/directories
        d['children'] = [directoryToJSON(os.path.join(directory,x)) for x in os.listdir(directory)]
    else:
        d['type'] = "file" 
    return d

    
    
def verifyBundleStructure(expected, actual, currentPath):
    """
    Function to verify if an uploaded bundle follows IBM defined structure
    
    @param expected    the JSON representation of the IBM defined structure
    @param actual    the JSON representation of the actual structure of the uploaded bundle
    @param currentPath    the path currently being checked (used to build paths recursively for error msg)
    
    @return True if structure of the uploaded bundle follows IBM defined structure. False otherwise.
    """
    isMatched = True
    if type(expected) is dict:
        if matches(expected,actual): # a matching file or directory was found
            if expected['type'] == 'directory':
                currentPath = currentPath + actual['name'] + "/"
                if expected['children'] == "_any": 
                    isMatched = isMatched & True # if the contents of the directory can be anything then do no further checking
                else:
                    isMatched = isMatched & verifyBundleStructure(expected['children'], actual['children'], currentPath) # do further checking
        else: # a matching file or directory was not found
            if expected['fail-if-not-found'] == "yes":
                logBundleStructureErrorMessage(expected, currentPath)
                return False
    if type(expected) is list:
        for k in range(0,len(expected)):
            isMatched = isMatched & verifyActualContainsExpectedElement(actual, expected[k], currentPath, isMatched)
                    
    return isMatched

def logBundleStructureErrorMessage(expected, currentPath):
    """
    Function to adds error messages to the global array.
    
    @param expected   the expected element
    @param currentPath    the current path we are on that has the missing file or directory

    """
    addToErrorMessages("A "+ expected['type'] +" is missing from the path: \"" + currentPath + "\"")
    addToErrorMessages(expected['error-message-if-fails'])
    
    return

def matches(expectedElement, actualElement):
    """
    Function to check if files/directories match. They must have the same name and must both be the same type.
    
    @param expectedElement   the expected element. May be defined by regular expression
    @param actualElement    the actual element
    """
    ret = False
    
    if re.fullmatch(expectedElement['name'], actualElement['name']) is not None and expectedElement['type'] == actualElement['type']:
        ret = True
    return ret

def verifyActualContainsExpectedElement(actual, expectedElement, currentPath, isMatched):
    """
    Function to verify if an actual list of objects contains an expected element. Helper method to verifyBundleStructure.
    
    @param actual   list of the actual files and directories in the bundle
    @param expectedElement    the expected element to find in the bundle
    @param currentPath    the path currently being checked (used to build paths recursively for error msg)
    @param isMatched    (only used for recursive calls)
    
    @return True if the list of actual objects contain the expected element
    """
    # if actual is a dict then verify it and its children
    if type(actual) is dict:
        isMatched = isMatched & verifyBundleStructure(expectedElement,actual, currentPath)
        
    # if actual is a list then find out if they match anywhere, if so get the matched position
    elif type(actual) is list:
        matchedPosition = -1
        for i in range(0, len(actual)): 
            if matches(expectedElement,actual[i]):
                matchedPosition = i
                break

        if matchedPosition != -1: # if they match then verify their children too
            isMatched = isMatched & verifyBundleStructure(expectedElement, actual[matchedPosition] , currentPath)

        else : # if they don't match then log the error msg and return false
            if expectedElement['fail-if-not-found'] == "yes": # log error msg and return false if needed
                isMatched = False 
                logBundleStructureErrorMessage(expectedElement, currentPath)
    
    return isMatched

def addToErrorMessages(errorMessage):
    """
    Function to add error messages to the global list of errorMessages 

    @param errorMessage    the error message to add
    """
    print(errorMessage) 
    
    global errorMessges
    errorMessages.extend([errorMessage])
    
    return
        
def unzipRecursively(zipFileName, directoryToUnzipTo):
    """
    Function to unzip a ZIP file recursively

    @param zipFileName    the zip file to be extracted
    @param directoryToUnzipTo   the destination directory to extract the zip file to
    """
    # update
    if zipFileName.endswith(".zip"): #check if it's a .zip

        unzip(zipFileName,directoryToUnzipTo)
        os.remove(zipFileName)
        for x in os.listdir(directoryToUnzipTo):
            subdirectory = os.path.join(directoryToUnzipTo, os.path.splitext(x)[0])
            subfile = os.path.join(directoryToUnzipTo, x )
            unzipRecursively(subfile, subdirectory)
    return 

        
def zipFileIsGood(filePath):
    """
    Function to test if a ZIP file is good or bad

    @param filePath    the zip file to be tested
    
    @return True if the ZIP file is good. False otherwise.
    """
    ret = True
    
    try:
        the_zip_file = zipfile.ZipFile(filePath)
        badFile = the_zip_file.testzip()
    
        if badFile is not None:
            ret = False
        else:
            ret = True
    except:
        ret = False
    return ret


def verifyZipFile(zipDirectory, nameOfBundle):
    """
    Function to verify if an uploaded bundle is:
        1) a valid zip file
        2) follows IBM defined structure
    
    @param zipDirectory    where the bundle ZIP is located
    @param nameOfBundle    name of the bundle ZIP file
    """
    print ('Validating bundle structure...')
    
    bundleIsGood = True
    bundleZip = os.path.join(zipDirectory, nameOfBundle)

    if zipFileIsGood(bundleZip):
        try:
            # copy bundle into new working directory -----------------------------------------------------------
            directoryToUnzipTo = os.path.join(zipDirectory, "temp")
    
            if not os.path.exists(directoryToUnzipTo):
                os.makedirs(directoryToUnzipTo)
            
            shutil.copy(bundleZip, os.path.join(directoryToUnzipTo, nameOfBundle))
            
            # unzip the bundle ----------------------------------------------------------------------------------
            unzipRecursively(os.path.join(directoryToUnzipTo, nameOfBundle), os.path.join(directoryToUnzipTo, os.path.splitext(nameOfBundle)[0]))
            
            # verify structure of bundle ------------------------------------------------------------------------
            # check package stucture
            expectedPackageStructure = openJSONfile(os.path.join(zipDirectory, "bundle-definition.json"))
            actualBundleStructure = directoryToJSON(directoryToUnzipTo) # convert the unzipped directory to JSON file
            bundleIsGood = verifyBundleStructure(expectedPackageStructure, actualBundleStructure, "")
            
            if not bundleIsGood:
                addToErrorMessages("The uploaded bundle does not meet predefined structure. Could not proceed with deployment.")
                
            # clean up unzipped stuff and package structure Json -------------------------------------------------
            shutil.rmtree(directoryToUnzipTo)
        except:
            addToErrorMessages("Exception occurred while verifying bundle structure. Could not proceed with deployment.")
            bundleIsGood = False
            
    else:
        bundleIsGood = False
        addToErrorMessages("The uploaded bundle could not be unzipped. Could not proceed with deployment.")

    # out put report value , join all the messages together
    print ("report=[" + ". ".join(str(x) for x in errorMessages) + "]")
    return  bundleIsGood
