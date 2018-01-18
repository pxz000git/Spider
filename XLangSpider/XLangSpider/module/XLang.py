# -*- coding:utf-8 -*-

import time
import json
import random
import urllib
import urllib2
from lxml import etree
from module.MongoDB import MongoOperat
from conf import settings
from module import Parse


class Spider(object):
    def __init__(self):
        # 初始化起始页
        self.page = settings.page
        # 设定结束页
        self.end_page = settings.end_page
        # for cat in [0, 2, 3, 10011, 10010, 10007, 10005, 99991]:
        #     self.category = cat

    def Proxy(self):
        '''
        设置代理IP
        :return:opener
        '''
        proxy = random.choice(settings.proxy_list)
        httpproxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(httpproxy_handler)
        return opener

    def loadPage(self, url):
        '''
        根据URL发送请求,获取服务器响应文件
        :param url:地址前半部分
        '''
        print("正在下载第%s页" % str(self.page))
        headers = {
            "Host": "weibo.com",
            "User-Agent": "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;TencentTraveler4.0;.NETCLR2.0.50727)",
            # "User-Agent": "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)",
            # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            # "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://weibo.com/",
            # "Cookie": "SUB=_2AkMtCFfEf8NxqwJRmPEQzWPqaYV2zgvEieKbVKYfJRMxHRl-yT83qlYTtRB6Boh5K36EXcuFlQ9bBu447gXsKXXlZlCE; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWr3Vd6q.LEVmlshJEXroLv; SINAGLOBAL=4269470727850.435.1515510018659; ULV=1515635821439:3:3:3:581152108391.7881.1515635821317:1515579704263; UOR=,,www.baidu.com; YF-V5-G0=da1eb9ea7ccc47f9e865137ccb4cf9f3; login_sid_t=5953859e0f4253c868bc486d65ea9b8f; cross_origin_proto=SSL; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; WBStorage=c1cc464166ad44dc|undefined; _s_tentry=www.baidu.com; Apache=581152108391.7881.1515635821317; YF-Page-G0=f994131fbcce91e683b080a4ad83c421; wb_cusLike_3655689037=N",
            # "Cookie": "SINAGLOBAL=6868967315112.739.1504056806226; ULV=1514947034749:25:3:4:6628763923800.313.1514947034693:1514870265726; UOR=,,www.baidu.com; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhvWLx6zbOhyRQUPFygs.uF5JpVF02NSo2EeK-N1KB7; SCF=Avevf87cmugmln_CpgVJE7JUlQ5Iv-61PzgerzPK2Ne8PDgnt6HAFO_M9eTNGewIP7YNs9ZHreYRVznJglF8Q9Q.; SUHB=05i6hMPBA6HTgD; UM_distinctid=15e6ab56be4118-00183f30ff14b58-40544130-15f900-15e6ab56be5cd; un=17612157940; SUB=_2AkMtEM7SdcPxrABUm_sTzWjib41H-jyexackAn7uJhMyAxgv7gtUqSdutBF-XMrAFh_naYT6FRfL6a8fIK9qLl73; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-V5-G0=5468b83cd1a503b6427769425908497c; YF-Page-G0=fc0a6021b784ae1aaff2d0aa4c9d1f17; _s_tentry=www.baidu.com; Apache=6628763923800.313.1514947034693; login_sid_t=9c21037fea95af8f324b1596b2fbe270; cross_origin_proto=SSL; WBStorage=c1cc464166ad44dc|undefined",
            "Connection": "keep-alive"
        }
        # 获取本地时间戳
        time_data = time.time()
        # 请求参数
        # 0, 2, 3, 10011, 10007, 10005, 99991
        formdata = {
            "ajwvr": "6",
            "category": "0",
            "page": str(self.page),
            "lefnav": "0",
            "__rnd": str(time_data * 100),
        }
        # 请求参数的解析
        data = urllib.urlencode(formdata)
        # 拼接url
        url = url + data
        # 请求对象
        request = urllib2.Request(url, data=data, headers=headers)
        # # 使用代理IP发送请求
        response = self.Proxy().open(request)

        # 获取每页的HTML源码信息
        source = response.read()
        # 获取到的是json对象,进行json解析
        text2 = json.loads(source)['data'].encode('utf-8')
        # xpath解析html页面
        selector = etree.HTML(text2)

        self.dealPage(selector)

    def writePage(self, wb_list):
        '''
        将内容写到数据库
        :param a_id: 微博博文id
        :param post: 微博正文
        :param author: 发布者
        :param open_time: 发布时间
        :param share_nums: 分享数量
        :param comments_nums: 评论数量
        :param like_nums: 点赞数量
        :return:
        '''
        host = settings.host
        port = settings.port

        # 数据库和集合
        DB_NAME_XL = settings.DB_NAME_XL
        XL_POST = settings.XL_POST

        db = MongoOperat(host, port, DB_NAME_XL, XL_POST)
        # 写入数据库
        db.DataInsert(wb_list, XL_POST)
        # item长度是15,每页
        # with open('wb.txt', 'a') as f:
        #     for wb in wb_list:
        #         for item in wb:
        #             if type(item) != list:
        #                 f.write("微博:%s" % item+"\n")
        #                 print(item)
        #                 # f.write("微博正文:%s" % item + "\n"),
        #                 # f.write("发布时间:%s" % item + "\n"),
        #                 # f.write(":%s" % item + "\n"),
        #                 # f.write("微博:%s" % item + "\n"),
        #                 # f.write("微博:%s" % item + "\n")
        #             else:
        #                 for i in item:
        #                     # print(len(item))
        #                     f.write("评论:%s" % i[1] + '\n')
        #                     f.write("评论者:%s" % i[0] + '\n')

    def dealPage(self, selector):
        '''
        处理解析html页面源码
        :param source:
        :return:
        '''
        # 调用博文解析方法,post_a:a类博文列表,post_b:b类博文列表
        # Parse.ParsePost_b(selector)
        wb_list_a = Parse.ParsePost_a(selector)
        wb_list_b = Parse.ParsePost_b(selector)
        # print(len(wb_list[7]))
        # for wb in wb_list_b:
        #     for item in wb:
        #         if type(item) != list:
        #             # print(type(item))
        #             print(item)
        #         else:
        #             for i in item:
        #                 # print(len(item))
        #                 print("评论:%s" % i[1])
        #                 print("评论者:%s" % i[0])
        #         # print(type(item))
        self.writePage(wb_list_a)
        self.writePage(wb_list_b)

    def XLSpider(self):
        '''
        爬虫调度器,负责组合处理每个页面的url
        :param url: url前半部分
        :param start_page:
        :param end_page:
        :return:
        '''
        url = "https://weibo.com/a/aj/transform/loadingmoreunlogin?"
        while self.page:
            # 每5页随机睡眠1~10秒
            if self.page % 5 == 0:
                ran = int(random.random() * 10) + 1
                print("**********正在随机睡眠%s秒**********" % ran)
                time.sleep(ran)
            # 到达指定页码不再抓取
            if self.page == self.end_page:
                print("抓取网页完毕...")
                break
            else:
                self.loadPage(url)
                # 每次循环，页码自增1
                self.page += 1


if __name__ == "__main__":
    wb = Spider()
    wb.XLSpider()
