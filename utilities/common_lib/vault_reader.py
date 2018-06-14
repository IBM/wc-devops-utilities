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

"""
Fetches information from the Vault mounts, using the hvac API client
"""

import os
import sys
import hvac

def set_requests_ca_bundle():
    """
    Sets the REQUESTS_CA_BUNDLE environment variable to allow the
    requests module to use the correct certs for SSL communication
    """
    os.environ['REQUESTS_CA_BUNDLE'] = '/etc/pki/tls/certs/ca-bundle.crt'
    #print("The cert used for SSL communication with Vault is: " + os.environ['REQUESTS_CA_BUNDLE'])


def connect_to_vault(vault_url, vault_token):
    """
    Returns an hvac client to communicate with Vault

    :param str vault_url: the vault server url
    :param str vault_token: the vault token
    """
    client = hvac.Client(url=vault_url, token=vault_token)
    return client


def get_information(vault_client, key_path, key):
    """
    Reads the value of a key in Vault given its absolute path

    :param hvac.Client() vault_client: vault api client
    :param str key_path: full vault key path
    :param str key: the information key
    :returns: a string with the value associated with the specified key
    """
    try:
        # read and store the dictionary of items in the specified path
        key_path_dict = vault_client.read(key_path)

        # check if 'data' exists in the read json response
        if 'data' in key_path_dict.keys():
            key_data_pair = key_path_dict['data']
        else:
            # exit unsuccessfully
            sys.exit(f"Error: Data for '{key}' was not found in Vault")

        # check if the 'value' key exists in the key_data_pair dictionary
        if 'value' in key_data_pair.keys():
            # return the value associated with the param key
            return key_data_pair['value']
        else:
            # exit unsuccessfully
            sys.exit(f"Error: The value associated with '{key}' was not found in Vault")

    # catch exceptions thrown when reading from Vault
    except Exception as e:
        #print error message and exit unsuccessfully
        print(f"Failed to read or find the param '{key}' from Vault")
        sys.exit("Error: " + str(e))


def get_tenant_information(vault_client, tenant_id, key):
    """
    Gets information from the tenant mount in Vault

    :param hvac.Client() vault_client: vault api client
    :param str tenant_id: the tenant id
    :param str key: the information key
    :returns: a string with the value associated with the specified key
    """
    key_path = f"{tenant_id}/{key}"
    return get_information(vault_client, key_path, key)


def get_tenant_env_information(vault_client, tenant_id, env_name, key):
    """
    Gets information from the tenant environment path in Vault

    :param hvac.Client() vault_client: vault api client
    :param str tenant_id: the tenant id
    :param str env_name: the tenant environment name: [production|nonproduction<id>]
    :param str key: the information key
    :returns: a string with the value associated with the specified key
    """
    key_path = f"{tenant_id}/{env_name}/{key}"
    return get_information(vault_client, key_path, key)


def get_tenant_env_type_information(vault_client, tenant_id, env_name, env_type, key):
    """
    Gets information from the tenant environment path in Vault

    :param hvac.Client() vault_client: vault api client
    :param str tenant_id: the tenant id
    :param str env_name: the tenant environment name: [production|nonproduction<id>]
    :param str env_type: the tenant environment type: [live|auth]
    :param str key: the information key
    :returns: a string with the value associated with the specified key
    """
    key_path = f"{tenant_id}/{env_name}/{env_type}/{key}"
    return get_information(vault_client, key_path, key)


def get_selfserve_information(vault_client, key):
    """
    Gets information from the selfserve mount in Vault

    :param hvac.Client() vault_client: vault api client
    :param str key: the information key
    :returns: a string with the value associated with the specified key
    """
    key_path = f"selfserve/{key}"
    return get_information(vault_client, key_path, key)


def get_mount_information(vault_client, mount_name, key):
    """
    Gets information from the tenant mount in Vault

    :param hvac.Client() vault_client: vault api client
    :param str mount_name: vault mount to read from
    :param str key: the information key
    :returns: a string with the value associated with the specified key
    """
    key_path = f"{mount_name}/{key}"
    return get_information(vault_client, key_path, key)


def list_mount_keys(vault_client, mount_path):
    """
    Lists all the keys available under a mount path in Vault

    :param hvac.Client() vault_client: vault api client
    :param str mount_path: full vault mount path
    :returns: a list of keys under a vault mount
    """
    try:
        # read and store the dictionary of items in the specified path
        response_dict = vault_client.list(mount_path)

        # check if 'data' exists in the json response
        if 'data' in response_dict.keys():
            keys_dict = response_dict['data']
        else:
            # exit unsuccessfully
            sys.exit(f"Error: Data for '{mount_path}' was not found in Vault")

        # check if the 'keys' key exists in the keys_dict dictionary
        if 'keys' in keys_dict.keys():
            # return the list of data keys available under the vault mount path
            return keys_dict['keys']
        else:
            # exit unsuccessfully
            sys.exit(f"Error: No information keys were found under '{mount_path}' in Vault")

    # catch exceptions thrown when reading from Vault
    except Exception as e:
        #print error message and exit unsuccessfully
        print(f"Failed to read from or find the mount path '{mount_path}' in Vault")
        sys.exit("Error: " + str(e))
