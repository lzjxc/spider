# encoding: utf-8

import telnetlib
import time

import pymongo
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from sina.resource.resource import USER_AGENT_LIST
from sina.reuseIp import renewIps
from sina.settings import LOCAL_MONGO_PORT, LOCAL_MONGO_HOST, DB_NAME
import random

#class RandomUserAgent(UserAgentMiddleware):
#   def process_request(self, request, spider):
#       ua = random.choice(USER_AGENT_LIST)
#       request.headers.setdefault('User-Agent', ua)

class CookieMiddleware(object):
    """
    每次请求都随机从账号池中选择一个账号去访问
    """

    def __init__(self, ip=''):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.account_collection = client[DB_NAME]['account']
        self.ips_collection = client[DB_NAME]['ips']
        self.ip = ip

    '''def delete_ip(self, ip):
        try:
            self.ips_collection.find_one_and_update({'_id': ip}, {'$set': {'available': -1, "status": "success"}})
            print("delete success")
        except Exception as e:
            print(e)
    
    def verify_ip(self, ip, port):
        try:
            telnetlib.Telnet(ip, port=port, timeout=3)
        except:
            print(ip + ' is dead,' + "deleting it from database")
            self.delete_ip(ip)

        else:
            print('success')
    
    def select_ip(self):
        all_count = self.ips_collection.find({'available': 0}).count()
        if all_count == 0:
            raise Exception("ip池死完了")
        random_index = random.randint(0, all_count - 1)
        random_ip = self.ips_collection.find({'available': 0})[random_index]
        if telnetlib.Telnet(random_ip['_id'], port=random_ip['port'], timeout=3):
            print(random_ip)
            return random_ip
        else:
            self.delete_ip(random_ip['_id'])
            self.select_ip()
    '''
    def process_request(self, request, spider):
        all_count = self.account_collection.find({'status': 'success'}).count()
        if all_count == 0:
            raise Exception('当前账号池为空')
        random_index = random.randint(0, all_count - 1)
        random_account = self.account_collection.find({'status': 'success'})[random_index]
        request.headers.setdefault('Cookie', random_account['cookie'])
        request.meta['account'] = random_account
        #thisip = self.select_ip()
        #print("thisip: " + str(thisip["_id"]) + ":" + str(thisip["port"]))
        #request.meta["proxy"] = "http://" + str(thisip["_id"]) + ":" + str(thisip["port"])



class RedirectMiddleware(object):
    """
    检测账号是否正常
    302 / 403,说明账号cookie失效/账号被封，状态标记为error
    418,偶尔产生,需要再次请求
    """

    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.account_collection = client[DB_NAME]['account']

    def process_response(self, request, response, spider):
        http_code = response.status
        if http_code == 302 or http_code == 403:
            self.account_collection.find_one_and_update({'_id': request.meta['account']['_id']},
                                                        {'$set': {'status': 'error'}}, )
            return request
        elif http_code == 418:
            spider.logger.error('ip 被封了!!!请更换ip,或者停止程序...')
            time.sleep(random.randint(60, 600))
            return request
        else:
            return response


class MyproxiesSpiderMiddleware(object):

    def __init__(self, ip=''):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.ips_collection = client[DB_NAME]['ips']
        self.ip = ip

    def delete_ip(self, ip):
        try:
            self.ips_collection.find_one_and_update({'_id': ip}, {'$set': {'available': -1, "status": "success"}})
            print("delete success")
        except Exception as e:
            print(e)

    def verify_ip(self, ip, port):
        try:
            telnetlib.Telnet(ip, port=port, timeout=3)
        except:
            self.delete_ip(ip)
            print("connect failed")
            return -1
        else:
            print("success")
            return 0
            
    def process_request(self, request, spider):
        #pass
        random_ip = {}
        while random_ip == {}:
            all_count = self.ips_collection.find({'available': 0}).count()
            if all_count == 0:
                while all_count == 0:
                    print("ip池死完了")
                    time.sleep(180)
                    renewIps()
                    all_count = self.ips_collection.find({'available': 0}).count()
            random_index = random.randint(0, all_count - 1)
            random_ip = self.ips_collection.find({'available': 0})[random_index]
            if self.verify_ip(random_ip["_id"], random_ip["port"]) == 0:
                print(random_ip['_id'])
                print(random_ip['port'])
                urlT = "http://"+str(random_ip['_id']) + ":" + str(random_ip['port'])
                print(urlT)
                request.meta["proxy"] = urlT
            else:
                random_ip ={}



