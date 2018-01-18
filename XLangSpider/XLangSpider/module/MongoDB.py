# -*- coding:utf-8 -*-

import pymongo as pm
from collections import *


class MongoOperat(object):
    def __init__(self, host, port, db_name_xl, XL_Post):
        '''
        设置mongodb的地址,端口
        :param host: ip
        :param port: 端口
        :param db_name_xl: 数据库
        :param XL_Post 数据集合
        '''
        self.host = host
        self.port = port
        self.XLPost = XL_Post
        # 建立数据库连接
        self.client = pm.MongoClient(host=host, port=port)
        # 选择相应的数据库
        self.db_xl = self.client.get_database(db_name_xl)

    def DataInsert(self, wb_list, XL_POST):
        '''
        写入微博数据
        :param wb_list: 微博,生成器
        :param XL_POST: 集合名称
        :return:
        '''
        collection1 = self.db_xl.get_collection(XL_POST)
        # 由于微博不同页面有相同的数据，根据post_id去重
        lis = []
        for Cursor in (collection1.find({}, {'_id': 0, 'post_id': 1})):
            li = Cursor['post_id']
            lis.append(li.encode('utf-8'))
        for wb in wb_list:
            if wb[0] in lis:
                continue
            # 去除有不规则的字符的微博
            try:
                collection1.save({"post_id": wb[0], "post": wb[1], "author": wb[2], "open_time": wb[3], "share_nums": wb[4],
                                  "comments_nums": wb[5], "like_nums": wb[6], "comments": wb[7]})
            except BaseException, e:
                print(e.message)
