# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from ..items import OpencourseItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
import pymongo
from scrapy.http import Request
from scrapy.exceptions import CloseSpider

class CourseSpider(scrapy.Spider):
    name = "EDX"
    allowed_domains = ["edx.org"]
    start_urls = [
        'https://www.edx.org/api/v1/catalog/search?page=1&page_size=10&partner=edx&content_type[]=courserun&content_type[]=program&featured_course_ids=course-v1%3APennX+SD1x+2T2017%2Ccourse-v1%3AUQx+IELTSx+3T2016%2Ccourse-v1%3AMicrosoft+DAT101x+2T2017%2Ccourse-v1%3AUCSanDiegoX+CSE165x+2T2017%2Ccourse-v1%3AGTx+CS1301x+1T2017%2Ccourse-v1%3AMicrosoft+DAT201x+2T2017&featured_programs_uuids=865bbad4-6643-4d59-85d3-936cf3a7acf4%2Cf5448140-88fc-451c-82cf-976504bdfa8d%2C482dee71-e4b9-4b42-a47b-3e16bb69e8f2%2C98b7344e-cd44-4a99-9542-09dfdb11d31b%2Ca015ce08-a727-46c8-92d1-679b23338bc1%2C77d865f3-456a-4ea6-9e0d-65529e8864d6'
    ]
    #每次开始执行抓取，都将之前的数据清空
    i = 1
    MAIN_HOST = 'https://www.edx.org'

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
        courseNumber = courseData['objects']['count']
        pagesCount = int(int(courseNumber)/10 + 1)
        self.logger.info("总数是：" + str(pagesCount))
        for i in range(1,pagesCount):
            yield Request(self.getRequestUrl(i),callback=self.parse_course)

    def getRequestUrl(self,i):
        return 'https://www.edx.org/api/v1/catalog/search?page=' + str(i) + '&page_size=10&partner=edx&content_type[]=courserun&content_type[]=program&featured_course_ids=course-v1%3APennX+SD1x+2T2017%2Ccourse-v1%3AUQx+IELTSx+3T2016%2Ccourse-v1%3AMicrosoft+DAT101x+2T2017%2Ccourse-v1%3AUCSanDiegoX+CSE165x+2T2017%2Ccourse-v1%3AGTx+CS1301x+1T2017%2Ccourse-v1%3AMicrosoft+DAT201x+2T2017&featured_programs_uuids=865bbad4-6643-4d59-85d3-936cf3a7acf4%2Cf5448140-88fc-451c-82cf-976504bdfa8d%2C482dee71-e4b9-4b42-a47b-3e16bb69e8f2%2C98b7344e-cd44-4a99-9542-09dfdb11d31b%2Ca015ce08-a727-46c8-92d1-679b23338bc1%2C77d865f3-456a-4ea6-9e0d-65529e8864d6'

    def parse_course(self, response):
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        courseList = json.loads(response.body)['objects']['results']
        for course in courseList:
            item = OpencourseItem()
            if 'authoring_organizations' in course:
                organization =  course['authoring_organizations'][0]
                if 'description' in organization:
                    item['html'] = course['authoring_organizations'][0]["description"]
                else:
                    item['html'] = course['subtitle']
                item['college'] = "EDX_" + course['authoring_organizations'][0]['name']
            else:
                item['html'] = course['full_description']
                item['college'] = "EDX_base"
            item['title'] = course['title']
            item['catchUrl'] = course['marketing_url']

            self.i += 1
            yield item


