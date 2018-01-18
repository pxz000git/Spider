# -*- coding=utf-8 -*-
# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider,Spider, Rule
from ..items import ZhiWangItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from .commonFn import *
from bs4 import BeautifulSoup


class CourseSpider(Spider):
    name = "ZheJiangLLL"
    allowed_domains = ["zjerc.cn"]
    start_urls = [
        "http://www.zjerc.cn/Web/default.aspx"
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.headers = {
            'accept': "application/json, text/javascript, */*; q=0.01",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'content-length': "73",
            'content-type': "application/x-www-form-urlencoded",
            'cookie': "ASP.NET_SessionId=sfz54tr5bkyj05y0snnegs45",
            'host': "www.zjerc.cn",
            'origin': "http://www.zjerc.cn",
            'pragma': "no-cache",
            'referer': "http://www.zjerc.cn/Web/Media/Media.aspx",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'x-requested-with': "XMLHttpRequest"
        }

    def parse_item(self,response):
        #对页面详情做处理
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        detailSoup = BeautifulSoup(response.text,"lxml")
        courseInfo = detailSoup.find("div",{"class":"lht22 mgt20"})
        if not courseInfo:
            print("没有找到信息")
            pass
        else:
            item = ZhiWangItem()
            item['title'] = response.meta["title"]
            item['url'] = response.url
            item['hotValue'] = response.meta["hotValue"]
            item['downloadNum'] = response.meta["downloadNum"]
            item['sourceType'] = self.name
            item['college'] = response.meta['college']
            item['cateTag'] = ""
            #关键词
            keywords = detailSoup.find("input",{"class":"keyword"})
            if keywords:
                keywords = keywords.get("value")
                item['tags'] = keywords.replace(",","").split("，")
            else:
                item['tags'] = []
            #获取详情
            descriptionDiv = detailSoup.find("div",{"class":"lht22 mgt20"}).find("p")
            if descriptionDiv:
                item["html"] = descriptionDiv.text
            else:
                item['html'] = ""
            yield item
            # print(item)
            self.i += 1

    def parse(self,response):
        url = "http://www.zjerc.cn/Data/CourseData.aspx"
        querystring = {"action":"courselist","pagesize":"520","pageindex":"0","refresh":"0.6971929987519265"}
        payload = "orderby=Create_Date&classid=&tag=zt"
        res = requests.request("POST", url, data=payload, headers=self.headers, params=querystring)
        if res.status_code != 200:
            print("请求课程list失败")
            exit(0)
        courseList = json.loads(res.text)
        urlProfix = "http://www.zjerc.cn/Web/Course/CourseDetail.aspx?resid="
        for course in courseList["BaseData"]:
            item = {}
            item['title'] = course["COURSE_NAME"]
            item['college'] = course["COURSE_SOURCE"]
            item['startTime'] = course["CREATE_DATE"]
            item['downloadNum'] = course["CLICK_NUM"]
            item['hotValue'] = course["COMM_COUNT"]
            yield scrapy.Request(urlProfix + course["COURSE_NUM"],meta=item,callback=self.parse_item)



