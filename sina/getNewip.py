import json
import telnetlib
import threading
from threading import Timer

import urllib3
import requests


#resp = requests.get('http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=3&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
#print (resp.status_code)
#dict_resp = json.loads(resp.text)['data'][0]
#print(dict_resp)
#telnetlib.Telnet('220.186.174.4', port='4207', timeout=3)
from sina.reuseIp import renewIps

dict1 = {
    "code":0,
    "success":'true',
    "msg":"0",
    "data":[
        {
            "ip":"112.85.124.8",
            "port":4230,
            "expire_time":"2019-03-19 13:57:18"
        },
        {
            "ip":"124.112.105.75",
            "port":4227,
            "expire_time":"2019-03-19 14:05:46"
        }
    ]
}
#def printHello():
#    print("start")
#    timer = threading.Timer(5, printHello)
#    timer.start()


#if __name__ == "__main__":
#    timer = threading.Timer(5, printHello)
 #   timer.start()

#for i in dict1:
#    print(i)
#{"ip":"113.121.146.124","port":5649}
#{"code":0,"success":true,"msg":"0","data":[{"ip":"111.72.107.13","port":9756,"expire_time":"2019-03-19 04:59:34"}]}
#222.188.136.167 20124
#180.95.170.12 3012
'''ip='119.114.98.106'
port='4286'
try:
    telnetlib.Telnet(ip, port=port, timeout=3)
except:
    print(ip + ' is dead,' + "deleting it from database")
else:
    print('success')'''
renewIps()