# -*- coding=utf-8 -*-
from time import sleep

import requests
import scrapy
from scrapy.spiders import Spider
from ..items import ZhiWangItem, _DBConf
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
from .commonFn import *
from redis import Redis


class CourseSpider(Spider):
    name = "HaoDaXue"
    allowed_domains = ["cnmooc.org"]
    start_urls = [
        "http://www.cnmooc.org/portal/frontCourseIndex/course.mooc"
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=True, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.headers = {
            'accept': "*/*",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'content-length': "106",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'cookie': "moocvk=1393979b065c41c780d24ddb5e4e7e26; JSESSIONID=FF9921460AC765265E3A4C0930118498.tomcat-host1-1; moocsk=9f4c8b20716b489c9febc069e2d1aa60; userLocale=zh_CN; Hm_lvt_ed399044071fc36c6b711fa9d81c2d1c=1507600708,1507710535,1507722933; Hm_lpvt_ed399044071fc36c6b711fa9d81c2d1c=1507723675; BEC=f6c42c24d0c76e7acea242791ab87e34|1507723674|1507722932",
            'host': "www.cnmooc.org",
            'origin': "http://www.cnmooc.org",
            'pragma': "no-cache",
            'referer': "http://www.cnmooc.org/portal/frontCourseIndex/course.mooc",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'x-requested-with': "XMLHttpRequest",
        }

    def parse(self, response):
        url = "http://www.cnmooc.org/portal/ajaxCourseIndex.mooc"
        data = {
            "keyWord":"",
            "openFlag":0,
            "fromType":"",
            "learningMode":0,
            "certType":"",
            "languageId":"",
            "categoryId":"",
            "menuType":"course",
            "pageIndex":1
        }
        isGoon = True
        num = 1
        while(isGoon):
            data["pageIndex"] = num
            if num >= self.limit_count != 0:
                self.close(CourseSpider, "抓取完成")
                isGoon = False
                raise CloseSpider("已抓取完成")
            else:
                response = requests.request("POST",url=url,data=data,headers=self.headers)
                if response.status_code == 200:
                    html = BeautifulSoup(response.text,"lxml")
                    tagAs = html.find_all("a",{"class":"view-shadow link-course-detail"})
                    if len(tagAs) > 0:
                        for tagA in tagAs:
                            courseId = tagA.get("courseid")
                            courseOpenId = tagA.get("courseopenid")
                            if not courseId or not courseOpenId:
                                self.logger.debug("获取课程ID和课程OpenId")
                                continue
                            else:
                                #跳转课程详情页面
                                courseUrl = "http://www.cnmooc.org/portal/course/"+courseId+"/"+courseOpenId+".mooc"
                                Dresponse = requests.request("GET",courseUrl)
                                if Dresponse.status_code == 200:
                                    Dhtml = BeautifulSoup(Dresponse.text,"lxml")
                                    item = ZhiWangItem()
                                    item["title"] = Dhtml.find("h3",{"class":"view-title substr"}).text
                                    item["html"] = Dhtml.find("p",{"class":"para-row"}).text
                                    item["sourceType"] = "好大学"
                                    item["college"] = self.name
                                    item["hotValue"] = int(Dhtml.find("span",{"id":"favoriteNum"}).get("favoritenum"))
                                    item["downloadNum"] = item["hotValue"]
                                    item["url"] = Dresponse.url
                                    item["tags"] = ""
                                    item["cateTag"] = ""
                                    yield item
                                    sleep(1)
                                else:
                                    self.logger.debug("获取课程详情页面失败")
                        num += 1
                    else:
                        isGoon = False
                        self.logger.debug("页面上获取课程信息失败")
                else:
                    isGoon = False
                    self.logger.error("获取list页面失败")

