# -*- coding=utf-8 -*-
from time import sleep

import re
import requests
import scrapy
from scrapy.spiders import Spider
from ..items import ZhiWangItem, _DBConf
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
from .commonFn import *
from redis import Redis


class CourseSpider(Spider):
    name = "JSStudy"
    allowed_domains = ["js-study.cn"]
    start_urls = [
        "http://www.js-study.cn/course/front/courseResourcesAll.bsh?firstCategory=&interId=&jobId=&siteId=e089405566cf4a539106cb198ff14b94&order=0&searchContent="
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)

        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
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
        url = "http://www.js-study.cn/course/front/getCourseBySiteId.bsh"
        data = "search=&order=0&siteId=e089405566cf4a539106cb198ff14b94&categoryId=&currentPage="
        isGoon = True
        num = 1
        while(isGoon and num <= 36):
            if num >= self.limit_count != 0:
                self.close(CourseSpider, "抓取完成")
                isGoon = False
                raise CloseSpider("已抓取完成")
            else:
                response = requests.request("POST",url=url,data=data+str(num),headers=self.headers)
                if response.status_code == 200:
                    courseList = json.loads(response.text)
                    if courseList["status"] != "success":
                        continue
                    # print(courseList)
                    if len(courseList["course"]["results"]) > 0:
                        for course in courseList["course"]["results"]:
                            #课程详情链接：
                            detailUrl = "http://www.js-study.cn/course/front/courseResourcesDetail.bsh?courseId="+course["courseId"]+"&siteId=e089405566cf4a539106cb198ff14b94"
                            res = requests.request("GET",url=detailUrl)
                            html = res.text
                            htmlObj = BeautifulSoup(html,'lxml')
                            item = {}
                            courseDiv = htmlObj.find("div",{"class":"cd_top_txt"})
                            if courseDiv:
                                item["title"] = courseDiv.find("h4").get("title")
                                item["url"] = detailUrl
                                item["sourceType"] = self.name
                                item["college"] = self.name
                                item["hotValue"] = courseDiv.find("div",{"class":"cd_pj_fs"}).find("i").text.split("分")[0]
                                item["downloadNum"] = courseDiv.find("div",{"class":"cd_top_list"}).find_all("span")[3].find("i").text
                                item["startTime"] = re.findall(r":(.*?)~",courseDiv.find_all("span")[5].text)[0]
                                detailDiv = htmlObj.find("div",{"id":"chiose0"})
                                if detailDiv:
                                    p = detailDiv.find("div",{"class":"cd_zy"}).find("p")
                                    if p:
                                        description = p.text
                                    else:
                                        description = ""
                                    item["html"] = description
                                    item["tags"] = [detailDiv.find_all("li")[4].find("i").text]
                                    item["cateTag"] = detailDiv.find_all("li")[4].find("i").text
                                else:
                                    item["html"] = ""
                                    item["tags"] = []
                                    item["cateTag"] = ""
                                self.saveToMongodb(item)
                                # print(item)
                            else:
                                continue
                        num += 1
                    else:
                        isGoon = False
                        self.logger.debug("页面上获取课程信息失败")
                else:
                    isGoon = False
                    self.logger.error("获取list页面失败")

    def filterStr(self,str):
        r = u'[0-9!"#$%&\'()；\ （）*+-/:;<=>?@，\\ \\ \\r\\t\\n\\：。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        return re.sub(r, '', str)

    def saveToMongodb(self,item):
        from bson import ObjectId
        item["_id"] = ObjectId()
        item["html"] = self.filterStr(item["html"])
        item["title"] = self.filterStr(item["title"])
        self.collection.insert(item)