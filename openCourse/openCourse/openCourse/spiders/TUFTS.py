# -*- coding: utf-8 -*-
import json

import scrapy
from ..items import OpencourseItem, _DBConf, loadConf
import pymongo
from scrapy.http import Request
from scrapy.exceptions import CloseSpider

class CourseSpider(scrapy.Spider):
    name = "TUFTS"
    allowed_domains = ["tufts.edu"]
    start_urls = [
        'http://ocw.tufts.edu/CourseList',
    ]
    #每次开始执行抓取，都将之前的数据清空
    i = 1

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
        for i in range(1,81):
            yield Request(self.getRequestUrl(i),callback=self.parse_detail)

    def getRequestUrl(self,i):
        return 'http://ocw.tufts.edu/Course/' + str(i)


    def parse_detail(self, response):
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        if response.status == 200:
            sel = scrapy.Selector(response)
            item = OpencourseItem()
            div_main = sel.xpath("//div[@class='body']/table[1]/tr[1]/td[1]")
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

