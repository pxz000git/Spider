# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhiWangItem(scrapy.Item):
    _id = scrapy.Field()
    html = scrapy.Field(iterable=str)
    sourceType = scrapy.Field(iterable=str)
    url = scrapy.Field(iterable=str)
    title = scrapy.Field(iterable=str)
    tags = scrapy.Field(iterable=list)
    downloadNum = scrapy.Field(iterable=int)
    hotValue = scrapy.Field(iterable=int)
    cateTag = scrapy.Field(iterable=str)
    college = scrapy.Field(iterable=str)


class DrugItem(scrapy.Item):
    _id = scrapy.Field()
    drug_name = scrapy.Field()
    drug_en_name = scrapy.Field()
    drug_license_number = scrapy.Field()
    drug_base_code = scrapy.Field()
    drug_base_code_notice = scrapy.Field()
    drug_factory = scrapy.Field()
    drug_factory_address = scrapy.Field()
    drug_gui_ge = scrapy.Field()
    drug_ji_xin = scrapy.Field()
    drug_access_date = scrapy.Field()
    drug_type = scrapy.Field()
    drug_yi_bao_type = scrapy.Field()
    drug_instruction = scrapy.Field()



class KeywordItem(ZhiWangItem):
    keyword = scrapy.Field(iterable=str)


class TimeItem(ZhiWangItem):
    startTime = scrapy.Field(iterable=str)


#将数据库的默认配置写在这里
_DBConf = dict(
    DBTYPE="mongodb",
    MONGODB_URI="mongodb://175.102.18.112:27018/",
    MONGODB_DATABASE="OSOpenCollege",
    MONGODB_COLLECTION="ICDE"
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