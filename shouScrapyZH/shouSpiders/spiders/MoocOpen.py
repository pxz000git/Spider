# -*- coding=utf-8 -*-
# -*- coding: utf-8 -*-
import json

import re
from time import sleep

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider,Spider, Rule
from ..items import ZhiWangItem, _DBConf, loadConf
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from .commonFn import *
from bs4 import BeautifulSoup


class CourseSpider(Spider):
    name = "MoocOpen"
    allowed_domains = ["icourses.cn"]
    start_urls = [
        "http://www.icourses.cn/dirQueryVCourse.action"
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count


    def parse(self,response):
        url = "http://www.icourses.cn/dirVCoursePage.action"
        urlProfix = "http://www.icourses.cn/"
        isGoon = True
        num = 1
        headers = {
            'accept': "text/html, */*; q=0.01",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'content-length': "138",
            'content-type': "application/x-www-form-urlencoded",
            'cookie': "icoursesSymbol=wKg3KFneH1B3cyKZH2IMAg==; TJ_VISIT=1509330666088; route=e463d8a73b281261355472cb8f8581d3; JSESSIONID=30DD9CAA7966FCE0AE9D10F483A068E9.sns81-4; Hm_lvt_787dbcb72bb32d4789a985fd6cd53a46=1508997260,1508997698,1509000382,1509330668; Hm_lpvt_787dbcb72bb32d4789a985fd6cd53a46=1509330750; TJ_PVT=1509330749956",
            'host': "www.icourses.cn",
            'origin': "http://www.icourses.cn",
            'pragma': "no-cache",
            'referer': "http://www.icourses.cn/dirQueryVCourse.action",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'x-requested-with': "XMLHttpRequest",
            'postman-token': "bfca7cc2-3f03-dcbc-b8c9-743ab4abd8c6"
        }
        while(isGoon and num < 101):
            print(num)
            payload = "videoCourse.title=&videoCourse.mainTeacherName=&videoCourse.organName=&videoCourse.organId=&mod=query&page.currentPage="+str(num)+"&page.pageSize=10"
            if self.limit_count != 0 and num > self.limit_count:
                self.close(CourseSpider, "抓取完成")
                isGoon = False
                raise CloseSpider("已抓取完成")
            else:
                res = requests.request("POST", url, data=payload, headers=headers)
                sleep(1)
                if res.status_code == 200:
                    html = BeautifulSoup(res.text,"lxml")
                    if num == 2:
                        print(res.text)
                    lis = html.find_all("li",{"class":"fl_li"})
                    if len(lis) > 0:
                        for li in lis:
                            item = ZhiWangItem()
                            item["title"] = li.find("p",{"class":"fl_til"}).text
                            descP = li.find_all("p",{"class":"fl_tex"})[1]
                            if descP.find("span"):
                                #这里需要做个详情请求,提取id
                                idStr = descP.find("span").get("onclick")
                                if idStr:
                                    id = re.findall(r"showVCourseDesc\(\'(.*?)\'",idStr)
                                    if len(id) > 0:
                                        id = id[0]
                                    else:
                                        id = ""
                                else:
                                    id = ""
                                if not id:
                                    item["html"] = descP.text
                                else:
                                    print("需要请求更详细的描述介绍,且ID获取到了")
                                    Durl = "http://www.icourses.cn/viewVCourseDesc.action"
                                    querystring = {"id":id}
                                    Dheaders = {
                                        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                                        'accept-encoding': "gzip, deflate",
                                        'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
                                        'cache-control': "no-cache",
                                        'connection': "keep-alive",
                                        'cookie': "icoursesSymbol=wKg3KFneH1B3cyKZH2IMAg==; TJ_VISIT=1509330666088; route=e463d8a73b281261355472cb8f8581d3; bdshare_firstime=1509330954725; JSESSIONID=822B56BFFDC38F5FF06CE1BA376589BD.sns81-4; TJ_PVT=1509344390658; Hm_lvt_787dbcb72bb32d4789a985fd6cd53a46=1508997260,1508997698,1509000382,1509330668; Hm_lpvt_787dbcb72bb32d4789a985fd6cd53a46=1509344391",
                                        'host': "www.icourses.cn",
                                        'pragma': "no-cache",
                                        'referer': "http://www.icourses.cn/dirQueryVCourse.action",
                                        'upgrade-insecure-requests': "1",
                                        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                                        'postman-token': "c7b4da89-f843-8167-5a86-76a486792f96"
                                    }
                                    descRes = requests.request("GET", Durl, params=querystring, headers = Dheaders)
                                    sleep(1)
                                    descHtml = BeautifulSoup(descRes.text,'lxml')
                                    item["html"] = descHtml.find("div",{"id":"Win"}).text
                                    item["html"] = descP.text
                            else:
                                item["html"] = descP.text
                            #其他属性
                            item["sourceType"] = self.name
                            infoP = li.find_all("p",{"class":"fl_tex"})[0]
                            item["college"] = infoP.find("a").text
                            item["hotValue"] = infoP.find("i",{"class":"ico_comment"}).text
                            item["downloadNum"] = infoP.find("i",{"class":"ico_player"}).text
                            item["url"] = urlProfix + li.find("p",{"class":"fl_til"}).find("a").get("href")
                            item["tags"] = []
                            item["cateTag"] = ""
                            yield item
                            # print(item)
                        num += 1
                    else:
                        isGoon = False
                        self.logger.debug("页面上获取课程信息失败")
                else:
                    print("请求失败了？")
                    isGoon = False
                    self.logger.error("获取list页面失败")


