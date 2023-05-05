#!/usr/bin/env python3
import os
import requests
from requests.auth import HTTPBasicAuth

def check_file_exists(url, username=None, password=None):
    
    response = requests.request("PROPFIND", url, auth=(username, password))
    print(f"checking: {url} for existence")
    return response.status_code == 200

def initialization(user="", password="", nextcloudAdress="",folder=""):
    
    if user =="":
        user = input("User: ")
    if password =="":
        password = input("password: ")
    if nextcloudAdress =="":
        nextcloudAdress = input("nextcloud address: ")
    if folder =="":
        folder = input("subfolder: ")
    
    returnItems = {}
    returnItems["user"] = user
    returnItems["password"] = password
    returnItems["nextcloudAddress"] = nextcloudAdress
    returnItems["subfolder"] = folder
    return returnItems



def processing(config):
    dir = os.listdir()
    #check if subfolder exists
    urlFolder=f'https://{config["nextcloudAddress"]}/remote.php/dav/files/{config["user"]}/{config["subfolder"]}/'
    if check_file_exists(urlFolder) == False:
        print(f"Creating subfolder {config['subfolder']}")
        r = requests.request("MKCOL",urlFolder, auth = HTTPBasicAuth(config["user"], config["password"]))
        if r.status_code != 201:
            print(f"error creating subfolder {urlFolder}")
            print(f"error message: {r}")
        
    for i in dir:
        url = f'https://{config["nextcloudAddress"]}/remote.php/dav/files/{config["user"]}/{config["subfolder"]}/{i}'
        if check_file_exists(url, config["user"], config["password"]) == False:
            if os.path.isfile(i):
                file=open(i, 'rb')
                r = requests.put(url, data=file ,auth = HTTPBasicAuth(config["user"], config["password"]))
                if r.status_code != 201:
                    print(f"error uploading file: {i} to {url}")
                    print(f"error message: {r}")
            else:
                #create subfolder structure
                r = requests.request("MKCOL",url, auth = HTTPBasicAuth(config["user"], config["password"]))
                
                lastDirectory=os.getcwd()
                newDirectory = f"{lastDirectory}/{i}"
                os.chdir(newDirectory)
            
                newConfig = config.copy()
                newConfig["subfolder"] = f'{config["subfolder"]}/{i}/'
                
                processing(newConfig)
                
                os.chdir(lastDirectory)
#       result = os.system(f"curl -g -u {user}:{password} -T '{i}' https://{nextcloudAdress}/remote.php/dav/files/{user}/{folder}/")


config = initialization()
print(config)
processing(config)
