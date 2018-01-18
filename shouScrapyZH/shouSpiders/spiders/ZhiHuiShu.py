# -*- coding=utf-8 -*-
from time import sleep

import requests
import scrapy
from scrapy.spiders import Spider
from ..items import ZhiWangItem, _DBConf
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
from .commonFn import initSpider
import json
from redis import Redis


class CourseSpider(Spider):
    name = "ZhiHuiShu"
    allowed_domains = ["shuxiavip.com"]
    start_urls = [
        'http://www.shuxiavip.com/course.html'
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=True, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.r = Redis(db=1)
        self.cookie = {
            'cookie': "SERVERID=958b97eacbe3c49360ace2dfc0bd31b4|1507717368|1507713772",
        }
        self.headers = {
            'host': "appmember.zhihuishu.com",
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cookie': "SERVERID=958b97eacbe3c49360ace2dfc0bd31b4|1507717368|1507713772",
            'connection': "keep-alive",
            'accept': "*/*",
            'user-agent': "WisdomMemberStore/3.1.4 (iPhone; iOS 10.3.3; Scale/3.00)",
            'accept-language': "zh-Hans-CN;q=1",
            'content-length': "46",
            'accept-encoding': "gzip, deflate",
            'cache-control': "no-cache"
        }

    def parse(self, response):
        #请求到这里就与scrapy没有关系了我需要自己再构造App的接口请求
        if response.status == 200:
            isGoon = True
            num = 1
            url = "https://appmember.zhihuishu.com/appmember/member/course/select/filterAllCourse"
            self.session = requests.session()
            while(isGoon):
                data = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"attributeId\"\r\n\r\n-1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"pageNum\"\r\n\r\n'+str(num)+'\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"pageSize\"\r\n\r\n20\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"sortBy\"\r\n\r\n-1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'
                response = self.session.request("POST", url, data=data, headers=self.headers,verify=False)
                if response.status_code == 200:
                    #请求成功,查看是否是有返回的
                    reData = json.loads(response.text)
                    if "status" in reData and reData['status'] == "200":
                        #有数据返回的就可以继续了
                        courseDetailUrl = 'https://appmember.zhihuishu.com/appmember/member/course/getCourseDetailInfo'
                        if not reData["rt"]:
                            isGoon = False
                            continue
                        for course in reData["rt"]:
                            #然后就是进行课程的详细信息请求
                            courseDetailData = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"courseId\"\r\n\r\n'+str(course["courseId"])+'\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"recruitId\"\r\n\r\n'+str(course["recruitId"])+'\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"userId\"\r\n\r\n168597861\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'
                            courseRe = self.session.request("POST", courseDetailUrl, data=courseDetailData, headers=self.headers,verify=False)
                            if courseRe.status_code == 200:
                                courseReData = json.loads(courseRe.text)
                                if "status" in courseReData and courseReData["status"] == "200":
                                    courseInfo = courseReData["rt"]["teacherInfo"]
                                    item = ZhiWangItem()
                                    des = BeautifulSoup(courseInfo["introduction"],"lxml").get_text().replace(u"\\xa0","")
                                    back = BeautifulSoup(courseInfo["courseBackground"]).get_text().replace(u"\\xa0","")
                                    item["html"] = des + " " + back
                                    item["sourceType"] = "智慧树"
                                    item["url"] = "POST: " + courseDetailUrl + "  DATA: " + str({"courseId":course["courseId"],"recruitId":course['recruitId'],"userId":"168597861"})
                                    item["title"] = courseInfo["name"]
                                    item["tags"] = "",
                                    item["downloadNum"] = int(course["studentCount"])
                                    item["hotValue"] = int(course["studentCount"])
                                    item["cateTag"] = ""
                                    item["college"] = self.name
                                    yield item
                                    sleep(1)
                                else:
                                    self.logger.debug(u"课程详情失败，原因为：" + courseReData["msg"])
                            else:
                                self.logger.debug(u"请求课程详情失败")
                        num += 1
                    else:
                        self.logger.debug(u"课程列表解析失败，原因为：" + reData["msg"])
                else:
                    print(response.text)
                    self.logger.debug(u"课程列表请求失败")
                    isGoon = False
