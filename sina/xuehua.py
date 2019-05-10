import telnetlib

import requests
import random

import json
import re
import csv
import codecs
import pymongo
import time

from sina.reuseIp import renewIps
from sina.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME

base_url = {
    '雪花1' : 'https://rate.tmall.com/list_detail_rate.htm?itemId=12361150270&spuId=273161719&sellerId=725677994&order=3&currentPage=',
    '雪花2' : 'https://rate.tmall.com/list_detail_rate.htm?itemId=537498345853&spuId=287917935&sellerId=725677994&order=3&currentPage=',
    '雪花3' : 'https://rate.tmall.com/list_detail_rate.htm?itemId=526403860575&spuId=473546328&sellerId=2616970884&order=3&currentPage=',
    '雪花4' : 'https://rate.tmall.com/list_detail_rate.htm?itemId=12587476646&spuId=273538780&sellerId=725677994&order=3&currentPage=',
    '雪花5' :'https://rate.tmall.com/list_detail_rate.htm?itemId=44601123454&spuId=328431322&sellerId=725677994&order=3&currentPage=',
    '雪花6' : 'https://rate.tmall.com/list_detail_rate.htm?itemId=38521201116&spuId=269441864&sellerId=2056438400&order=3&currentPage=',
}
cookies='cna=6OMZFSdQ6BkCAbSoupYMZ6wI; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; t=f4102d486c82c8dc5ecf6b7103228314; _tb_token_=eb616ee337b77; cookie2=17e795908b6b689e7c914ab7b238955b; __YSF_SESSION__={"baseId":"073760f69bd583c9","brandId":"28473332e5ccff32","departmentId":"bc3d239b2bfffa54","smartId":"8ec9f175e5a28d2b","databankProjectId":"456c38ff1c8be3da"}; skt=a765f92b655d1520; hng=CN%7Czh-CN%7CCNY%7C156; dnk=%5Cu519C%5Cu592B%5Cu82B1%5Cu9732%5Cu6C34; lid=%E5%86%9C%E5%A4%AB%E8%8A%B1%E9%9C%B2%E6%B0%B4; _m_h5_tk=2d1c306315c5f8a8517e3f5a1689a906_1557479011902; _m_h5_tk_enc=6e290b34cb98595b54354fdf26a4792c; x=__ll%3D-1%26_ato%3D0; uc1=cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=UIHiLt3xThH8t7YQouiW&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false&pas=0&cookie14=UoTZ48F60oPIjA%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dBy3qLpzNdVPPFVVI%3D&id2=UoTUPcTvBCAXWQ%3D%3D&nk2=pj4%2F6OhleeRjLA%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=%5Cu519C%5Cu592B%5Cu82B1%5Cu9732%5Cu6C34; _l_g_=Ug%3D%3D; unb=1587808208; lgc=%5Cu519C%5Cu592B%5Cu82B1%5Cu9732%5Cu6C34; cookie1=UNaG6uxMHFEL6vyIuV3g9%2FagPJIiTpC3EPU0TEYYWXQ%3D; login=true; cookie17=UoTUPcTvBCAXWQ%3D%3D; _nk_=%5Cu519C%5Cu592B%5Cu82B1%5Cu9732%5Cu6C34; sg=%E6%B0%B48c; csg=e99f7343; whl=-1%260%260%260; x5sec=7b22726174656d616e616765723b32223a226134376663373532363231666662303263313039643635303038383565366363434c6e75314f594645504343344f4b69357375774c526f4d4d5455344e7a67774f4449774f447378227d; isg=BFZW8dpNFvQr5iIdsLOTg0cmpwyYX5oe8zicCMC_bjnUg_cdKIY3QL4yH1fKK5JJ; l=bBrphVoqvAS2v6J1BOCNVuI8aCQTRIRfguPRwNjBi_5I9_TswW_OlLt2ME96Vf5P9-LB4orbVwJt0er8-y8N.'
# cookies = 't=f4102d486c82c8dc5ecf6b7103228314; _uab_collina=155348188451598513925242; cna=6OMZFSdQ6BkCAbSoupYMZ6wI; thw=cn; miid=1233431571484108734; hng=CN%7Czh-CN%7CCNY%7C156; XSRF-TOKEN=a8e8ee40-4747-4624-a9fd-e8321dca6c37; cookie2=17e795908b6b689e7c914ab7b238955b; _tb_token_=eb616ee337b77; lid=%E5%86%9C%E5%A4%AB%E8%8A%B1%E9%9C%B2%E6%B0%B4; tg=0; _gcl_aw=GCL.1556614476.Cj0KCQjw5J_mBRDVARIsAGqGLZCwaJ0Q9jkpmGgjzFf7Y1HAunHdgumd9mPHfdG1JCznoQyKyShX37EaAr40EALw_wcB; _fbp=fb.1.1556614476485.166053516; lc=VypWTWQUsuSupvdk1pFP; _cc_=UIHiLt3xSw%3D%3D; enc=4QFpMDAMa5Lce5V1ttk5BrOaJo%2Bt58RTYBazDf4rhxEmb2f4rmbskIEnYxtgdb9Zv9AX%2BUm8gbdDWGz5aETCrA%3D%3D; _m_h5_tk=12bd9247c74a0e43f5121ac6cef622f6_1557477370250; _m_h5_tk_enc=af9c468a3d0dcf2d381e88dc68c03232; whl=-1%260%260%260; x=908483460%26e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; mt=ci=0_0; v=0; cookieCheck=20165; isg=BF1dYKiF3Sk4XrlIz06nFApYbDmX0pHjhK2nPR8ij7Tj1n0I58oPnClHAIL1FqmE; l=bBMW992PvAS2vEydBOCgZuI8aCQtQIRAguPRwNjBi_5aP_T_7abOlLtPOE96Vf5R_78B4orbVwy9-etkw'
#cookies = '_uab_collina=155373986199907886304676; cna=pkUiFXGMyCwCAbSoupaINSL3; t=176948d0c346c31227397d30cb51b8df; tg=0; thw=cn; UM_distinctid=169e5db1ae7b9-086dce3a686147-7a1437-15f900-169e5db1ae859f; hng=CN%7Czh-CN%7CCNY%7C156; miid=1289992153465519228; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5hkbERWmlY9qnC73jngoSShOG8ddp80d696dn43uyKLJplOo9a821C2LNy%2FSGWB8FVX0Vvy6m4ERmgTkC%2FU94RPrxNwrccCBPJG8JHYJtt4xlNbIt1FiucNxm35NSQwXSD%2BXx8%2F%2B50DbQB%2F3XqmK7EtH2aEHunwu15VV8QWHCY3Yz0phuPXqieYIdLjMvbjm%2FSPHVg6RoF43Q3BG8q5tW2EkkoCCkfIJc7cBBk3BtVsbFgZVv0rAujDXyn8; cookie2=113c596ad29cb8027a88b7ae4579b68c; _tb_token_=eeb3e1e8eb7e8; XSRF-TOKEN=4d517010-60ce-4f71-843f-401f047cf841; lc=VypWGue0g72M7Lr29TyEVY%2B5nA%3D%3D; _cc_=Vq8l%2BKCLiw%3D%3D; enc=zbKXx4zIyof1iGV47%2Ffize2Yxdvbnnk5qOwmXERnUy0Gpev%2BkwL2O9Exd2e3iH0FRy2LWtSFtY88%2FEmJTefu7Q%3D%3D; mt=ci=0_0; cookieCheck=94275; v=0; l=bBMCU_Smv4rn9NyyBOfaCuI8aR_T4IRbzsPzw4_M0ICPOYfMS-FdWZ9vNK8HC3GVa6m9-387PXqQB08SeyUIh; isg=BJCQScTZ-MNTcqSLCgfD2cAkYd4i8XSCHr0k7Yphg-umxTJvMG0dMxS3nc2AFSx7'
# cookies = '_uab_collina=155373986199907886304676; cna=pkUiFXGMyCwCAbSoupaINSL3; t=176948d0c346c31227397d30cb51b8df; tg=0; thw=cn; UM_distinctid=169e5db1ae7b9-086dce3a686147-7a1437-15f900-169e5db1ae859f; log=lty=Ug%3D%3D; lc=VypVrlLrKxvhd%2BvVgdlFOWtKCg%3D%3D; _cc_=UIHiLt3xSw%3D%3D; enc=wkN4W9dlwNTGJG8tAx5ZBO2CAA%2FfHmMcR2ys564xuSavMev43Eq15dEnOi7jaYDN%2BlAd09CzYmxCx1SrJONHVA%3D%3D; uc3=id2=&nk2=&lg2=; tracknick=; XSRF-TOKEN=e81567bb-9166-4a91-9d81-058b99e8f0b9; cookie2=148bafadd264a95729d67c8c59f89058; _tb_token_=e50e86d737bd9; x=908483460; uc1=cookie14=UoTZ4Sw25byvIQ%3D%3D&lng=zh_CN; skt=86056188d10960de; sn=%E9%9D%92%E8%9B%99%E7%8E%8B%E5%AD%90%E6%97%97%E8%88%B0%E5%BA%97%3A%E7%81%AB%E7%82%AC; unb=2200732297847; csg=4b975287; v=0; cookieCheck=12876; l=bBMCU_Smv4rn9QMkBOfwquI8aR_ONIRbzsPzw4_M0ICP_-1pWMxcWZ_eHqL9C3GVa6EkJ3y1Nww8BcY7Dyznh; isg=BJiYNs59cMVgaFxjsi9bQZjMacbqKfwqejlKzNKJSVOKbTpXe5WYmigPpeV4_bTj'
user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
	"Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25"]

def get_user_agent():
    return random.choice(user_agent)

def w_cookie(cookies):
    cookiee = {}
    for cookie in cookies.split(';'):
        name, value = cookie.strip().split('=', 1)
        cookiee[name] = value
    return cookiee

def write_csv(file_name, datas):
    f = codecs.open(file_name,'a','utf-8')
    writer = csv.writer(f)
    writer.writerows(datas)

def save_mongo(name,datadict):
    client = pymongo.MongoClient('localhost', 27017)
    db_name = '评论数据'
    db = client[db_name]
    collection = db[name]
    collection.save(datadict)

def get_page(base_url,headers,cookies):

    clientJJ = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
    ips_collection = clientJJ[DB_NAME]['ips']
    random_ip = {}
    urlT=""

    def delete_ip(ip):
        try:
            ips_collection.find_one_and_update({'_id': ip}, {'$set': {'available': -1, "status": "success"}})
            print("delete success")
        except Exception as e:
            print(e)

    def verify_ip(ip, port):
        try:
            telnetlib.Telnet(ip, port=port, timeout=3)
        except:
            delete_ip(ip)
            print("connect failed")
            return -1
        else:
            print("success")
            return 0

    while random_ip == {}:
        all_count = ips_collection.find({'available': 0}).count()
        if all_count == 0:
            while all_count == 0:
                print("ip池死完了")
                time.sleep(180)
                renewIps()
                all_count = ips_collection.find({'available': 0}).count()
        random_index = random.randint(0, all_count - 1)
        random_ip = ips_collection.find({'available': 0})[random_index]
        if verify_ip(random_ip["_id"], random_ip["port"]) == 0:
            print(random_ip['_id'])
            print(random_ip['port'])
            urlT = "http://" + str(random_ip['_id']) + ":" + str(random_ip['port'])

        else:
            random_ip = {}
    print(urlT)
    proxies = {"http": urlT}
    first_url = base_url + '1'
    r = requests.get(url=first_url, headers=headers, cookies=cookies, proxies=proxies)
    print(first_url)

    print(r.text)
    pettrn = re.compile('\((.*)\)', re.S)
    con = re.findall(pettrn, str(r.text))

    jc = json.loads(str(con[0]))
    # print(jc.keys())
    contents = []
    # content = {}
    #details = jc.get('rateDetail').get('rateList')
    try:
        page = jc.get('rateDetail').get('paginator').get('lastPage')
        print('共有{}页评论'.format(page))
        return int(page)
    except:
        page = 1
        print('共有{}页评论'.format(page))
        return int(page)

def w_content(url,headers,cookies,k):
    clientJJ = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
    ips_collection = clientJJ[DB_NAME]['ips']
    random_ip = {}
    urlT=""

    def delete_ip(ip):
        try:
            ips_collection.find_one_and_update({'_id': ip}, {'$set': {'available': -1, "status": "success"}})
            print("delete success")
        except Exception as e:
            print(e)

    def verify_ip(ip, port):
        try:
            telnetlib.Telnet(ip, port=port, timeout=3)
        except:
            delete_ip(ip)
            print("connect failed")
            return -1
        else:
            print("success")
            return 0

    while random_ip == {}:
        all_count = ips_collection.find({'available': 0}).count()
        if all_count == 0:
            while all_count == 0:
                print("ip池死完了")
                #time.sleep(180)
                renewIps()
                all_count = ips_collection.find({'available': 0}).count()
        random_index = random.randint(0, all_count - 1)
        random_ip = ips_collection.find({'available': 0})[random_index]
        if verify_ip(random_ip["_id"], random_ip["port"]) == 0:
            print(random_ip['_id'])
            print(random_ip['port'])
            urlT = "http://" + str(random_ip['_id']) + ":" + str(random_ip['port'])

        else:
            random_ip = {}
    print(urlT)
    proxies = {"http": urlT}
    r = requests.get(url=url, headers=headers, cookies=cookies,proxies=proxies)
    #print(r.text)
    pettrn = re.compile('\((.*)\)', re.S)
    con = re.findall(pettrn, str(r.text))

    jc = json.loads(str(con[0]))
    #print(jc.keys())
    contents = []
    #content = {}
    details = jc.get('rateDetail').get('rateList')
    #page = jc.get('rateDetail').get('paginator').get('lastPage')
    for detail in details:
        id = detail.get('id')
        # content['sellerId'] = detail.get('sellerId')
        time = detail.get('rateDate')
        content = detail.get('rateContent')
        s = [id, time, content]
        contents.append(s)
    print(contents)
    time.sleep(10)
    write_csv(k+'.csv',contents)
    save_mongo(k,contents)
    #time.sleep(5)


if __name__ == '__main__':
    # # 代理服务器
    # proxyHost = "http-pro.abuyun.com"
    # proxyPort = "9010"
    #
    # # 代理隧道验证信息
    # proxyUser = "H1T2K1E210A6427P"
    # proxyPass = "B3A3992CB1D70227"
    #
    # proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    #     "host": proxyHost,
    #     "port": proxyPort,
    #     "user": proxyUser,
    #     "pass": proxyPass,
    # }
    #
    # proxies = {
    #     "http": proxyMeta,
    #     "https": proxyMeta,
    # }
    cookiee = w_cookie(cookies)
    lose = []
    for k,v in base_url.items():
        pages = get_page(v,{'user_agent': get_user_agent()},cookiee)
        for i in range(1, pages + 1):
            if i % 10 == 0:
                time.sleep(30)
            else:
                url = v + str(i)
                print('正在抓取店铺{}第{}页'.format(k,i))
                headers = {'user_agent': get_user_agent()}
                try:
                    w_content(url, headers, cookiee,k)
                    time.sleep(random.randint(10, 30))
                except:
                    print('店铺{}第{}页抓取失败'.format(k,i))
                    lose.append(i)
                    print(lose)
                    continue