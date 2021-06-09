from flask import Flask, render_template
from flask import jsonify, request
import requests
import csv
import sys
import os
import argparse
import subprocess
import datetime as dt
import urllib, json
import glob
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
username = config['keycloak']['username']
password = config['keycloak']['password']
data_storage = config['keycloak']['storage_url']

#def generate_key(arguments):
def generate_key():
    global keycloak

    keycloak_data = {
        'client_id': 'CLOUDFERRO_PUBLIC',
        'username': username,
        'password': password,
        'grant_type': 'password'
    }
    response = requests.post('https://auth.creodias.eu/auth/realms/DIAS/protocol/openid-connect/token', data=keycloak_data)
    resp_dict = response.json()
    keycloak = resp_dict['access_token']
    return(resp_dict['access_token'])

# def add_config_option(config, section, option, string):
#     if config.get(section, option) == 'false':
#         return string
#     else:
#         string=string+'&'+option+'='+config.get(section, option)
#         return string

class files:
    def __init__(self, name, zipper):
        self.name = name
        self.zipper = zipper

def generate_data(listString):
    # turn string back to json object
    string = json.loads(listString)

    search_base='https://finder.creodias.eu/resto/api/collections/' \
    + string[0]['collection'] \
    + '/search.json?maxRecords=' \
    + string[0]['max_records'] \
    + '&processingLevel=' \
    + string[0]['processing_level'] \
    + '&sortParam=' \
    + string[0]['sort_by'] \
    + '&sortOrder=' \
    + string[0]['sort_order'] \
    + '&status=' \
    + string[0]['status'] \
    + '&dataset=' \
    + string[0]['dataset']

    search_string=search_base
    # for section in config.sections():
    #     for par in config[section]:
    #         print(par)
    #         if ((par !='maxRecords') & (par !='collection')) :
    #             search_string=add_config_option(config, section, par, search_string)


    req=requests.get(search_string)
    ret=req.json()
    print('status code on query: %s' %req.status_code)
    files_list = []
    for x in ret['features']:
        files_list.append( (x['properties']['title'], x['properties']['services']['download']['url']) )

    for obj in files_list:
        print( obj[0], obj[1], sep =':')
        download_url = str(obj[1]) + '?token=' + keycloak
        resp = requests.get(download_url)
        name = str(obj[0]) + '.zip'
        #filename = os.path.join('downloaded_data',name)
        filename = os.path.join(data_storage, name)
        file = open(filename, 'wb')
        file.write(resp.content)
        file.close
    
    return('data downloaded')
