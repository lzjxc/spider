import json
import os
import random
import telnetlib

import datetime
import threading

import pymongo
import requests
from pymongo.errors import DuplicateKeyError
import sys

sys.path.append(os.getcwd())
from sina.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME


class IpService:

    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.ips_collection = client[DB_NAME]['ips']

    def addNewIp(self):
        resp = requests.get(
            'http://webapi.http.zhimacangku.com/getip?num=10&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=1&lb=1&sb=0&pb=4&mr=1&regions=')
        print(resp.status_code)
        for i in json.loads(resp.text)['data']:
            print(i)
            try:
                self.ips_collection.insert(
                    {"_id": i["ip"], "port": i["port"], "status": "success", "available":0, "expire_time":i["expire_time"]})
            except DuplicateKeyError as e:
                self.ips_collection.find_one_and_update({'_id': i["ip"]}, {'$set': {'port': i["port"], "status": "success", "available":0, "expire_time": i["expire_time"]}})


    def deleteIp(self, ip):
        try:
            self.ips_collection.find_one_and_update({'_id': ip}, {'$set': {'available': -1, "status": "success"}})
            print("delete success")
        except Exception as e:
            print(e)

    def verifyIp(self, ip, port):
        try:
            tn = telnetlib.Telnet(ip, port=port, timeout=3)
        except:
            print(ip + ' is dead,' + "deleting it from database")
        else:
            print('success')

    def selectIp(self):
        all_count = self.ips_collection.find({'available': -1}).count()
        random_index = random.randint(0, all_count - 1)
        random_ip = self.ips_collection.find({'available': -1})[random_index]
        try:
            self.verifyIp(random_ip['_id'], random_ip['port'])
            print(random_ip)
            self.ips_collection.find_one_and_update({'_id': random_ip["ip"]}, {
                '$set': {'port': random_ip["port"], "status": "success", "available": 0,"edit_time": datetime.datetime.now(), "expire_time": random_ip["expire_time"]}})

        except:
            print(random_ip["_id"] + 'is dead,' + "deleting it from database")

client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
ips_collection = client[DB_NAME]['ips']

def verifyIp(ip, port):
    try:
        tn = telnetlib.Telnet(ip, port=port, timeout=3)
    except:
        print(ip + ' is dead,' + "deleting it from database")
    else:
        print('success')
        ips_collection.find_one_and_update({'_id': ip}, {
            '$set': {'port': port, "status": "success", "available": 0,
                     "edit_time": datetime.datetime.now()}})
        print("updating")

def renewIps():
    timer = threading.Timer(5, renewIps)
    timer.start()
    all_count = ips_collection.find({'available': -1}).count()
    random_index = random.randint(0, all_count - 1)
    random_ip = ips_collection.find({'available': -1})[random_index]
    try:
        verifyIp(random_ip['_id'], random_ip['port'])
        print(random_ip)
    except:
        print(random_ip["_id"] + 'is dead,' + "deleting it from database")
ip1 = IpService()
#ip1.addNewIp()
#ip1.deleteIp('13.128.11.1704')
ip1.selectIp()

if __name__ == "__main__":
    timer = threading.Timer(5, renewIps)
    timer.start()