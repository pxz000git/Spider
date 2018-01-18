# -*- coding=utf-8 -*-
from time import sleep

import re
import requests
from scrapy.spiders import Spider
from ..items import ZhiWangItem, _DBConf
from bson import ObjectId
from .commonFn import initSpider
import json
from redis import Redis
import threading

threadCount = 0
isGoon = True
myLock = threading.RLock()


class CourseSpider(Spider):
    name = "WangYiYun"
    allowed_domains = ["163.com"]
    start_urls = [
        'https://c.open.163.com/search/search.htm?query=&enc=%E2%84%A2#/search/course'
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0

    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        self.collection = initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.r = Redis(db=1)
        self.headers = {
            'host': "c.open.163.com",
            'connection': "keep-alive",
            'content-length': "207",
            'pragma': "no-cache",
            'cache-control': "no-cache",
            'origin': "https://c.open.163.com",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'content-type': "text/plain",
            'accept': "*/*",
            'referer': "https://c.open.163.com/search/search.htm?query=&enc=%E2%84%A2",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            'cookie': "mail_psc_fingerprint=b98d53b9a03092e94f93fa4faf3d26ef; _ntes_nnid=8d63a00e17eac68f6fe33653e8a7efb6,1487146966421; _ntes_nuid=8d63a00e17eac68f6fe33653e8a7efb6; NTES_CMT_USER_INFO=8025510%7C179564369%7Chttps%3A%2F%2Fsimg.ws.126.net%2Fe%2Fimg5.cache.netease.com%2Ftie%2Fimages%2Fyun%2Fphoto_default_62.png.39x39.100.jpg%7Cfalse%7CejMwNjIyMzU1OEAxNjMuY29t; usertrack=ZUcIhViti+ccr1dYA1tXAg==; vjuids=18755ba10.15c7c578b9f.0.dcbbfeeb062a4; __gads=ID=c545d00d56c36cd6:T=1496734732:S=ALNI_MbZ533W9YUyHHN3E63dZWTzLBvfTg; UM_distinctid=15c7c5cf423ac-0e2654bf69577-30657509-1fa400-15c7c5cf4251c8; __s_=1; _ga=GA1.2.235581014.1487768553; P_INFO=z306223558@163.com|1506678215|0|other|11&14|shh&1504370037&gbox-lushi#shh&null#10#0#0|131160&0||z306223558@163.com; Province=021; City=021; vjlast=1496734731.1507729099.11; ne_analysis_trace_id=1507729099230; vinfo_n_f_l_n3=7822ab8d01b9ca88.1.12.1496735087228.1507609696703.1507729099459; s_n_f_l_n3=7822ab8d01b9ca881507729099235; __utma=187553192.235581014.1487768553.1501145566.1507729100.2; __utmb=187553192.3.10.1507729100; __utmc=187553192; __utmz=187553192.1507729100.2.2.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/ted/; __oc_uuid=71efe830-ae89-11e7-8920-6f292c2ba499; __utma=130438109.235581014.1487768553.1507729117.1507729117.1; __utmb=130438109.2.10.1507729117; __utmc=130438109; __utmz=130438109.1507729117.1.1.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/ocw/"
        }


    def requestsUrl(self,num):
        url = "https://c.open.163.com/dwr/call/plaincall/OpenSearchBean.searchCourse.dwr"
        global threadCount,isGoon
        myLock.acquire()
        print(u"Start Requests："+str(num))
        payload = "callCount=1\nscriptSessionId=${scriptSessionId}190\nhttpSessionId=\nc0-scriptName=OpenSearchBean\nc0-methodName=searchCourse\nc0-id=0\nc0-param0=string:\nc0-param1=number:"+str(num)+"\nc0-param2=number:50\nbatchId=1507729229005"
        myLock.release()
        try:
            response = requests.request("POST", url, headers=self.headers, data=payload)
            if response.status_code == 200:
                #列表页请求成功，开始分析数据
                pattern = r"\.category=\"(.*?)\".*\.courseUrl=\"(.*?)\".*\.description=\"(.*?)\";.*\.instructor=\"(.*?)\".*\.movieCount=(.*?);.*\.school=\"(.*?)\".*\.startTime=(.*?);.*\.subject=\"(.*?)\".*\.tags=\"(.*?)\".*\.title=\"(.*?)\""
                string = response.text
                courseLists = re.findall(pattern=pattern,string=string)
                for course in courseLists:
                    if self.checkInData(course[1]) == 0:
                        item = ZhiWangItem()
                        item["title"] = eval("u" + "\'" + course[9] + "\'")
                        item["html"] = eval("u" + "\'" + course[2] + "\'")
                        item["sourceType"] = "WangYiYun"
                        item["tags"] = eval("u" + "\'" + course[8] + "\'").split(",")
                        item["cateTag"] = eval("u" + "\'" + course[7] + "\'")
                        item["url"] = course[1]
                        item["downloadNum"] = 0
                        item["hotValue"] = 0
                        if course[6] != "null":
                            item["startTime"] = course[6]
                        #获取完成，返回item
                        self.saveToMongodb(item)
                    else:
                        print("重复")
                #抓取完成，count--
                print(str(num) + "page scrapyed success， count--")
                threadCount = threadCount -1
                sleep(2)
            else:
                #请求失败的考虑重新加入到队列中
                print(u"Requests Field")
                print(response.text)
                print(response.status_code)
                threadCount = threadCount - 1
        except Exception as e:
            print(str(e))
            threadCount = threadCount - 1
            print(u"Requests Error")

    def parse(self,response):
        global threadCount,isGoon
        num = 1
        while(isGoon):
            if num > 500:
                isGoon = False
            else:
                if threadCount < 4:
                    t = threading.Thread(target=self.requestsUrl, name = "Name: "+str(num),args=(num,))
                    threadCount += 1
                    num += 1
                    t.start()

    def filterStr(self,str):
        r = u'[0-9!"#$%&\'()；\ （）*+-/:;<=>?@，\\ \\ \\r\\t\\n\\：。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        return re.sub(r, '', str)

    def saveToMongodb(self,item):
        item["_id"] = ObjectId()
        self.collection.insert(item)

    def checkInData(self,course):
        return self.collection.count({"url":course})