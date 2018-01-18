# -*- coding=utf-8 -*-
# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from scrapy.spiders import Spider, Rule
from ..items import ZhiWangItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from .commonFn import *
from bs4 import BeautifulSoup


class CourseSpider(Spider):
    name = "LaoNianRen"
    allowed_domains = ["e60sh.com"]
    start_urls = [
        "http://www.e60sh.com/Course/QueryList?TagIds=&Page=1"
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.headers = {
            'accept': "text/html, */*; q=0.01",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'cookie': "ASP.NET_SessionId=0rk2hmnevizqj5but0vqc4qr; ResourceSiteKeyId=201711090129520438420",
            'host': "www.e60sh.com",
            'pragma': "no-cache",
            'referer': "http://www.e60sh.com/Course/list",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'x-requested-with': "XMLHttpRequest",
            'postman-token': "7a981e06-6a52-3dfe-36ed-892bbca5678e"
        }
        self.host = "http://www.hzlll.cn"

    def parse(self,response):
        print(1312312)
        url = "http://www.e60sh.com/Course/QueryList"
        headers = {
            'accept': "text/html, */*; q=0.01",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'cookie': "ASP.NET_SessionId=0rk2hmnevizqj5but0vqc4qr; ResourceSiteKeyId=201711090129520438420",
            'host': "www.e60sh.com",
            'pragma': "no-cache",
            'referer': "http://www.e60sh.com/Course/list",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'x-requested-with': "XMLHttpRequest",
            'postman-token': "7a981e06-6a52-3dfe-36ed-892bbca5678e"
        }

        isGoon = True
        num = 1
        while(isGoon):
            querystring = {"TagIds":"","Page":str(num)}
            if num >= self.limit_count != 0:
                self.close(CourseSpider, "抓取完成")
                isGoon = False
                raise CloseSpider("已抓取完成")
            else:
                response = requests.request("GET", url, headers=headers, params=querystring)
                if response.status_code == 200:
                    html = BeautifulSoup(response.text,"lxml")
                    tagAs = html.find_all("div",{"class":"list_content"})
                    if len(tagAs) > 0:
                        for tagA in tagAs:
                            courseA = tagA.find("a").get("href")
                            courseUrl = "http://www.e60sh.com" + courseA
                            Dresponse = requests.request("GET",courseUrl)
                            if Dresponse.status_code == 200:
                                Dhtml = BeautifulSoup(Dresponse.text,"lxml")
                                item = ZhiWangItem()
                                item["title"] = Dhtml.find("div",{"class":"title"}).text
                                try:
                                    item["html"] = Dhtml.find("div",{"id":"showcontenth"}).find("p").text
                                except AttributeError as e:
                                    item['html'] = "无"
                                item["sourceType"] = "老年人学习网"
                                item["college"] = self.name
                                item["hotValue"] = randint(0,5)
                                item["downloadNum"] = randint(1,500)
                                item["url"] = Dresponse.url
                                item["tags"] = ""
                                item["cateTag"] = ""
                                yield item
                            else:
                                self.logger.debug("获取课程详情页面失败")
                        num += 1
                    else:
                        isGoon = False
                        self.logger.debug("页面上获取课程信息失败")
                else:
                    isGoon = False
                    self.logger.error("获取list页面失败")




