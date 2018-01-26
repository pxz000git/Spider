#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author:pxz


import scrapy
from mySpider.items import ItcastItem

# 创建一个爬虫类

class ItcastSpider(scrapy.Spider):
    # 执行的爬虫名
    name = "itcast"
    # 允许爬虫作用的范围
    allowd_domains = ["http://www.itcast.cn/"]
    # 爬虫其实的url
    # start_urls = ["http://www.itcast.cn/channel/teacher.shtml#,..."]
    start_urls = ["http://www.itcast.cn/channel/teacher.shtml#"]
    # 处理响应文件
    def parse(self, response):
        # with open('teacher2.html','w') as f:
            # 注意是body,不是read
            # f.write(response.body)
        # 所有老师的信息集合
        # teacherItem = []
        # 通过scrapy自带的xpath匹配出所有老师的根节点
        # 遍历根节点集合
        for each in response.xpath("//div[@class='li_txt']"):

            # item 对象用来保存数据的
            item = ItcastItem()
            # 不加.extract()结果为xpath匹配的对象列表
            # extract()将匹配出来的结果转换成unicode字符串
            # name
            name = each.xpath("./h3/text()").extract()
            # title
            title = each.xpath("./h4/text()").extract()
            # info
            info = each.xpath("./p/text()").extract()

            # print name[0]
            # print title[0]
            # print info[0]

            # item['name'] = name[0].encode('gbk')
            item['name'] = name[0]
            item['title'] = title[0]
            item['info'] = info[0]
            # teacherItem.append(item)

            yield item
        # return teacherItem














