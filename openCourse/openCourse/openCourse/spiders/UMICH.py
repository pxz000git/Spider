# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from ..items import OpencourseItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
import pymongo
from scrapy.http import Request
from scrapy.exceptions import CloseSpider


class CourseSpider(CrawlSpider):
    name = "UMICH"
    allowed_domains = ["umich.edu"]
    start_urls = (
        'https://open.umich.edu/find/find-open-educational-resources',
    )
    rules = [
        Rule(LinkExtractor(allow='/find/open-educational-resources/(.*?)',
                           restrict_xpaths='//a[@class="menu__link"]'),
             callback='parse_list',
             follow=False),
        Rule(LinkExtractor(allow='/find/open-educational-resources/(.*?)/(.*?)',
                           restrict_xpaths='//a[@class="menu__link"]'),
             callback='parse_item',
             follow=False)
    ]
    MAIN_HOST = 'https://open.umich.edu'
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=True, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        trash_data = bool(trash_data)
        self.limit_count = int(limit_count)
        self.logger.info("开始爬虫：")
        self.logger.info("参数信息: " + storeConf)
        self.logger.info("额外参数: " + 'limit_count' + "  " + str(limit_count))
        self.logger.info("额外参数: " + 'trash_data' + "  " + str(trash_data))
        if trash_data:
            DBConf = loadConf(json.loads(storeConf),_DBConf)
            collection = pymongo.MongoClient(DBConf["MONGODB_URI"]).get_database(
                DBConf['MONGODB_DATABASE']).get_collection(DBConf['MONGODB_COLLECTION'])
            self.logger.info("正在清除数据：。。。\n")
            self.logger.info(collection.remove(dict(college=self.name)))

    def parse_list(self, response):
        if response.status == 200:
            sel = scrapy.Selector(response)
            courses = sel.xpath(
                "//div[@class='field field-name-field-unit-courses field-type-entityreference field-label-above']/article/@about").extract()
            for course in courses:
                yield Request(self.MAIN_HOST + course, callback=self.parse_item)

    def parse_item(self, response):
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        sel = scrapy.Selector(response)
        item = OpencourseItem()
        div_main = sel.xpath("//div[@id='overview']")
        if len(div_main) > 0:
            div_main = div_main[0]
            stringMain = div_main.xpath("string(.)").extract()
            if len(stringMain) > 0:
                stringMain = stringMain[0]
                item['html'] = stringMain
                item['title'] = sel.xpath("//title/text()").extract()[0]
                item['catchUrl'] = response.url
                item['college'] = self.name
                self.i += 1
                yield item
            else:
                self.logger.info("获取字符失败: " + str(self.i))
                pass
        else:
            self.logger.info("获取div失败: " + str(self.i) + "  url: " + response.url)
            pass
