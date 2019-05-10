import json
import os
import random
import telnetlib

import datetime
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
        resp = requests.get('http://webapi.http.zhimacangku.com/getip?num=30&type=2&pro=&city=0&yys=0&port=1&time=3&ts=1&ys=0&cs=1&lb=1&sb=0&pb=4&mr=1&regions=')
        print(resp.status_code)
        for i in json.loads(resp.text)['data']:
            print(i)
            try:
                self.ips_collection.insert(
                    {"_id": i["ip"], "port": i["port"], "status": "success", "available":0, "expire_time":i["expire_time"],"edit_time": datetime.datetime.now()})
            except DuplicateKeyError as e:
                self.ips_collection.find_one_and_update({'_id': i["ip"]}, {'$set': {'port': i["port"], "status": "success", "available":0, "expire_time": i["expire_time"]}})


    def deleteIp(self, ip):
        try:
            self.ips_collection.find_one_and_update({'_id': ip}, {'$set': {'available': -1, "status": "success"}})
            print(ip+"delete success")
        except Exception as e:
            print(e)

    def verifyIp(self, ip, port):
        try:
            telnetlib.Telnet(ip, port=port, timeout=3)
        except:
            print('connect fail')
            self.deleteIp(ip)
        else:
            print('success')


    def selectIp(self):
        all_count = self.ips_collection.find({'available': 0}).count()
        for i in range(int(all_count -1)):
            print(i)
            selectedIp = self.ips_collection.find({'available': 0})[i]
            self.verifyIp(selectedIp['_id'], selectedIp['port'])
            print(selectedIp)

ip1 = IpService()
#ip1.addNewIp()
#ip1.deleteIp('13.128.11.1704')
ip1.selectIp()
