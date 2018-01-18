# -*- coding=utf-8 -*-
from time import sleep

import re
import requests
import scrapy
from scrapy.spiders import Spider
from ..items import DrugItem, _DBConf
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
from .commonFn import initSpider,getProxy,randomIP
import json
from redis import Redis
import threading

threadCount = 0
isGoon = True
myLock = threading.RLock()


class CourseSpider(Spider):
    name = "YaoZhiAPP"
    allowed_domains = ["yaozh.com"]
    start_urls = [
        'http://www.yaozh.com/'
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.r = Redis(db=1)
        self.headers = {
            'host': "db.yaozh.com",
            'content-type': "application/x-www-form-urlencoded; charset=utf-8",
            'cookie': "PHPSESSID=l83u0f3sivqagringcn9l7vem5",
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
            'accept-language': "zh-Hans-CN, en-us",
            'content-length': "56",
            'connection': "keep-alive",
            'cache-control': "no-cache"
        }
        self.host = "https://db.yaozh.com"


    def requestsUrl(self,num):
        global threadCount,isGoon
        myLock.acquire()
        print(u"Start Requests："+str(num))
        url = "http://db.yaozh.com/api/index.php/Home/index/pijian/id/"+str(num)
        instructUrl = "http://db.yaozh.com/api/index.php/Home/index/app_instruct/id/"+str(num)
        payload = "v=1.0&id="+str(num)+"&access_token=6960ec647f61f5e620a8e4621857bd7b"
        myLock.release()
        try:
            session = requests.Session()
            response = session.request("POST", url, data=payload, headers=self.headers ,timeout=20)
            sleep(1)

            if response.status_code == 200:
                #这是json
                resJSON = json.loads(response.text)
                drugInfo = resJSON['data']
                #请求说明书信息
                instructRes = session.request("POST",url=instructUrl,data=payload,headers=self.headers,timeout=20)
                if instructRes.status_code == 200:
                    instructInfo = json.loads(instructRes.text)["data"]
                    drugInfo['instruction'] = instructInfo
                else:
                    drugInfo['instruction'] = {}
                print("药品" + str(num) + "抓取完成")
                self.saveToMongodb(drugInfo)
                threadCount = threadCount - 1
            else:
                print("请求药品信息失败")
                threadCount = threadCount - 1
        except Exception as e:
            print(str(e))
            threadCount = threadCount - 1
            print(u"Requests Error")

    def parse(self,response):
        global threadCount,isGoon
        num = 100000
        while(isGoon):
            if num > 200000:
                isGoon = False
            else:
                if threadCount < 4:
                    t = threading.Thread(target=self.requestsUrl, name = "Name: "+str(num),args=(num,))
                    threadCount += 1
                    num += 1
                    t.start()

    def filterStr(self,str):
        r = u'[!"#$%&\'()；\ （）*+-/:;<=>?@，\\ \\ \\r\\t\\n\\：。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        return re.sub(r, '', str)

    def saveToMongodb(self,item):
        self.collection.update({"me_uid":item['me_uid']},{"$set":item},True)