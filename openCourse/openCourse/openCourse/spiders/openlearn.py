# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from ..items import OpencourseItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
import pymongo
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
import html2text

class CourseSpider(CrawlSpider):
    name = "OpenLearn"
    allowed_domains = ["open.edu"]
    start_urls = (
        'http://www.open.edu/openlearn/free-courses/full-catalogue',
    )
    rules = [
        Rule(LinkExtractor(allow='/openlearn/(.*?)',
                           restrict_xpaths='//div[@class="dropdown-box"]'),
             callback='parse_item',
             follow=False)
    ]
    #每次开始执行抓取，都将之前的数据清空
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


    def parse_item(self, response):
        sel = scrapy.Selector(response)
        div_main = sel.xpath("//div[@id='pagenid']/text()").extract()
        if len(div_main) > 0:
            url = 'http://www.open.edu/openlearn/content_api/html_content/block.json?node='+ div_main[0] +'&nid='+div_main[0]+'&element=ocw_learning_outcomes'
            yield Request(url=url,callback=self.parse_ajax,meta={"courseTitle":sel.xpath("//title/text()").extract()[0],"courseUrl":response.url})

    def parse_ajax(self, response):
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        item = OpencourseItem()
        item['catchUrl'] = response.meta['courseUrl']
        item['title'] = response.meta['courseTitle']
        item['html'] = html2text.html2text(json.loads(response.body)['content'])
        item['college'] = 'OpenLearn'
        self.i += 1
        yield item