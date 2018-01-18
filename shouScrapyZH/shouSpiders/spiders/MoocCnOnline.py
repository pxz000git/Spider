# -*- coding=utf-8 -*-
# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider,Spider, Rule
from ..items import TimeItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from .commonFn import *
from bs4 import BeautifulSoup


class CourseSpider(Spider):
    name = "MoocCnOnline"
    allowed_domains = ["icourses.cn","icourse163.org"]
    start_urls = [
        "http://www.icourses.cn/oc/"
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
            'content-length': "53",
            'content-type': "application/x-www-form-urlencoded",
            'cookie': "icoursesSymbol=wKg3KFneH1B3cyKZH2IMAg==; TJ_VISIT=1509330666088; route=e463d8a73b281261355472cb8f8581d3; bdshare_firstime=1509330954725; JSESSIONID=822B56BFFDC38F5FF06CE1BA376589BD.sns81-4; TJ_PVT=1509347521582; Hm_lvt_787dbcb72bb32d4789a985fd6cd53a46=1508997260,1508997698,1509000382,1509330668; Hm_lpvt_787dbcb72bb32d4789a985fd6cd53a46=1509347522",
            'host': "www.icourses.cn",
            'origin': "http://www.icourses.cn",
            'pragma': "no-cache",
            'referer': "http://www.icourses.cn/oc/",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'x-requested-with': "XMLHttpReques",
            'postman-token': "b6f026a6-6d5c-4133-6f98-ed1b92045eff"
        }

    def parse_item(self,response):
        #对页面详情做处理
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        detailSoup = BeautifulSoup(response.text,"lxml")
        courseInfo1 = detailSoup.find("p",{"id":"j-rectxt"})
        descHtml = courseInfo1.text.replace("spContent=","")
        courseInfo2 = detailSoup.find_all("div",{"class":"f-richEditorText"})[0].get_text()
        descHtml += courseInfo2
        item = TimeItem()
        item['title'] = response.meta["title"]
        item['url'] = response.url
        item['hotValue'] = 0
        item['downloadNum'] = 0
        item['sourceType'] = self.name
        item['college'] = response.meta['college']
        item['cateTag'] = ""
        item['tags'] = []
        item['startTime'] = response.meta['startTime']
        #获取详情
        item['html'] = descHtml
        yield item
        # print(item)
        self.i += 1

    def parse(self,response):
        isGoon = True
        url = "http://www.icourses.cn/ocPage.action"
        pageNum = 1
        while(isGoon):
            payload = "page.currentPage="+str(pageNum)+"&page2.pageSize=12&typeId=1&sortId="
            res = requests.request("POST", url, data=payload, headers=self.headers)
            if res.status_code != 200:
                print("请求课程list失败")
                isGoon = False
                exit(0)
            Chtml = BeautifulSoup(res.text,'lxml')
            CourseDiv = Chtml.find_all("div",{"class":"cour"})
            if len(CourseDiv) > 0 :
                for Course in CourseDiv:
                    href = Course.find("div",{"class":"cour_img"}).find("a").get("href")
                    item = {}
                    item['title'] = Course.find("div",{"class":"mb_p"}).text
                    item['college'] = Course.find("div",{"class":"cour_xx"}).find_all("a")[1].text
                    item['startTime'] = Course.find("div",{"class":"cour_xx"}).find_all("span")[1].text
                    yield scrapy.Request(href,meta=item,callback=self.parse_item)
                pageNum += 1
            else:
                print("获取list失败")
                isGoon = False



