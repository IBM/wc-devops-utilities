## Objective ##
This document will shows how to setup python environment to support CI/CD pipeline. Python is the backend
scripts we choose in CommerceV9 to implement detailed deploy logic.

User need to setup the Python environment by themself

Python Version 3.6
OS :  Centos 7.3


## Install Python Steps ##
1. Install Python3.6 dependence lib
yum install openssl openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel zlib zlib-devel

2. Download python3.6 packge to tmp directory and compile it

>* wge thttps://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
* tar -xzvf Python-3.6.0.tgz
* cd Python-3.6.0
* mkdir /usr/python3.6
* ./configure --prefix=/usr/python3.6
* make
* make install

3. move python3.6 to /usr/bin

rm -f /usr/bin/python
ln -s /usr/python3.6/bin/python3.6 /usr/bin/python
ln -s /usr/python3.6/bin/python3.6 /usr/bin/python3

Note:
 when you finish install python, yum need to change the dependence to new python3.6, otherwise, it can not work

## Install Python module ##
Commerce V9 reference pipeline dependence on some third-party module, so you need to install them

python -m pip install jinja2 argparse python-jenkins multi_key_dict six


## Usage  ##

 We could run this script to create a view and copy templates for this tenant as follows:
 
 #./jenkins_user_control $tenant_id $jenkins_user $jenkins_password
 

