# -*- coding=utf-8 -*-
# -*- coding: utf-8 -*-
import json
from time import sleep

import scrapy
from scrapy import Request
from scrapy.spiders import Spider, Rule
from ..items import KeywordItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from .commonFn import *
from bs4 import BeautifulSoup


class CourseSpider(Spider):
    name = "ERIC"
    allowed_domains = ["eric.ed.gov"]
    start_urls = [
        "http://www.baidu.com"
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }
        self.host = "https://eric.ed.gov/"

    def parse(self,response):

        headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }

        #keywords
        # keywords = ["Massive Open Online Courses","Mobile Learning"]
        keywords = [
                    "Open learning"
                    ]
        for word in keywords:
            isGoon = True
            num = 1
            while(isGoon):
                if num >= self.limit_count != 0:
                    self.close(CourseSpider, "抓取完成")
                    isGoon = False
                    raise CloseSpider("已抓取完成")
                else:
                    url = "https://eric.ed.gov/?q="+word.replace(" ","+")+"&pg="
                    response = requests.request("GET", url+str(num), headers=headers)
                    if response.status_code == 200:
                        html = BeautifulSoup(response.text,"lxml")
                        tagAs = html.find_all("div",{"class":"r_i"})
                        if len(tagAs) > 0:
                            for content in tagAs:
                                item = KeywordItem()
                                item['title'] = content.find("div",{"class":"r_t"}).text
                                item['html'] = content.find("div",{"class":"r_d"}).text
                                item['downloadNum'] = '0'
                                if content.find("div",{"class":"number"}):
                                    item['downloadNum'] = content.find("div",{"class":"number"}).text
                                item['tags'] = []
                                keywordsDiv = content.find("div",{"class":"keywords"}).text.split(", ")
                                for a in keywordsDiv:
                                    item['tags'].append(a)
                                item['url'] = self.host +  content.find("div",{"class":"r_t"}).find("a").get("href")
                                #请求详情数据
                                try:
                                    dRes = requests.request("GET",url=item['url'],headers=headers)
                                    if dRes.status_code == 200:
                                        dSoup = BeautifulSoup(dRes.text,'lxml')
                                        item['html'] = dSoup.find("div",{"class":"abstract"}).text
                                except Exception as e:
                                    pass
                                item['cateTag'] = ""
                                item['college'] = self.name
                                item['sourceType'] = self.name
                                item['hotValue'] = randint(0,5)
                                item['keyword'] = word
                                yield item
                                try:
                                    print(item)
                                except Exception as e:
                                    print(e)
                            num += 1
                        else:
                            isGoon = False
                            self.logger.debug("页面上获取课程信息失败")
                    else:
                        isGoon = False
                        self.logger.error("获取list页面失败")




