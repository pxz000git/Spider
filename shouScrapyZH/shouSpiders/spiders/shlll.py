# -*- coding=utf-8 -*-
# -*- coding: utf-8 -*-
import json

import re
import scrapy
from scrapy import Request
from scrapy.spiders import Spider, Rule
from ..items import ZhiWangItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from .commonFn import *
from bs4 import BeautifulSoup


class CourseSpider(Spider):
    name = "SHLLL"
    allowed_domains = ["xinstudy.cn"]
    start_urls = [
        "http://course.xinstudy.cn/course/coursesearch/p_1/1/A63B73AEB3B95A63"
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
            'cookie': "KeyId=201711090222579566160; _ssma_uuid=h2lz08587684%7C1%7C1510208596547%7C4; _ssma_prom=%21%21%21%21%21%21%21%21%21%21shlll.xinstudy.cn; Hm_lvt_6ca93febbe5f3e3b14f8ee9b8ef13802=1510208597; Hm_lpvt_6ca93febbe5f3e3b14f8ee9b8ef13802=1510208603; _ssma_sess=3omm6547%7C1510208596547%7C6885%7C0%7C; _ssma_tm=1510208603432",
            'host': "course.xinstudy.cn",
            'pragma': "no-cache",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'postman-token': "063d843a-f765-16de-5a8c-e063cb416542"
        }
        self.host = "http://www.hzlll.cn"

    def parse(self,response):
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'cookie': "KeyId=201711090222579566160; _ssma_uuid=h2lz08587684%7C1%7C1510208596547%7C4; _ssma_prom=%21%21%21%21%21%21%21%21%21%21shlll.xinstudy.cn; Hm_lvt_6ca93febbe5f3e3b14f8ee9b8ef13802=1510208597; Hm_lpvt_6ca93febbe5f3e3b14f8ee9b8ef13802=1510210914; _ssma_sess=3omm6547%7C1510208596547%7C2317122%7C0%7C; _ssma_tm=1510210913669",
            'host': "course.xinstudy.cn",
            'pragma': "no-cache",
            'referer': "http://course.xinstudy.cn/course/coursesearch/p_1/1/A63B73AEB3B95A63",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'postman-token': "e1a29c51-f17a-c8d0-b9e5-50e49a9ca046"
        }

        isGoon = True
        num = 1
        while(isGoon):
            if num >= self.limit_count != 0:
                self.close(CourseSpider, "抓取完成")
                isGoon = False
                raise CloseSpider("已抓取完成")
            else:
                url = "http://course.xinstudy.cn/course/coursesearch/p_"+str(num)+"/1/A63B73AEB3B95A63"
                response = requests.request("GET", url, headers=headers)
                if response.status_code == 200:
                    html = BeautifulSoup(response.text,"lxml")
                    tagAs = html.find("div",{"id":"d_coursesearch"}).find_all("div",{"class":"item"})
                    if len(tagAs) > 0:
                        for tagA in tagAs:
                            item = ZhiWangItem()
                            item['title'] = tagA.find("div",{"class":"title"}).text
                            item['hotValue'] = tagA.find("div",{"class":"info"}).find("span").get("class")[1][-2:-1]
                            courseA = tagA.find("a").get("href")
                            courseUrl = "http://course.xinstudy.cn" + courseA
                            Dresponse = requests.request("GET",courseUrl,headers=headers)
                            if Dresponse.status_code == 200:
                                Dhtml = BeautifulSoup(Dresponse.text,"lxml")
                                try:
                                    item["html"] = Dhtml.find("div",{"id":"d_courseintro"}).find("div",{"class":"area txt-justify"}).text.encode("ISO-8859-1").decode("utf-8")
                                except Exception as e:
                                    item['html'] = "无"
                                item["sourceType"] = "上海学习网"
                                item["college"] = self.name
                                item["downloadNum"] = Dhtml.find("span",{"id":"info1"}).text
                                item["url"] = Dresponse.url
                                item['tags'] = []
                                try:
                                    tagsA = Dhtml.find("div",{"id":"d_coursetag"}).find_all("a")
                                    for tag in tagsA:
                                        item['tags'].append(tag.text.encode("ISO-8859-1").decode("utf-8"))
                                except Exception as e:
                                    pass
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


    def filterStr(self,str):
        r = u'[!"#$%&\'()；\ （）*+-/:;<=>?@，\\ \\ \\r\\t\\n\\：。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        return re.sub(r, '', str)

