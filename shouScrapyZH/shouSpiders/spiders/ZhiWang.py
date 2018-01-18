# -*- coding=utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from ..items import ZhiWangItem, _DBConf
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
from .commonFn import *
from redis import Redis


class CourseSpider(Spider):
    name = "ZhiWang"
    allowed_domains = ["cnki.net"]
    start_urls = [
        'http://kns.cnki.net/kns/brief/brief.aspx?RecordsPerPage=50&QueryID=4&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=custommode&SortType=(FFD%2c%27RANK%27)+desc&PageName=ASP.brief_default_result_aspx&curpage='
    ]
    # 每次开始执行抓取，都将之前的数据清空
    i = 0
    DetailHost = 'http://kns.cnki.net/KCMS/detail/detail.aspx?'
    cookie = {'Ecp_ClientId':'4170914141501293278',
              'RsPerPage':'50',
              'cnkiUserKey':'4bcf35ba-7b24-69e1-d39f-a147753bba0a',
              'KNS_DisplayModel':'custommode@SCDB',
              'ASP.NET_SessionId':'e01taqdc52focwigjyyn1ur4',
              'Ecp_IpLoginFail':'171009101.226.164.165',
              'SID_kns':'123109',
              'SID_klogin':'125144',
              'SID_kredis':'125144',
              'SID_krsnew':'125131',
              'SID_crrs':'125131',
              'SID_kcms':"124108",
              'SID_knsdelivery':"125124",
              "DisplaySave":"0",
              'ASPSESSIONIDQCQTSTAT':'NKEPLDMAHFPBBJFACPBJPJKJ'}


    def __init__(self, storeConf=json.dumps(_DBConf), limit_count=0, trash_data=False, *a, **kw):
        # 获取数据库配置
        super().__init__(*a, **kw)
        initSpider(self,trash_data=trash_data,limit_count=limit_count,storeConf=storeConf)
        self.limit_count = limit_count
        self.r = Redis(db=1)

    def request(self,url,callback):
        request = scrapy.Request(url=url, callback=callback)
        request.cookies = self.cookie
        return request

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield self.request(url+"1#J_ORDER", self.parse_page)


    def parse_page(self,response):
        #获取总页数
        # print(self.start_urls[0]+str(1))
        # yield self.request(self.start_urls[0] + str(2),self.parse_item)
        sel = scrapy.Selector(response)
        span = sel.xpath("//*[@class='countPageMark']")
        spanText = span.xpath("text()").extract()
        if len(spanText) > 0:
            #说明找到了对应总页数的数据
            totalPages = int(spanText[0].split("/")[-1])
            #根据对应的page数，发起对应的页面请求
            for j in range(1,16):
                # self.r.lpush("ZHiWANG:Page",self.start_urls[0]+str(j)+"#J_ORDER")
                print(j)
                yield self.request(self.start_urls[0]+str(j)+"#J_ORDER",self.parse_item)
        else:
            checkCode = sel.xpath("//*[@id='CheckCode']")
            if(len(checkCode)>0):
                #表示出现了验证码验证,我自己请求验证码验证
                print("需要验证才能继续加载了")
            else:
                print("没有找到页面的总数,考虑可能是session失效，或者数据到了最后或者被Ban")


    def parse_item(self, response):
        btS = BeautifulSoup(response.body,'lxml')
        lis = btS.find_all("h3",{"class":"title_c"})
        if len(lis) > 0 :
            # db = pymongo.MongoClient("mongodb://127.0.0.1:27017").OpenCollege.zhiwang
            for h3 in lis:
                aHref = h3.find("a").get('href')
                if aHref:
                    #查询数据库，已经抓取的不抓
                    # if db.find({"url":self.DetailHost + aHref.split("?")[-1]}).count() == 0:
                    self.r.lpush("ZHiWANG:Detail",self.DetailHost + aHref.split("?")[-1])
                    self.i += 1
                    # yield self.request(self.DetailHost + aHref.split("?")[-1],self.parse_detail)
                    # else:
                    #     print("重复！")
                else:
                    pass
        else:
            print(response.url)
            print("table页面数据获取失败")

    def parse_detail(self,response):
        if self.i >= self.limit_count != 0:
            self.close(CourseSpider, "抓取完成")
            raise CloseSpider("已抓取完成")
        item = ZhiWangItem()
        html = BeautifulSoup(response.body,'lxml')
        description = html.find("span",{"id":"ChDivSummary"})
        if len(description) > 0:
            item["html"] = description.get_text()
            item["url"] = response.url
            item["title"] = html.find("title").get_text()
            item["sourceType"] = "知网"
            #关键词
            divInfo = html.find("div",{"class":"wxBaseinfo"})
            tempA = []
            tempCT = ""
            tempDN = 0
            tempHV = 0
            if divInfo:
                infoPs = divInfo.find_all("p")
                tagsP = infoPs[1]
                tagsA = tagsP.find_all("a")
                for ta in tagsA:
                    tempA.append(ta.get_text())
                #在获取cateTag
                tempCT = infoPs[2].get_text() if infoPs[2] else ""
                #获取下载等信息
                totalDiv = divInfo.find("div",{"class":"total"})
                if totalDiv:
                    tempDN = totalDiv.find_all("b")[0].get_text()
                tempHV = divInfo.find("span",{"id":"HotValue"}).get_text()
            item["tags"] = tempA
            #其他信息
            item["downloadNum"] = tempDN
            item["hotValue"] = tempHV
            item["cateTag"] = tempCT
            yield item
            self.i += 1
        else:
            self.log("获取详细信息失败")
