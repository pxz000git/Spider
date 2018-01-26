# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class TencenpositionSpider(scrapy.Spider):
    # 爬虫名
    name = 'tencenPosition'
    allowed_domains = ['tencent.com']
    url = "http://hr.tencent.com/position.php?&start="
    offset = 0
    # 第一次处理的url(只处理一次)
    start_urls = [
        url + str(offset),
    ]

    def parse(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):

            # 初始化模型对象
            item = TencentItem()
            # xpath返回的是一个选择器的列表，
            # 我们通过.extract()方法把选择器转化成unicode字符串,
            # 然后再取出这列表里的第一个字符串（）唯一的一个字符串

            # 职位名称
            item['name'] = each.xpath("./td[1]/a/text()").extract()[0]
            print type(item['name'])
            print item['name']
            print type(each.xpath("./td[1]/a/text()"))
            # 详情连接
            item['link'] = each.xpath("./td[1]/a/@href").extract()[0]
            # 职位类别
            item['type'] = each.xpath("./td[2]/text()").extract()[0]
            # 招聘人数
            item['num'] = each.xpath("./td[3]/text()").extract()[0]
            # 工作地点
            item['location'] = each.xpath("./td[4]/text()").extract()[0]
            # 发布时间
            item['time'] = each.xpath("./td[5]/text()").extract()[0]

            # 将数据交给管道文件处理
            yield item

        if self.offset < 20:
            self.offset += 10
        else:
            raise "停止工作..."

        # offset自增10
        # 每次处理完一页 的数据之后，重新发送下一页的页面请求，同时拼接新的url，
        # 并调用回调函数self.parse()处理Request
        # 多个请求，将请求重新发送为调度器入队列，出队列，交给下载器下载
        # 第一个参数url,第二个参数callback
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
