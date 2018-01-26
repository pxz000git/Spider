# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class MyspiderPipeline(object):
#     def process_item(self, item, spider):
#         return item
import json


class ItcastPipeline(object):
    # 管道文件尅可以处理数据,也可以处理请求
    # __init__方法可选，作为类的初始化方法
    def __init__(self):
        # 创建一个文件
        self.filename = open("teacher.json", "w")

    # 该方法必须写，用来处理item数据
    def process_item(self, item, spider):
        print(type(item))
        # ensure_ascii=False，如果数据有中文（默认用ascii），这样就会用unicode编码
        jsontext = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.filename.write(jsontext.encode('utf-8'))
        # 一定要return
        return item

    # close_spider方法是可选的，结束时调用这个方法
    def close_spider(self, spider):
        self.filename.close()
