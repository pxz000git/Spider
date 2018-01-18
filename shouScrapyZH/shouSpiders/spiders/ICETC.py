# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from ..items import ZhiWangItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from .commonFn import *
from bs4 import BeautifulSoup


class CourseSpider(CrawlSpider):
    name = "ICETC"
    allowed_domains = ["icetc.org"]
    start_urls = [
        "http://www.icetc.org/index.html"
    ]
    rules = [
        Rule(LinkExtractor(allow='/(.*?)'),
             callback='parse_item',
             follow=True)
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

    def parse_item(self,response):
        #对页面详情做处理
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        detailSoup = BeautifulSoup(response.text,"lxml")
        courseInfo = detailSoup.find("body")
        if not courseInfo:
            print("没有找到信息")
            pass
        else:
            item = ZhiWangItem()
            item['title'] = detailSoup.find("title").text
            item['url'] = response.url
            item['hotValue'] = str(randint(0,5))
            item['downloadNum'] = str(randint(0,150))
            item['sourceType'] = self.name
            item['college'] = self.name
            item['cateTag'] = ""
            item['tags'] = []
            #获取详情
            item['html'] = courseInfo.get_text()
            yield item
            self.i += 1
            # print(item)



