# -*- coding=utf-8 -*-
# -*- coding: utf-8 -*-
import json
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from ..items import ZhiWangItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from .commonFn import *
from bs4 import BeautifulSoup


class CourseSpider(CrawlSpider):
    name = "HaoKeWang"
    allowed_domains = ["class.cn"]
    start_urls = [
        "http://www.class.cn/search/search_do?index=class"
    ]
    rules = [
        Rule(LinkExtractor(allow='/search/search_do',restrict_xpaths='//*[@id="pagenav"]'),
             callback='parse_page',
             follow=True),
        Rule(LinkExtractor(allow='http://www.class.cn/course/course_detail',restrict_xpaths='//div[@class="search_result_contents"]'),
             callback='parse_item',
             follow=False)
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'cookie': "UM_distinctid=15f56992e679c8-086c7fe32b783b-31657c00-1fa400-15f56992e687ab; PHPSESSID=lq8vsrra9o1npt4t5hvbajav87; lastvisit=1509349558031; topAdFlag=true; CNZZDATA5333700=cnzz_eid%3D1533558404-1508983076-%26ntime%3D1509347792; Hm_lvt_5907fb81dedac17075ae6def57dc2989=1508986401,1509349558; Hm_lpvt_5907fb81dedac17075ae6def57dc2989=1509349793; eol_avd_got=150934955803123; _va_id=aa421446e109c254.1508986400.2.1509349798.1509349558.; _va_ses=*",
            'host': "www.class.cn",
            'pragma': "no-cache",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'postman-token': "23fb2eed-d445-d1b5-d780-50add13528b6",
            'content-type': "application/x-www-form-urlencoded"
        }

    def parse_item(self,response):
        #对页面详情做处理
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider,"抓取完成")
            raise CloseSpider("已抓取完成")
        detailSoup = BeautifulSoup(response.text,"lxml")
        courseInfo = detailSoup.find("p",{"class":"intro_more"})
        if not courseInfo:
            print("没有找到信息")
            pass
        else:
            item = ZhiWangItem()
            item['title'] = detailSoup.find("div",{"class":"fl intro_content posr"}).find("h1").text
            item['url'] = response.url
            item['hotValue'] = detailSoup.find("div",{"class":"course_message marr10"}).find("h2").text.split("共")[1].split("条")[0]
            item['downloadNum'] = detailSoup.find("p",{"class":"course_raty marall0"}).find("em",{"class":"red"}).text
            item['sourceType'] = self.name
            item['college'] = courseInfo.find_all("span")[1].find("a").text
            item['cateTag'] = ""
            item['tags'] = []
            try:
                cateSpan = courseInfo.find_all("span")[3].find_all("a")
            except Exception as e:
                cateSpan = courseInfo.find_all("span")[2].find_all("a")
            for cate in cateSpan:
                item['tags'].append(cate.text)
            #获取详情
            description = ""
            try:
                descriptionDiv = detailSoup.find("section",{"class":"info_readmore"}).find_all("p")
                for p in descriptionDiv:
                    description += p.text
            except Exception as e:
                description = ""
            item['html'] = description
            yield item
            # print(item)
            self.i += 1

    def parse_page(self,response):
        #对列表页做处理
        listSoup = BeautifulSoup(response.text,"lxml")
        hrefs = listSoup.find_all("a",{"class":"search_result_img"})
        if len(hrefs) > 0:
            for href in hrefs:
                yield Request(href.get("href"),callback=self.parse_item)