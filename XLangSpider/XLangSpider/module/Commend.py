# -*- coding:utf-8 -*-

import urllib
import urllib2
import time
import json
import requests
from lxml import etree


def CommSpider(id):
    page_start = 1
    headers = {
        "Host": "weibo.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        # "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        # "Referer": "https://weibo.com/1742566624/FDLgDiCos?ref=feedsdk&type=comment",
        "Cookie": "SUB=_2AkMtCFfEf8NxqwJRmPEQzWPqaYV2zgvEieKbVKYfJRMxHRl-yT83qlYTtRB6Boh5K36EXcuFlQ9bBu447gXsKXXlZlCE; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWr3Vd6q.LEVmlshJEXroLv; SINAGLOBAL=4269470727850.435.1515510018659; ULV=1515635821439:3:3:3:581152108391.7881.1515635821317:1515579704263; UOR=,,www.baidu.com; YF-V5-G0=da1eb9ea7ccc47f9e865137ccb4cf9f3; login_sid_t=5953859e0f4253c868bc486d65ea9b8f; cross_origin_proto=SSL; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; WBStorage=c1cc464166ad44dc|undefined; _s_tentry=www.baidu.com; Apache=581152108391.7881.1515635821317; YF-Page-G0=f994131fbcce91e683b080a4ad83c421; wb_cusLike_3655689037=N",
        "Connection": "keep-alive",
    }

    # 获取本地时间戳
    time_data = time.time()

    # 请求参数
    formdata = {
        "ajwvr": "6",
        "id": str(id),
        "page": str(page_start),
        "from": "singleWeiBo",
        "__rnd": str(long(time_data * 100))
    }
    url = "https://weibo.com/aj/v6/comment/big?"

    # 请求参数的解析
    data = urllib.urlencode(formdata)
    # 拼接url

    newurl = url + data
    # print(newurl)

    request = urllib2.Request(newurl, headers=headers)

    response = urllib2.urlopen(request)

    # 获取每页的HTML源码信息
    source = response.read()
    return source


# def SumSource(id, page_start, page_end):
#     '''
#     返回网页源码所有评论列表
#     :param id: 博文id
#     :param page_start: 起始页
#     :param page_end: 结束页
#     :return: 网页列表
#     '''
#
#     source_list = []
#
#     for page in range(page_start, page_end):
#         if int(page_start) < page_end:
#             source = CommSpider(id, page_start)
#             source_list.append(source)
#             page_start = int(page_start) + 1
#
#     return source_list


# if __name__ == "__main__":
#
#     id = "4194779179408912"
#     page_start = 1
#     page_end = 2
#     source_list = SumSource(id, page_start, page_end)
#     with open('comm.html', 'a') as f:
#         for source_comm in source_list:
#             text_comm = json.loads(source_comm)['data'].values()
#             # 剔除不合评论格式的评论
#             if len(text_comm) != 0:
#                 global html
#                 html = text_comm[1].encode('utf-8')
#             # print(html)
#             f.write(html)
