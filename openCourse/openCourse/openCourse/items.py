# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OpencourseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    html = scrapy.Field(iterable=str)
    college = scrapy.Field(iterable=str)
    catchUrl = scrapy.Field(iterable=str)
    title = scrapy.Field(iterable=str)

class ZWItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    html = scrapy.Field(iterable=str)
    title = scrapy.Field(iterable=str)

#将数据库的默认配置写在这里
_DBConf = dict(
    DBTYPE="mongodb",
    MONGODB_URI="mongodb://127.0.0.1:27017/",
    MONGODB_DATABASE="openCourse",
    MONGODB_COLLECTION="college_html"
)
#写入一个覆盖的参数函数

def loadConf(conf, confBase, type="cover"):
    """通用的2个字典属性覆盖的方法"""
    baseKeys = confBase.keys()
    loadKeys = conf.keys()
    for key in loadKeys:
        if type == 'cover':
            confBase[key] = conf[key]
        if type == "append":
            confBase[key] = conf[key]
        if type == "short":
            if key in baseKeys:
                del confBase[key]
    return confBase