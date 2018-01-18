# -*- coding: utf-8 -*-
import json

import scrapy
from ..items import OpencourseItem, _DBConf, loadConf
import pymongo
from scrapy.http import Request
from scrapy.exceptions import CloseSpider

class CourseSpider(scrapy.Spider):
    name = "PCE"
    allowed_domains = ["pce.uw.edu"]
    start_urls = [
        'https://www.pce.uw.edu/program-finder?pagesize=12&page=1&onlyvalidsec=true&ajax=true',
    ]
    #每次开始执行抓取，都将之前的数据清空
    i = 1
    MAIN_HOST = 'https://www.pce.uw.edu'

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=True,*a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        trash_data = bool(trash_data)
        self.limit_count = int(limit_count)
        self.logger.info("开始爬虫：")
        self.logger.info("参数信息: " + storeConf)
        self.logger.info("额外参数: " + 'limit_count' + "  "+str(limit_count))
        self.logger.info("额外参数: " + 'trash_data' + "  "+str(trash_data))
        if trash_data:
            DBConf = loadConf(json.loads(storeConf),_DBConf)
            collection = pymongo.MongoClient(DBConf["MONGODB_URI"]).get_database(
                DBConf['MONGODB_DATABASE']).get_collection(DBConf['MONGODB_COLLECTION'])
            self.logger.info("正在清除数据：。。。\n" )
            self.logger.info(collection.remove(dict(college=self.name)))


    def parse(self,response):
        courseData = json.loads(response.body)
        courseNumber = courseData['Count']
        pagesCount = int(int(courseNumber)/12 + 1)
        self.logger.info("总数是：" + str(pagesCount))
        for i in range(1,pagesCount):
            yield Request(self.getRequestUrl(i),callback=self.parse_course)

    def getRequestUrl(self,i):
        return 'https://www.pce.uw.edu/program-finder?pagesize=12&page=' + str(i) + '&onlyvalidsec=true&ajax=true'


    def parse_course(self, response):
        #获取当页的12个课程的信息
        courseList = json.loads(response.body)['Items']
        for course in courseList:
            yield Request(url=self.MAIN_HOST + course['url'],callback=self.parse_detail)

    def parse_detail(self, response):
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        if response.status == 200:
            sel = scrapy.Selector(response)
            item = OpencourseItem()
            div_main = sel.xpath("//section[@class='content-block after-hero bar-before sect-about-course']")
            if len(div_main) > 0:
                div_main = div_main[0]
                stringMain = div_main.xpath("string(.)").extract()
                if len(stringMain) > 0:
                    stringMain = stringMain[0]
                    item['html'] = stringMain
                    item['title'] = sel.xpath("//title/text()").extract()[0]
                    item['catchUrl'] = response.url
                    item['college'] = self.name
                    yield item
                    self.i += 1
                else:
                    self.logger.info("获取字符失败: "+str(self.i))
                    pass
            else:
                self.logger.info("获取div失败: "+str(self.i) + "  url: " + response.url)
                pass
        else:
            print("获取网页完成")

