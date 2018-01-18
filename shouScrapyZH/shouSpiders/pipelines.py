# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from pymongo import MongoClient

class ShouspidersPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool


    def filterStr(self,str):
        r = u'[!"#$%&\'()；（）*+-/:;<=>?@，\\r\\t\\n\\：。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        return re.sub(r, ' ', str)

    @classmethod
    def from_settings(cls, settings):
        db_type = settings['DBTYPE']
        if db_type == 'mongodb':
            mongodb_uri = settings['MONGODB_URI']
            mongodb_collection = settings['MONGODB_COLLECTION']
            mongodb_database = settings['MONGODB_DATABASE']
            dbpool = MongoClient(mongodb_uri).get_database(mongodb_database).get_collection(mongodb_collection)
            return cls(dbpool)


    def process_item(self, item, spider):
        if self.dbpool:
            d = self.__do_insert__(self.dbpool, item, spider)
            if d:
                return item
            else:
                spider.log("Insert db failed!!!!!!!")
        else:
            spider.log("Db instence none!!!!!!!")
        return item

    def __do_insert__(self, conn, item, spider):
        try:
            if "html" in item:
                item["html"] = self.filterStr(item['html'])
                item["title"] = self.filterStr(item["title"])
            conn.insert(item)

            return True
        except Exception as e:
            print(e)
            spider.log("insert db error:" + str(e))
            return False