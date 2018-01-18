# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from ..items import OpencourseItem, _DBConf,loadConf
from scrapy.linkextractors import LinkExtractor
import pymongo
from scrapy.http import Request
from scrapy.exceptions import CloseSpider


class CourseSpider(CrawlSpider):
    name = "AC"
    allowed_domains = ["www.gresham.ac.uk"]
    start_urls = (
        'https://www.gresham.ac.uk/watch/?files=audio',
        'https://www.gresham.ac.uk/watch/?files=video',
        'https://www.gresham.ac.uk/watch/?files=transcript'
    )
    rules = [
        Rule(LinkExtractor(allow='/lectures-and-events/(.*?)',
                           restrict_xpaths='//div[@class="row jumpoffs type-lectures"]'),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow='/watch/',
                           restrict_xpaths='//li[@class="next"]'),
             callback='parse_page',
             follow=True)
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

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

    def parse_page(self, response):
        if response.status == 200:
            print("当前页面url: " + response.url)
            # 然后降请求转发出去
            yield Request(response.url, callback=self.parse_item)
        else:
            print("页面请求失败")

    def parse_item(self, response):
        sel = scrapy.Selector(response)
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        item = OpencourseItem()
        div_main = sel.xpath("//*[@id='lectures']/div[3]/div/div[1]/div[1]")
        if len(div_main) > 0:
            div_main = div_main[0]
            stringMain = div_main.xpath("string(.)").extract()
            if len(stringMain) > 0:
                stringMain = stringMain[0]
                item['html'] = stringMain
                item['title'] = sel.xpath("//title/text()").extract()
                if len(item['title']) > 0:
                    item['title'] = item['title'][0]
                else:
                    item['title'] = "AC course"
                item['catchUrl'] = response.url
                item['college'] = self.name
                print(str(self.i) + "获取成功")
                yield item
            else:
                print("获取字符失败: " + str(self.i))
                pass
        else:
            print("获取div失败: " + str(self.i) + "  url: " + response.url)
            pass
        self.i += 1
