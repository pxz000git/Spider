# -*- coding=utf-8 -*-
import requests

from ..items import loadConf,_DBConf
import json
import pymongo
from random import randint

def initSpider(spider,trash_data,limit_count,storeConf):
    trash_data = bool(trash_data)
    spider.limit_count = int(limit_count)
    spider.logger.info("开始爬虫：")
    spider.logger.info("参数信息: " + storeConf)
    spider.logger.info("额外参数: " + 'limit_count' + "  " + str(limit_count))
    spider.logger.info("额外参数: " + 'trash_data' + "  " + str(trash_data))
    DBConf = loadConf(json.loads(storeConf), _DBConf)
    spider.collection = pymongo.MongoClient(DBConf["MONGODB_URI"]).get_database(
        DBConf['MONGODB_DATABASE']).get_collection(DBConf['MONGODB_COLLECTION'])
    if trash_data:
        spider.logger.info("正在清除数据：。。。\n")
        spider.logger.info(spider.collection.remove(dict(college=spider.name)))
    return spider.collection

def getProxy():
    isGoon = True
    resultsP = {}
    while(isGoon):
        response = requests.get("http://127.0.0.1:5010/get")
        proxiesText = response.text
        proxies = {"http":"http://" + response.text,"https":"https://" + response.text}
        #请求自己的一个地址，若有返回就表示这个代理可用
        try:
            response = requests.get("http://www.baidu.com",proxies=proxies,timeout=20)
            resultsP = proxies
            isGoon = False
        except Exception as e:
            #如果代理请求链接失败，我们请求接口，将这个ip从池中删除掉
            requests.get("http://127.0.0.1:5010/delete?proxy="+proxiesText)
    return resultsP

def randomIP():
    return str(randint(11,255))+"."+str(randint(11,255))+"."+str(randint(11,255))+"."+str(randint(11,255))