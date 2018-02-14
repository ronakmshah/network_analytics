#!/usr/bin/env python

import copy
from elasticsearch import Elasticsearch, helpers
import random
import time
import uuid
import yaml

CONFIG_DICT = {}
VPORTS = []


def populateVPorts():
    vport_prop = {}
    for i in range(CONFIG_DICT["no_of_vports_per_pgs"]):
        vport_prop['name'] = "VPort-" + str(i+1)
        vport_prop['uuid'] = str(uuid.uuid4())
        VPORTS.append(vport_prop)
        vport_prop = {}

def generateVPortStats():
    for i in range(len(VPORTS)):
        es_data = {}
        #service_item = L4_SG[i%len(L4_SG)]
        # Always write it in specific index in specific doc_type
        es_data['_index'] = "nuage_vport"
        es_data['_type'] = "nuage_doc_type"
        es_data['vport-uuid'] = VPORTS[i]['uuid']
        es_data['vport-name'] = VPORTS[i]['name']
        print ("Writing vport information for " + VPORTS[i]['name'])
        writeToES(es_data)

def writeToES(es_data):
    es = Elasticsearch(CONFIG_DICT['elastic_host'])
    write_data = []
    # Create counters on the fly everytime
    # Write data for a day every minute
    # Start with 48 hours a go
    startTime = int(time.time()) * 1000 - (24 * 60 * 60 * 1000)
    for i in range(1440):
        if (i == 720 and es_data['vport-name'] == "VPort-5"):
            es_data['bytes'] = random.randint(1000000, 2000000)
            es_data['packets'] = random.randint(500000, 1000000)
        else:
            es_data['bytes'] = random.randint(10000, 20000)
            es_data['packets'] = random.randint(500, 1000)
        es_data['timestamp'] = startTime + (i * 60000)
        write_data.append(copy.deepcopy(es_data))
        #es1.index(index="flowindex", doc_type="flow", body=es_data)
    helpers.bulk(es, iter(write_data), request_timeout=50)

def populateData():
    populateVPorts()

def configRead():
    global CONFIG_DICT
    with open("insight.yml", "r") as fileread:
        try:
            CONFIG_DICT = yaml.load(fileread)
        except yaml.YAMLError as exc:
            print(exc)

if __name__ == "__main__":
    configRead()
    populateData()
    generateVPortStats()
        
