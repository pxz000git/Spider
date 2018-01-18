# -*- coding=utf-8 -*-
from time import sleep

import re
import requests
import scrapy
from scrapy.spiders import Spider
from ..items import ZhiWangItem, _DBConf
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
    name = "WanFang"
    allowed_domains = ["shuxiavip.com"]
    start_urls = [
        'http://www.shuxiavip.com/course.html'
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.r = Redis(db=1)
        self.cookie = {
            'cookie': "SERVERID=958b97eacbe3c49360ace2dfc0bd31b4|1507717368|1507713772",
        }
        self.headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'cookie': "Hm_lvt_f5e6bd27352a71a202024e821056162b=1507729920; Hm_lpvt_f5e6bd27352a71a202024e821056162b=1507729989; WFKS.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%5d%2c%22Data%22%3a%5b%5d%2c%22SessionId%22%3a%228e180150-d977-47e5-8435-96e76595ec9e%22%2c%22Sign%22%3a%22hi+authserv%22%7d%2c%22LastUpdate%22%3a%222017-10-11T13%3a59%3a36Z%22%2c%22TicketSign%22%3a%22uH%2bEBqcg0n1NXO48V9NQPg%3d%3d%22%7d",
            'host': "s.wanfangdata.com.cn",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }
        self.DetailHeaders = {
            "X-Forwarded-For":randomIP(),
            "X-Real-IP":randomIP()
        }


    def requestsUrl(self,num):
        url = "http://s.wanfangdata.com.cn/Paper.aspx"
        global threadCount,isGoon
        myLock.acquire()
        print(u"Start Requests："+str(num))
        querystring = {"q":"成人教育","f":"top","p":str(num)}
        myLock.release()
        try:
            response = requests.request("GET", url, headers=self.headers, params=querystring,timeout=20)
            if response.status_code == 200:
                html = BeautifulSoup(response.content,'lxml')
                recordItems = html.find_all("div",{"class":"record-item"})
                if len(recordItems) > 0:
                    #对于一个页面的所有详情，我们使用一个固定的代理去请求，避免过多的请求代理服务
                    proxies = getProxy()
                    #获取代理成功
                    print(proxies["http"])
                    for item in recordItems:
                        #解析数据,请求详
                        try:
                            res = requests.request("GET",item.find("a",{"class":"title"}).get("href"),headers=self.DetailHeaders,timeout=40,proxies=proxies)
                            if res.status_code == 200:
                                Dhtml = BeautifulSoup(res.text,'lxml')
                                baseInfo = Dhtml.find("div",{"class":"section-baseinfo"})
                                ScItem = ZhiWangItem()
                                ScItem["sourceType"] = "万方"
                                ScItem["college"] = "WanFang"
                                ScItem["hotValue"] = 0
                                ScItem["downloadNum"] = 0
                                if baseInfo:
                                    ScItem["title"] = baseInfo.find("h1").text
                                    ScItem["html"] = baseInfo.find("div",{"class":"text"}).text
                                    ScItem["url"] = res.url
                                else:
                                    continue
                                filedInfo = Dhtml.find("div",{"class":"fixed-width baseinfo-feild"})
                                if filedInfo:
                                    tagsA = filedInfo.find("div",{"class":"row row-keyword"})
                                    if tagsA:
                                        tagsA = tagsA.find_all("a")
                                    else:
                                        tagsA = []
                                    tempTag = []
                                    for tag in tagsA:
                                        tempTag.append(tag.text)
                                    ScItem["tags"] = tempTag
                                    ScItem["cateTag"] = ""
                                else:
                                    continue
                                #获取完成，返回item
                                self.saveToMongodb(ScItem)
                            else:
                                #请求详情失败，直接跳过
                                print("Detail Info Requests Field:")
                                continue
                        except Exception as e:
                            print("Process Detail Info Error: " + str(e))
                            continue
                    #请求完成了
                    print("Detail Info Requests Complete!! ThreadCount --")
                    threadCount = threadCount - 1
                else:
                    #获取列表失败了
                    print("List Count empty")
                    threadCount = threadCount - 1
            else:
                #请求失败的考虑重新加入到队列中
                print(u"Requests Field")
                print(response.text)
                print(response.status_code)
                threadCount = threadCount - 1
        except Exception as e:
            print(str(e))
            threadCount = threadCount - 1
            print(u"Requests Error")

    def parse(self,response):
        global threadCount,isGoon
        num = 1107
        while(isGoon):
            if num > 6292:
                isGoon = False
            else:
                if threadCount < 4:
                    t = threading.Thread(target=self.requestsUrl, name = "Name: "+str(num),args=(num,))
                    threadCount += 1
                    num += 1
                    t.start()

    def filterStr(self,str):
        r = u'[0-9!"#$%&\'()；\ （）*+-/:;<=>?@，\\ \\ \\r\\t\\n\\：。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        return re.sub(r, '', str)

    def saveToMongodb(self,item):
        from bson import ObjectId
        item["_id"] = ObjectId()
        item["html"] = self.filterStr(item["html"])
        item["title"] = self.filterStr(item["title"])
        self.collection.insert(item)