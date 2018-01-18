# -*- coding=utf-8 -*-
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
    name = "HangZhouLLL"
    allowed_domains = ["hzlll.cn"]
    start_urls = [
        "http://www.hzlll.cn/course/explore?page=1"
    ]
    rules = [
        Rule(LinkExtractor(allow='/course/explore(.*?)'),
             callback='parse_page',
             follow=True),
        Rule(LinkExtractor(allow='/course/(.*?)',restrict_xpaths='//ul[@class="course-wide-list"]'),
                               callback='parse_item',
                               follow=False)
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'cookie': "acw_tc=AQAAAG8JFnS1hAEApaTiZR4uilvZ02f0; JSESSIONID=c5clqzfcirdj190i5odsr4rvx; SERVERID=5b12d3171e855ece0b69bcdd0d01ecb6|1509086208|1509084471",
            'host': "www.hzlll.cn",
            'pragma': "no-cache",
            'referer': "http://www.hzlll.cn/course/explore?sort=popular&page=6",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'postman-token': "2daa4dc2-2737-c71c-9158-8d441384a54b",
            'content-type': "application/x-www-form-urlencoded"
        }
        self.host = "http://www.hzlll.cn"

    def parse_item(self,response):
        #对页面详情做处理
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        detailSoup = BeautifulSoup(response.text,"lxml")
        courseInfo = detailSoup.find("div",{"class":"col-sm-7 info"})
        if not courseInfo:
            print("没有找到信息")
            pass
        else:
            item = ZhiWangItem()
            item['title'] = courseInfo.find("h1",{"class":"title"}).text
            item['url'] = response.url
            item['hotValue'] = courseInfo.find("span",{"class":"rating-num"}).text.split("分")[0]
            item['downloadNum'] = courseInfo.find("span",{"class":"member-num"}).text
            item['sourceType'] = self.name
            item['college'] = self.name
            item['cateTag'] = ""
            item['tags'] = []
            #获取详情
            descriptionDiv = detailSoup.find("div",{"class":"panel-body"})
            if descriptionDiv:
                item["html"] = descriptionDiv.text
            else:
                item['html'] = ""
            yield item
            self.i += 1

    def parse_page(self,response):
        #对列表页做处理
        listSoup = BeautifulSoup(response.text,"lxml")
        hrefs = listSoup.find_all("a",{"class":"course-picture-link"})
        if len(hrefs) > 0:
            for href in hrefs:
                yield Request(self.host + href.get("href"),callback=self.parse_item)



