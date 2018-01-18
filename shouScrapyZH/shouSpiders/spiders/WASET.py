# -*- coding=utf-8 -*-
# -*- coding: utf-8 -*-
import json
from time import sleep

import scrapy
from scrapy import Request
from scrapy.spiders import Spider, Rule
from ..items import ZhiWangItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from .commonFn import *
from bs4 import BeautifulSoup


class CourseSpider(Spider):
    name = "WASET"
    allowed_domains = ["waset.org"]
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

    def parse(self,response):
        url = "https://waset.org/abstracts/educational-and-pedagogical-sciences?&page="
        headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }

        isGoon = True
        num = 26
        while(isGoon):
            if num >= self.limit_count != 0:
                self.close(CourseSpider, "抓取完成")
                isGoon = False
                raise CloseSpider("已抓取完成")
            else:
                response = requests.request("GET", url+str(num), headers=headers)
                if response.status_code == 200:
                    html = BeautifulSoup(response.text.replace("!--","").replace("--!",""),"lxml")
                    tagAs = html.find_all("div",{"class":"onePaper"})
                    if len(tagAs) > 0:
                        print(len(tagAs))
                        for content in tagAs:
                            item = ZhiWangItem()
                            item['title'] = content.find("div",{"class":"title"}).text
                            item['html'] = content.find("div",{"class":"description"}).text
                            item['downloadNum'] = '0'
                            if content.find("div",{"class":"number"}):
                                item['downloadNum'] = content.find("div",{"class":"number"}).text
                            item['tags'] = []
                            keywordsDiv = content.find("div",{"class":"keywords"}).find_all("a")
                            for a in keywordsDiv:
                                item['tags'].append(a.text)
                            item['url'] = response.url
                            item['cateTag'] = ""
                            item['college'] = self.name
                            item['sourceType'] = self.name
                            item['hotValue'] = randint(0,5)
                            yield item
                        num += 1
                        sleep(10)
                    else:
                        isGoon = False
                        self.logger.debug("页面上获取课程信息失败")
                else:
                    isGoon = False
                    self.logger.error("获取list页面失败")




