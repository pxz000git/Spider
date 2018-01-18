# -*- coding=utf-8 -*-
# from time import sleep
#

import requests
from bs4 import BeautifulSoup

url = "http://www.icourses.cn/dirVCoursePage.action"

payload = "videoCourse.title=&videoCourse.mainTeacherName=&videoCourse.organName=&videoCourse.organId=&mod=query&page.currentPage=1&page.pageSize=10"
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
num = 1
while(True):
    if num > 5:
        break
    response = requests.request("POST", url, data=payload, headers=headers)
    html = BeautifulSoup(response.text,"lxml")
    lis = html.find_all("li",{"class":"fl_li"})
    print(len(lis))
    num += 1


# # from .commonFn import initSpider,MyThread
# import json
# from redis import Redis
# import threading
#
# class ZhiWangItem(scrapy.Item):
#     _id = scrapy.Field()
#     html = scrapy.Field(iterable=str)
#     sourceType = scrapy.Field(iterable=str)
#     url = scrapy.Field(iterable=str)
#     title = scrapy.Field(iterable=str)
#     tags = scrapy.Field(iterable=list)
#     downloadNum = scrapy.Field(iterable=int)
#     hotValue = scrapy.Field(iterable=int)
#     cateTag = scrapy.Field(iterable=str)
#     college = scrapy.Field(iterable=str)
#
# threadCount = 0
# isGoon = True
# myLock = threading.RLock()
#
# headers = {
#     'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     'accept-encoding': "gzip, deflate",
#     'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
#     'cache-control': "no-cache",
#     'connection': "keep-alive",
#     'cookie': "Hm_lvt_f5e6bd27352a71a202024e821056162b=1507729920; Hm_lpvt_f5e6bd27352a71a202024e821056162b=1507729989; WFKS.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%5d%2c%22Data%22%3a%5b%5d%2c%22SessionId%22%3a%228e180150-d977-47e5-8435-96e76595ec9e%22%2c%22Sign%22%3a%22hi+authserv%22%7d%2c%22LastUpdate%22%3a%222017-10-11T13%3a59%3a36Z%22%2c%22TicketSign%22%3a%22uH%2bEBqcg0n1NXO48V9NQPg%3d%3d%22%7d",
#     'host': "s.wanfangdata.com.cn",
#     'upgrade-insecure-requests': "1",
#     'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
# }
#
#
# def requestsUrl(num):
#     global threadCount,isGoon
#     myLock.acquire()
#     print("开始请求："+str(num))
#     querystring = {"q":"成人教育","f":"top","p":str(num)}
#     myLock.release()
#     try:
#         sleep(2)
#         myLock.acquire()
#         print("现在执行的是："+ str(num))
#         threadCount -= 1
#         myLock.release()
#     except Exception as e:
#         print(str(e))
#         threadCount -= 1
#         print("请求错误")
#
# def parse():
#     url = "http://s.wanfangdata.com.cn/Paper.aspx"
#     num = 1
#     global threadCount,isGoon
#     while(isGoon):
#         if num > 50:
#             isGoon = False
#         if threadCount < 4:
#             t = threading.Thread(target=requestsUrl, name = "Name: "+str(num),args=(num,))
#             threadCount += 1
#             num += 1
#             t.start()
#
# def doRequests(url,querystring):
#     global threadCount
#     response = requests.request("GET", url, headers=headers, params=querystring,timeout=20)
#     if response.status_code == 200:
#         html = BeautifulSoup(response.content,'lxml')
#         recordItems = html.find_all("div",{"class":"record-item"})
#         if len(recordItems) > 0:
#             for item in recordItems:
#                 #解析数据,请求详
#                 try:
#                     res = requests.request("GET",item.find("a",{"class":"title"}).get("href"),timeout=20)
#                     if res.status_code == 200:
#                         Dhtml = BeautifulSoup(res.text,'lxml')
#                         baseInfo = Dhtml.find("div",{"class":"section-baseinfo"})
#                         ScItem = ZhiWangItem()
#                         ScItem["sourceType"] = "万方"
#                         ScItem["college"] = "WanFang"
#                         ScItem["hotValue"] = 0
#                         ScItem["downloadNum"] = 0
#                         if baseInfo:
#                             ScItem["title"] = baseInfo.find("h1").text
#                             ScItem["html"] = baseInfo.find("div",{"class":"text"}).text
#                             ScItem["url"] = res.url
#                         else:
#                             continue
#                         filedInfo = Dhtml.find("div",{"class":"fixed-width baseinfo-feild"})
#                         if filedInfo:
#                             tagsA = filedInfo.find("div",{"class":"row row-keyword"}).find_all("a")
#                             tempTag = []
#                             for tag in tagsA:
#                                 if not tag:
#                                     tempTag.append(tag.text)
#                             ScItem["tags"] = tempTag
#                             ScItem["cateTag"] = ""
#                         else:
#                             continue
#                         #获取完成，返回item
#                         print(ScItem)
#                     else:
#                         #请求详情失败，直接跳过
#                         print("详情请求失败了")
#                         continue
#                 except Exception as e:
#                     print("详情解析错误，跳过该请求。 " + str(e))
#                     continue
#             #请求完成了
#             print("详情请求完了，count减一")
#             threadCount -= 1
#         else:
#             #获取列表失败了
#             print("列表长度为0")
#             threadCount -= 1
#     else:
#         #请求失败的考虑重新加入到队列中
#         print("请求失败")
#         threadCount -= 1
#
# parse()

# def getProxy():
#     response = requests.get("http://127.0.0.1:5010/get")
#     return response.text
#
# url = "http://ip.chinaz.com/"
# httpProxy = "http://" + getProxy()
# print(httpProxy)
# proxies = { "http": httpProxy}
# res = requests.get(url,proxies=proxies)
# res.encoding = "utf-8"
# html = BeautifulSoup(res.text,"lxml")
# dds = html.find_all("dd",{"class":"fz24"})
# print(dds)



# pattern = r"\.category=\"(.*?)\".*\.courseUrl=\"(.*?)\".*\.description=\"(.*?)\".*\.instructor=\"(.*?)\".*\.movieCount=(.*?);.*\.school=\"(.*?)\".*\.startTime=(.*?);.*\.subject=\"(.*?)\".*\.tags=\"(.*?)\".*\.title=\"(.*?)\""
# string = """//#DWR-INSERT
# //#DWR-REPLY
# var s0={};var s1=[];var s2={};var s3={};var s4={};var s5={};var s6={};var s7={};var s8={};var s9={};var s10={};var s11={};var s12={};var s13={};var s14={};var s15={};var s16={};var s17={};var s18={};var s19={};var s20={};var s21={};s0.limit=20;s0.offset=40;s0.pageIndex=3;s0.pageSize=20;s0.totleCount=7763;s0.totlePageCount=389;
# s1[0]=s2;s1[1]=s3;s1[2]=s4;s1[3]=s5;s1[4]=s6;s1[5]=s7;s1[6]=s8;s1[7]=s9;s1[8]=s10;s1[9]=s11;s1[10]=s12;s1[11]=s13;s1[12]=s14;s1[13]=s15;s1[14]=s16;s1[15]=s17;s1[16]=s18;s1[17]=s19;s1[18]=s20;s1[19]=s21;
# s2.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/c/d/ccd1277ad3c84b3d9049c3be6b58d7cd.jpg";s2.category="\u5176\u4ED6";s2.courseId="MCOD6VJ36";s2.courseType=10;s2.courseUrl="http://open.163.com/movie/2017/7/I/1/MCOD6VJ36_MCOD73KI1.html";s2.description="\u9752\u5A92\u8BA1\u5212\u662F\u7F51\u6613\u65B0\u95FB\u9488\u5BF9\u5927\u5B66\u751F\u8BBE\u7ACB\u7684\u514D\u8D39\u81EA\u5A92\u4F53\u57F9\u8BAD\u9879\u76EE\u3002\u7F51\u6613\u4E3B\u7F16\u548C\u4E1A\u5185\u5927\u5496\u624B\u628A\u624B\u5E26\u4F60\u5B9E\u73B010\u4E07+\uFF01";s2.instructor="\u65B0\u95FB\u5B66\u9662";s2.movieCount=30;s2.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/3/c/0c2079919dbb4a38911503b7abe8093c.jpg_180x100x1x95.jpg";s2.school="\u7F51\u6613\u65B0\u95FB\u5B66\u9662";s2.startTime=null;s2.subject="\u5A92\u4F53,\u6280\u80FD,\u4E92\u8054\u7F51";s2.tags="\u7F51\u6613\u65B0\u95FB\u5B66\u9662,\u81EA\u5A92\u4F53\u57F9\u8BAD,\u9752\u5A92\u8BA1\u5212,";s2.title="\u65B0\u95FB\u5B66\u9662\u2014\u7F51\u6613\u9752\u5A92\u8BA1\u5212";
# s3.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/f/0/e8b416628921421f8f43cc4e54bfd5f0.jpg";s3.category="\u5176\u4ED6";s3.courseId="MCOSIVVHQ";s3.courseType=10;s3.courseUrl="http://open.163.com/movie/2017/7/D/F/MCOSIVVHQ_MCOSJ1JDF.html";s3.description="\u51E0\u767E\u4E07\u5E74\u524D\u53E4\u733F\u4E0D\u8FC7\u5904\u4E8E\u98DF\u7269\u94FE\u4E2D\u7AEF\u3002\u6CA1\u6709\u5F3A\u58EE\u7684\u4F53\u9B44\u548C\u950B\u5229\u7684\u722A\u7259\uFF0C\u4EBA\u7C7B\u662F\u5982\u4F55\u8FBE\u5230\u98DF\u7269\u94FE\u9876\u7AEF\u7684\uFF1F\uFF08\u611F\u8C22\u963F\u5C14\u6CD5\u5C0F\u5206\u961F\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s3.instructor="\u7F8E\u56FD";s3.movieCount=1;s3.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/0/3/356137ca51ed41fa9173a79572ca4e03.jpg_180x100x1x95.jpg";s3.school="\u7F8E\u56FD";s3.startTime=null;s3.subject="\u751F\u7269,\u8DA3\u5473\u79D1\u666E";s3.tags="\u4EBA\u7C7B,\u8FDB\u5316\u8BBA,\u8FDB\u5316,";s3.title="\u4E3A\u4EC0\u4E48\u8BF4\u4EBA\u7C7B\u7684\u8FDB\u5316\u5F88\u91CD\u8981\uFF1F";
# s4.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/5/2/c427d57ea4f44c7a8564e2e7b1bd4052.jpg";s4.category="\u5176\u4ED6";s4.courseId="MCOUOGBAO";s4.courseType=10;s4.courseUrl="http://open.163.com/movie/2017/7/I/4/MCOUOGBAO_MCOUOIPI4.html";s4.description="\u98DF\u7269\u4FDD\u8D28\u671F\u5341\u5206\u91CD\u8981\uFF0C\u6D88\u8D39\u8005\u8D2D\u4E70\u98DF\u54C1\u7684\u65F6\u5019\u603B\u662F\u4F1A\u770B\u770B\u4FDD\u8D28\u671F\uFF0C\u6765\u786E\u4FDD\u81EA\u5DF1\u8D2D\u4E70\u7684\u662F\u5B89\u5168\u65B0\u9C9C\u7684\u98DF\u54C1\u3002\u4F46\u4FDD\u8D28\u671F\u4E0A\u7684\u65E5\u671F\uFF0C\u771F\u7684\u53EF\u4FE1\u5417\uFF1F\u4E00\u4E9B\u98DF\u54C1\u9500\u552E\u4E1A\u754C\u4EBA\u58EB\u8BF4\uFF0C\u86CB\u7CD5\uFF0C\u8089\u7C7B\u4EA7\u54C1\u8FC7\u671F\u4E4B\u540E\u4F1A\u91CD\u65B0\u5305\u88C5\uFF0C\u4FEE\u6539\u4FDD\u8D28\u671F\u65E5\u671F\u3002\u53D1\u9709\u7684\u6C34\u679C\u4F1A\u5207\u6389\u53D1\u9709\u90E8\u5206\u6765\u505A\u6210\u679C\u76D8\u51FA\u552E\u3002\u4E13\u5BB6\u8868\u793A\uFF0C\u53D1\u9709\u7684\u852C\u83DC\u6C34\u679C\u548C\u8089\u5236\u54C1\u4F1A\u6ECB\u751F\u7EC6\u83CC\uFF0C\u98DF\u7528\u540E\u53EF\u80FD\u9020\u6210\u75BE\u75C5\uFF0C\u751A\u81F3\u6709\u81F4\u547D\u98CE\u9669\u3002\u52A0\u62FF\u5927\u7535\u89C6\u53F0\u6DF1\u5165\u8C03\u67E5\uFF0C\u5411\u4F60\u63ED\u9732\u5173\u4E8E\u4FDD\u8D28\u671F\u7684\u90A3\u4E9B\u9ED1\u5E55\u3002\uFF08\u611F\u8C22\u730E\u4EBA\u5B57\u5E55\u7EC4\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s4.instructor="\u52A0\u62FF\u5927";s4.movieCount=1;s4.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/5/f/d20c5fa3a8914730920e0a78124e4e5f.jpg_180x100x1x95.jpg";s4.school="\u52A0\u62FF\u5927";s4.startTime=null;s4.subject="\u793E\u4F1A,\u8DA3\u5473\u79D1\u666E,\u5065\u5EB7";s4.tags="\u98DF\u54C1\u4FDD\u8D28\u671F,\u53EF\u4FE1\u5417,\u52A0\u62FF\u5927\u7535\u89C6\u53F0,";s4.title="\u98DF\u54C1\u4FDD\u8D28\u671F\u771F\u7684\u53EF\u4FE1\u5417\uFF1F";
# s5.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/c/f/32072912b10d4761824a8927eddbeacf.jpg";s5.category="\u5176\u4ED6";s5.courseId="MCOUR6OSJ";s5.courseType=10;s5.courseUrl="http://open.163.com/movie/2017/7/8/R/MCOUR6OSJ_MCOUR8P8R.html";s5.description="\u8FD9\u53EF\u80FD\u662F\u53F2\u4E0A\u6700\u840C\u7684\u5173\u4E8E\u89E3\u8BF4\u201C\u4E00\u5E26\u4E00\u8DEF\u201D\u7684\u5B9A\u683C\u52A8\u753B\u4E86\u3002\uFF08\u611F\u8C22LetsVideo\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s5.instructor="\u4E2D\u56FD";s5.movieCount=1;s5.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/f/7/e47dd53b283a410193bde1286cff3af7.jpg_180x100x1x95.jpg";s5.school="\u4E2D\u56FD";s5.startTime=null;s5.subject="\u7F8E\u98DF,\u8DA3\u5473\u79D1\u666E,\u6587\u5316";s5.tags="\u5B9A\u683C\u52A8\u753B,\u7F8E\u98DF,\u4E00\u5E26\u4E00\u8DEF,";s5.title="\u201C\u4E00\u5E26\u4E00\u8DEF\u201D\u4ECE\u820C\u5C16\u5F00\u59CB";
# s6.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/8/6/ce66fc773ca24912be9a31fce7966986.jpg";s6.category="TED";s6.courseId="MCOSID16N";s6.courseType=10;s6.courseUrl="http://open.163.com/movie/2017/7/P/5/MCOSID16N_MCOUUG9P5.html";s6.description="\u5FD8\u8BB0\u6DF7\u5408\u52A8\u529B\u8F66\uFF0CShai Agassi\u8BF4\u5982\u679C\u6211\u4EEC\u8981\u771F\u7684\u6539\u53D8\u6392\u653E\u91CF\uFF0C\u6211\u4EEC\u5F97\u9009\u62E9\u7535\u529B\u8F66\u3002\u4ED6\u7684\u516C\u53F8\uFF0CBetter Place\uFF0C\u4E3A\u6211\u4EEC\u5E26\u6765\u4E00\u4E2A\u6FC0\u8FDB\u7684\u8BA1\u5212\uFF0C\u4E00\u4E2A\u53EF\u4EE5\u8BA9\u4E0D\u540C\u56FD\u5BB6\u57282020\u5E74\u5B8C\u5168\u6446\u8131\u77F3\u6CB9\u7684\u8BA1\u5212\u3002\uFF08\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s6.instructor="Shai Agassi";s6.movieCount=1;s6.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/d/e/453134fce9684168b60f8f2ca041fbde.jpg_180x100x1x95.jpg";s6.school="TED";s6.startTime=null;s6.subject="\u73AF\u5883";s6.tags="SHAI AGGASI\u7684\u8C6A\u8FC8\u7684\u7535\u529B\u8F66\u8BA1\u5212,SHAI AGASSI ON ELECTRIC CARS,";s6.title="[TED]Shai Aggasi\u7684\u8C6A\u8FC8\u7684\u7535\u529B\u8F66\u8BA1\u5212";
# s7.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/e/a/d2fa760bcabf4964b62eaec662fa02ea.jpg";s7.category="\u5176\u4ED6";s7.courseId="MCP3CI197";s7.courseType=10;s7.courseUrl="http://open.163.com/movie/2017/7/M/K/MCP3CI197_MCP3CN9MK.html";s7.description="\u66F4\u51C6\u786E\u7684\u8BA4\u77E5\uFF0C\u5E26\u6765\u66F4\u6709\u6548\u7684\u81EA\u6211\u5F62\u8C61\u7684\u5EFA\u7ACB\u3002\u4F60\u6709\u4ED4\u7EC6\u89C2\u5BDF\u8FC7\u81EA\u5DF1\u7684\u8EAB\u4F53\u5417\uFF1F\u4F60\u4F1A\u6709\u7247\u4E2D\u4E3B\u4EBA\u516C\u7684\u56F0\u60D1\u5417\uFF1F \u8BDA\u5B9E\u5730\u8BF4\uFF0C\u4EBA\u4EBA\u90FD\u4F1A\u6709\u7684\u3002\uFF08\u611F\u8C22\u963F\u5C14\u6CD5\u5C0F\u5206\u961F\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s7.instructor="\u7F8E\u56FD";s7.movieCount=1;s7.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/a/3/3d911feefe834d9a9d46f322b2df70a3.jpg_180x100x1x95.jpg";s7.school="\u7F8E\u56FD";s7.startTime=null;s7.subject="\u533B\u5B66,\u8DA3\u5473\u79D1\u666E,\u5065\u5EB7";s7.tags="\u7231\u62A4\u8EAB\u4F53,\u56F0\u60D1,\u89C2\u5BDF\u8EAB\u4F53,";s7.title="\u6211\u662F\u5982\u4F55\u5B66\u7740\u7231\u62A4\u81EA\u5DF1\u7684\u8EAB\u4F53\u7684\u5462";
# s8.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/e/c/5e2b2db38fa14645a198f8dd7b6654ec.jpg";s8.category="\u5176\u4ED6";s8.courseId="MCP3G9AGI";s8.courseType=10;s8.courseUrl="http://open.163.com/movie/2017/7/F/S/MCP3G9AGI_MCP3GLQFS.html";s8.description="\u5192\u9669\u5BB6\u548C\u8282\u76EE\u4E3B\u6301\u4EBA\u73ED\u798F\u683C\u548C\u725B\u7F9A\u5C08\u5BB6\u683C\u5170\u6DF1\u5165\u5766\u6851\u5C3C\u4E9E\u7684\u585E\u4F26\u76D6\u8482\u8349\u539F, \u63A2\u7D22\u725B\u7F9A\u7684\u6545\u4E8B\u3002\u4ED6\u4EEC\u7531\u6BCF\u65E5\u8BDE\u751F12000\u53EA\u725B\u7F9A\u7684\u8349\u539F\u5F00\u59CB, \u76EE\u7779\u8106\u5F31\u7684\u65B0\u751F\u547D, \u725B\u7F9A\u7FA4\u7684\u52A8\u6001\u53CA\u98DF\u8089\u517D\u5BF9\u725B\u7F9A\u7684\u5A01\u80C1\u3002\uFF08\u611F\u8C22\u5E84\u4E03\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s8.instructor="\u7F8E\u56FD";s8.movieCount=1;s8.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/0/6/93e24a27b7994ba39b5968d0841e5a06.jpg_180x100x1x95.jpg";s8.school="\u7F8E\u56FD";s8.startTime=null;s8.subject="\u73AF\u5883,\u8D4F\u8BFE,\u52A8\u7269";s8.tags="\u52A8\u7269\u5927\u8FC1\u5F99,\u72C2\u91CE,";s8.title="\u72C2\u91CE\u5927\u8FC1\u5F99";
# s9.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/3/5/9e96c0de8291442287b425a81537e535.jpg";s9.category="\u5176\u4ED6";s9.courseId="MCOUO6H8K";s9.courseType=10;s9.courseUrl="http://open.163.com/movie/2017/7/Q/5/MCOUO6H8K_MCOUQNKQ5.html";s9.description="\u5F20\u8700\u5EB7\uFF0C\u4E2D\u79D1\u9662\u53E4\u810A\u690E\u52A8\u7269\u4E0E\u53E4\u4EBA\u7C7B\u7814\u7A76\u6240\u535A\u58EB\uFF0C\u4ED6\u5C06\u544A\u8BC9\u5927\u5BB6\u6050\u9F99\u86CB\u91CC\u6709\u4EC0\u4E48\u4E0D\u786E\u5B9A\u6027\u5462\uFF1F\uFF08\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s9.instructor="\u5F20\u8700\u5EB7";s9.movieCount=1;s9.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/c/3/6707697ea9194e5b8a1885430289b3c3.jpg_180x100x1x95.jpg";s9.school="\u4E00\u5E2D";s9.startTime=null;s9.subject="\u5386\u53F2,\u751F\u7269,\u6F14\u8BB2,\u6587\u5316,\u6559\u80B2";s9.tags="\u6050\u9F99\u86CB\u91CC\u7684\u4E0D\u786E\u5B9A\u6027\uFF0C\u4E00\u5E2D\uFF0C,";s9.title="[\u4E00\u5E2D]\u6050\u9F99\u86CB\u91CC\u7684\u4E0D\u786E\u5B9A\u6027";
# s10.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/2/7/6fd8b20fb36c4fa4ab148bcc43cb5b27.jpg";s10.category="\u5176\u4ED6";s10.courseId="MCP620SS0";s10.courseType=10;s10.courseUrl="http://open.163.com/movie/2017/7/F/1/MCP620SS0_MCP6229F1.html";s10.description="\u76F8\u540C\u7EAC\u5EA6\uFF0C\u4E0D\u540C\u534A\u7403\u7684\u6C34\u5728\u6D41\u5411\u6392\u6C34\u53E3\u7684\u65F6\u5019\u5F62\u6210\u65CB\u6DA1\u7684\u65B9\u5411\u662F\u76F8\u53CD\u7684\u5417\uFF1F\uFF08\u611F\u8C22\u67DA\u5B50\u6728\u5B57\u5E55\u7EC4\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s10.instructor="\u7F8E\u56FD";s10.movieCount=1;s10.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/e/e/66958b195f504d63987aa1b99bc3ebee.jpg_180x100x1x95.jpg";s10.school="\u7F8E\u56FD";s10.startTime=null;s10.subject="\u73AF\u5883,\u8DA3\u5473\u79D1\u666E,\u79D1\u6280";s10.tags="\u5B9E\u9A8C,\u5357\u5317\u534A\u7403\u76F8\u53CD,\u6C34\u6D41\u65CB\u6DA1,";s10.title="\u5357\u534A\u7403\u6F29\u6DA1\u65B9\u5411\u4E0E\u5317\u534A\u7403\u76F8\u53CD\uFF1F";
# s11.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/0/a/efcbebbf5fd1465c898cbe24d922980a.jpg";s11.category="\u5176\u4ED6";s11.courseId="MCON7CE6N";s11.courseType=10;s11.courseUrl="http://open.163.com/movie/2017/7/2/G/MCON7CE6N_MCP65DP2G.html";s11.description="\u4F20\u8BF4\u6709\u4F4D\u5987\u4EBA\u56E0\u4E08\u592B\u5916\u9047\u5FC3\u751F\u5992\u6068\uFF0C\u4FBF\u6BCF\u5929\u9489\u7A3B\u8349\u4EBA\u6765\u8BC5\u5492\u5979\u7684\u4E08\u592B\uFF0C\u7ED3\u679C\u5728\u5FC3\u613F\u5FEB\u8981\u7ED3\u675F\u4E4B\u65F6\uFF0C\u5979\u81EA\u5DF1\u5374\u5012\u5728\u81EA\u5BB6\u4E95\u53E3\u524D\u6B7B\u53BB\u3002\u4ECE\u6B64\u6709\u4E86\u8FD9\u53E3\u5207\u65AD\u59FB\u7F18\u7684\u4E95\u3002";s11.instructor="\u65E5\u672C";s11.movieCount=1;s11.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/6/0/cca5cfc7cfff4b06ab1333ba7c110d60.jpg_180x100x1x95.jpg";s11.school="\u65E5\u672C";s11.startTime=null;s11.subject="\u8D4F\u8BFE,\u7F51\u6613\u516C\u5F00\u8BFE,\u6587\u5316";s11.tags="\u4EAC\u90FD\u4EBA\u7684\u79C1\u623F\u96C5\u8DA3\u2014\u2014\u590F.\u602A\u8AC7\u7BC7,\u4EAC\u90FD,";s11.title="\u4EAC\u90FD\u4EBA\u7684\u79C1\u623F\u96C5\u8DA3\u2014\u2014\u590F.\u602A\u8AC7\u7BC7";
# s12.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/6/2/507c164600ac453391be83190655dc62.jpg";s12.category="\u5176\u4ED6";s12.courseId="MCOUOCJOM";s12.courseType=10;s12.courseUrl="http://open.163.com/movie/2017/7/8/R/MCOUOCJOM_MCOUOOM8R.html";s12.description="\u672C\u671F\u6F14\u8BB2\u8005\u540D\u53EB\u987B\u4E00\u74DC\uFF0C\u4F5C\u5BB6\u3002\u4E3B\u8981\u4F5C\u54C1\u6709\u300A\u592A\u9633\u9ED1\u5B50\u300B\uFF08\u7535\u5F71\u300A\u70C8\u65E5\u707C\u5FC3\u300B\u539F\u8457\uFF09\u3001\u300A\u6DE1\u7EFF\u8272\u7684\u6708\u4EAE\u300B\u7B49\u3002\uFF08\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s12.instructor="\u987B\u4E00\u74DC";s12.movieCount=1;s12.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/2/b/574e07b3c60545a184fabb297ae7302b.jpg_180x100x1x95.jpg";s12.school="\u4E00\u5E2D";s12.startTime=null;s12.subject="\u6CD5\u5F8B,\u6F14\u8BB2";s12.tags="\u4E00\u5E2D\uFF0C,\u6240\u6709\u7684\u5224\u51B3\u4E66\u90FD\u662F\u4EBA\u751F\u526A\u5F71,";s12.title="[\u4E00\u5E2D]\u6240\u6709\u7684\u5224\u51B3\u4E66\u90FD\u662F\u4EBA\u751F\u526A\u5F71";
# s13.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/1/7/fc1a2d1862ce4416b9ceb7818ae19517.jpg";s13.category="TED";s13.courseId="MCP76PT9B";s13.courseType=10;s13.courseUrl="http://open.163.com/movie/2017/7/9/M/MCP76PT9B_MCP789R9M.html";s13.description="\u97E9\u96EA\u79F0\u81EA\u5DF1\u201C\u79EF\u6781\u7684\u60B2\u89C2\u4E3B\u4E49\u8005\u201D\uFF0C\u4E0D\u7BA1\u4EE5\u827A\u4EBA\u8EAB\u4EFD\u53C2\u52A0\u771F\u4EBA\u79C0\uFF0C\u4EA6\u6216\u4EE5\u5236\u4F5C\u4EBA\u8EAB\u4EFD\u5236\u4F5C\u7535\u5F71\uFF0C\u5979\u59CB\u7EC8\u5BF9\u7ACB\u770B\u5F85\uFF0C\u51C6\u5907\u8FCE\u63A5\u201Cworst\u201D\uFF0C\u524D\u8DEF\u53EA\u6709\u201Cbetter\u201D\u3002\uFF08\u611F\u8C22TEDxSuzhou\u6388\u6743\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s13.instructor="\u97E9\u96EA";s13.movieCount=1;s13.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/e/5/4b40a41b320d487e81ab84e5274f08e5.jpg_180x100x1x95.jpg";s13.school="TEDxSuzhou";s13.startTime=null;s13.subject="\u793E\u4F1A";s13.tags="\u79EF\u6781\u7684\u60B2\u89C2\u4E3B\u4E49\u8005,";s13.title="[TEDxSuzhou]\u97E9\u96EA\uFF1A\u79EF\u6781\u7684\u60B2\u89C2\u4E3B\u4E49\u8005";
# s14.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/0/9/28f31a37c8ff4f86a4e8f14b4edad009.jpg";s14.category="\u5176\u4ED6";s14.courseId="MCON5FKFS";s14.courseType=10;s14.courseUrl="http://open.163.com/movie/2017/7/7/M/MCON5FKFS_MCON5RA7M.html";s14.description="\u7537\u4EBA\u6765\u81EA\u706B\u661F\uFF0C\u5973\u4EBA\u6765\u81EA\u91D1\u661F\u3002\u5230\u5E95\u662F\u591A\u4E48\u5947\u602A\u7684\u4E24\u79CD\u751F\u7269?\uFF08\u611F\u8C22\u7EA2\u70E7\u725B\u8089\u5B57\u5E55\u7EC4\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s14.instructor="\u7F8E\u56FD";s14.movieCount=1;s14.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/4/9/a01857c50bce4765a03ff0493c59e449.jpg_180x100x1x95.jpg";s14.school="\u7F8E\u56FD";s14.startTime=null;s14.subject="\u793E\u4F1A,\u8D4F\u8BFE,\u7F51\u6613\u516C\u5F00\u8BFE";s14.tags="\u7537\u5973\u95F4\u5341\u5927\u9887\u53D7\u4E89\u8BAE\u7684\u5DEE\u5F02,\u4E24\u6027,";s14.title="\u7537\u5973\u95F4\u5341\u5927\u9887\u53D7\u4E89\u8BAE\u7684\u5DEE\u5F02";
# s15.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/2/a/f5a539172be345d9b3a6d9d73656162a.jpg";s15.category="\u5176\u4ED6";s15.courseId="MCP8MEFKK";s15.courseType=10;s15.courseUrl="http://open.163.com/movie/2017/7/A/2/MCP8MEFKK_MCP8MKRA2.html";s15.description="\u963F\u5179\u6D77\u9ED8\u75C7\u76EE\u524D\u8FD8\u65E0\u6CD5\u6CBB\u6108\uFF0C\u4F46\u8FD9\u90E8\u89C6\u9891\u5C06\u4F1A\u4E3A\u5927\u5BB6\u5206\u89E3\u963F\u5179\u6D77\u9ED8\u75C7\u7684\u6210\u56E0\uFF0C\u4E86\u89E3\u4F60\u5927\u8111\u53D1\u751F\u7684\u53D8\u5316\uFF01\uFF08\u611F\u8C22\u5B57\u5E55\u83CC\u56E2\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s15.instructor="\u7F8E\u56FD";s15.movieCount=1;s15.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/7/1/d6ffb4b72d254933a94144c21b396a71.jpg_180x100x1x95.jpg";s15.school="\u7F8E\u56FD";s15.startTime=null;s15.subject="\u533B\u5B66,\u8DA3\u5473\u79D1\u666E,\u5065\u5EB7";s15.tags="\u8001\u5E74\u75C5,\u963F\u5179\u6D77\u9ED8\u75C7,\u6210\u56E0,";s15.title="\u52A8\u753B\u5206\u89E3\u963F\u5179\u6D77\u9ED8\u75C7\u7684\u6210\u56E0\u5185\u5E55";
# s16.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/3/3/3/c37346ffe23a413281ae357cb0e65033.jpg";s16.category="\u56FD\u9645\u540D\u6821\u516C\u5F00\u8BFE";s16.courseId="MBCMMCILL";s16.courseType=10;s16.courseUrl="http://open.163.com/special/opencourse/crashcourseworldhistory2.html";s16.description="\u65E0\u5398\u5934\u5386\u53F2\u7B2C\u4E8C\u5B63\u5F00\u8BB2\u5566\uFF01\u5B83\u662FYoutube\u4E0A\u6700\u53D7\u6B22\u8FCE\u7684\u5386\u53F2\u8BFE\u7A0B\u3002John Green \u5E26\u4F60\u8FDB\u5165\u4E16\u754C\u5386\u53F2\uFF0C\u6BCF\u5929\u5341\u5206\u949F\uFF0C\u8F7B\u677E\u770B\u61C2\u4E16\u754C\u3002\uFF08\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s16.instructor="John Green";s16.movieCount=35;s16.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/3/0/6/db4529a1cee34593bb81cd6fb6dc3c06.jpg_180x100x1x95.jpg";s16.school="Crash Course";s16.startTime=null;s16.subject="\u5386\u53F2";s16.tags="\u5386\u53F2,\u4E16\u754C\u5386\u53F2,\u7EAA\u5F55\u7247,CRASH COURSE,\u7F51\u6613\u516C\u5F00\u8BFE,";s16.title="Crash Course \u4E16\u754C\u5386\u53F2 \uFF08\u7B2C\u4E8C\u5B63\uFF09";
# s17.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/8/e/f9420540282b459cb0b39386c747cf8e.jpg";s17.category="\u5176\u4ED6";s17.courseId="MCP6EOMPO";s17.courseType=10;s17.courseUrl="http://open.163.com/movie/2017/7/F/N/MCP6EOMPO_MCP6EPUFN.html";s17.description="\u5A01\u5C14\u00B7\u53F2\u5BC6\u65AF\u3001\u4E54\u5C14\u00B7\u57C3\u54F2\u987F\u53C2\u6F14\u7684\u300CBright\u300D\u5C06\u7531\u5927\u536B\u00B7\u963F\u8036\u6267\u5BFC\uFF0C\u9A6C\u514B\u65AF\u00B7\u5170\u8FEA\u65AF\u64CD\u5200\u5267\u672C\u3002\u5018\u82E5\u6211\u4EEC\u751F\u6D3B\u5728\u4E00\u4E2A\u534A\u517D\u4EBA\u3001\u7CBE\u7075\u4EE5\u53CA\u4EBA\u7C7B\u5171\u5B58\u7684\u65F6\u4EE3\uFF0C\u4E5F\u8BB8\u4F1A\u662F\u8FD9\u6837\u7684\uFF08\u611F\u8C22\u5F00\u773C\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s17.instructor="\u7F8E\u56FD";s17.movieCount=1;s17.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/e/3/e6c7b92967a945b492de7463bcaed0e3.jpg_180x100x1x95.jpg";s17.school="\u7F8E\u56FD";s17.startTime=null;s17.subject="\u8868\u6F14\u827A\u672F,\u8DA3\u5473\u79D1\u666E,\u6587\u5316";s17.tags="\u7535\u5F71\u9884\u544A\u7247,\u660E\u4EAE,\u5A01\u5C14\u00B7\u53F2\u5BC6\u65AF,";s17.title="\u5A01\u5C14\u00B7\u53F2\u5BC6\u65AF\u65B0\u7247\uFF1A\u300C\u660E\u4EAE\u300D\u4E2D\u6587\u9884\u544A";
# s18.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/a/7/f598ec705ada4df6adacc9fe833ad8a7.jpg";s18.category="\u5176\u4ED6";s18.courseId="MCP960VC6";s18.courseType=10;s18.courseUrl="http://open.163.com/movie/2017/7/S/C/MCP960VC6_MCP978VSC.html";s18.description="\u4E00\u4E2A\u638C\u7BA1\u7740\u6570\u4EBF\u8D44\u4EA7\u7684\u4F01\u4E1A\u5BB6\u70ED\u8877\u4E8E\u67D0\u79CD\u5192\u9669\u4F53\u80B2\u6D3B\u52A8\uFF0C\u8FD9\u79CD\u820D\u8EAB\u5BB6\u6027\u547D\u4E0D\u987E\u7684\u884C\u4E3A\u4EE4\u4E0D\u5C11\u4EBA\u5927\u60D1\u4E0D\u89E3\u3002\u6500\u767B\u8005\u7684\u52C7\u6C14\u6765\u81EA\u5F3A\u5065\u7684\u4F53\u683C\u548C\u5A34\u719F\u7684\u767B\u5C71\u6280\u5DE7\uFF0C\u672C\u7247\u63A2\u8BA8\u201C\u5230\u5E95\u4EC0\u4E48\u662F\u80C6\u91CF\u201D\u3002\uFF08\u611F\u8C22\u57D6\u57D6\u57D6\u57D6\u57D6\u57D6\u57D6\u57D6\u795E\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s18.instructor="\u7F8E\u56FD";s18.movieCount=1;s18.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/3/5/b61a5440739e4a38bab6dacb9072e735.jpg_180x100x1x95.jpg";s18.school="\u7F8E\u56FD";s18.startTime=null;s18.subject="\u5FC3\u7406,\u8D4F\u8BFE,\u8FD0\u52A8";s18.tags="\u5192\u9669,\u6781\u9650\u8FD0\u52A8,\u52C7\u6562\u6311\u6218,";s18.title="\u6781\u9650\u98DE\u8DC3\uFF1A\u5192\u9669\u7684\u5185\u6DB5";
# s19.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/9/a/bbe05794e1d14633aee3cbe66e857f9a.jpg";s19.category="\u5176\u4ED6";s19.courseId="MCPB4U2O6";s19.courseType=10;s19.courseUrl="http://open.163.com/movie/2017/7/G/G/MCPB4U2O6_MCPB5A8GG.html";s19.description="\u9A6C\u5FD7\u98DE\uFF0C\u5730\u8D28\u5DE5\u7A0B\u5E08\u3002\u51E0\u767E\u4E07\u5E74\u8FD9\u6837\u4E00\u4E2A\u65F6\u95F4\u5355\u4F4D\uFF0C\u5BF9\u77F3\u5934\u6765\u8BF4\u5C31\u597D\u50CF\u6211\u4EEC\u4EBA\u7C7B\u7684\u4E00\u6B21\u547C\u5438\u800C\u5DF2\u3002\uFF08\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s19.instructor="\u9A6C\u5FD7\u98DE";s19.movieCount=1;s19.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/f/3/59abe2d67b6b428cb8d6d9eb45da96f3.jpg_180x100x1x95.jpg";s19.school="\u4E00\u5E2D";s19.startTime=null;s19.subject="\u7269\u7406,\u73AF\u5883,\u6F14\u8BB2";s19.tags="\u4E00\u5E2D\uFF0C\u77F3\u5934\u662F\u5730\u7403\u7684\u5F80\u4E8B,";s19.title="[\u4E00\u5E2D]\u77F3\u5934\u662F\u5730\u7403\u7684\u5F80\u4E8B";
# s20.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/6/b/488107f7332c40c5aa80e6e03708a86b.jpg";s20.category="TED";s20.courseId="MCPB8FPEC";s20.courseType=10;s20.courseUrl="http://open.163.com/movie/2017/7/U/9/MCPB8FPEC_MCPB8OMU9.html";s20.description="\u53CC\u6EAA\u6BDB\u7CEF\u9EBB\u98CE\u75C5\u9662\u53C2\u8BAE\u4F1A\u7406\u4E8B\u517C\u300A\u56DE\u5BB6\u300B\u4F5C\u8005\u9648\u5F66\u59AE\u54FD\u54BD\u53D9\u8FF0\u793E\u4F1A\u5BF9\u9EBB\u98CE\u75C5\u7684\u6B67\u89C6\uFF0C\u4EE5\u53CA\u5F3A\u52A0\u4E8E\u60A3\u8005\u4E0E\u4EB2\u5C5E\u7684\u4E00\u4E2A\u8D1F\u9762\u6807\u7B7E\uFF1B\u5BF9\u9EBB\u98CE\u75C5\u7684\u8BEF\u89E3\uFF0C\u4EA7\u751F\u4E86\u4E16\u4EBA\u4E0E\u60A3\u8005\u4E4B\u95F4\u7684\u9E3F\u6C9F\u3002\u5979\u8BA4\u4E3A\uFF0C\u4F60\u7684\u8BA4\u540C\uFF0C\u4F60\u7684\u63A5\u53D7\uFF0C\u6B63\u662F\u5F15\u9886\u4ED6\u4EEC\u5F00\u653E\u56DE\u5BB6\u9053\u8DEF\u90A3\u6247\u5927\u95E8\u7684\u91CD\u8981\u4E4B\u5319\u3002\uFF08\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s20.instructor="\u9648\u5F66\u59AE";s20.movieCount=1;s20.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/5/9/c06120147a0543c79942b31bc2ef3b59.jpg_180x100x1x95.jpg";s20.school="TEDxPetalingStreet";s20.startTime=null;s20.subject="\u793E\u4F1A";s20.tags="\u56DE\u5BB6,THE WAY HOME,\u9648\u5F66\u59AE,";s20.title="[TEDx]\u56DE\u5BB6";
# s21.bigPicUrl="http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/e/f/96eae2f268744022991574fbd79472ef.jpg";s21.category="\u5176\u4ED6";s21.courseId="MCPBAFH1H";s21.courseType=10;s21.courseUrl="http://open.163.com/movie/2017/7/G/D/MCPBAFH1H_MCPBAIIGD.html";s21.description="\u81EA\u52A8\u552E\u8D27\u673A\u5982\u4F55\u7CBE\u51C6\u5730\u5B8C\u6210\u590D\u6742\u7684\u6536\u6B3E\u548C\u552E\u8D27\u73AF\u8282\uFF0C\u94A2\u7434\u7F8E\u5999\u7434\u58F0\u7684\u6765\u6E90\uFF0C\u8FD8\u6709\u624B\u63A7\u4E0B\u964D\u5668\u5B9E\u73B0\u591A\u91CD\u5B89\u5168\u4FDD\u969C\u7684\u5965\u79D8\u3002\uFF08\u611F\u8C22\u7EAA\u5F55\u7247\u4E4B\u5BB6\u5B57\u5E55\u7EC4\u8BD1\u5236\uFF0C\u7F51\u6613\u516C\u5F00\u8BFE\u7F16\u8F91\u6574\u7406\uFF09";s21.instructor="\u7F8E\u56FD";s21.movieCount=1;s21.picUrl="http://imgsize.ph.126.net/?enlarge=true&imgurl=http://open-image.nosdn.127.net/image/snapshot_movie/2017/7/4/9/3957c771e2f94a23b17d1f3584fae149.jpg_180x100x1x95.jpg";s21.school="\u63A2\u7D22\u9891\u9053";s21.startTime=null;s21.subject="\u8DA3\u5473\u79D1\u666E,\u79D1\u6280";s21.tags="\u81EA\u52A8\u552E\u8D27\u673A,\u94A2\u7434\u548C\u624B\u63A7\u4E0B\u964D\u5668,\u673A\u5668\u5927\u62C6\u89E3,";s21.title="\u673A\u5668\u5927\u62C6\u89E3\u4E4B\u81EA\u52A8\u552E\u8D27\u673A \u94A2\u7434\u548C\u624B\u63A7\u4E0B\u964D\u5668";
# dwr.engine._remoteHandleCallback('1507729229005','0',{baseQuery:s0,dtos:s1});"""
# courseLists = re.findall(pattern=pattern,string=string)
# for course in courseLists:
#     try:
#         print(str(course))
#     except UnicodeEncodeError as e:
#         print(course)
