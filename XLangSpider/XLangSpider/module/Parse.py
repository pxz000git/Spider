# -*- coding:utf-8 -*-

import json
import time
from module import Commend
from lxml import etree


def ParseComm(id):
    '''
    解析微博评论内容
    :param id:
    :return: 评论内容以及评论者
    '''
    # text_comm2 = ''
    source_comm = Commend.CommSpider(id)
    text_comm = json.loads(source_comm)['data'].values()
    # 剔除不合评论格式的评论
    if len(text_comm) != 0:
        global text_comm2
        text_comm2 = text_comm[1].encode('utf-8')

    # 微博评论
    comment_li_li = []
    selector_comm = etree.HTML(text_comm2)
    for each_comm in selector_comm.xpath("//div[@class='list_ul']/div/div[2]/div[@class='WB_text']"):
        # 获取评论和评论者
        comment = each_comm.xpath("string(.)")
        comment = comment.replace('\n', '').replace('\t', '').replace(' ', '').replace(u'\xa0\xa0', '').replace(
            u'\xc2\xa0', '')
        comment = comment.encode('raw_unicode_escape')
        # 切分评论
        comment_list = comment.replace('¡评论配图', '').split('：')
        comment_li_li.append(comment_list)
    return comment_li_li
        # 评论者
        # commenter = comment_list[0]
        # 评论内容,剔除不符合内容
        # comment_cont = comment_list[1]
        # print("评论:%s" % comment_cont + '\n')
        # print("评论者:%s" % commenter + '\n')


def ParsePost_a(selector):
    '''
    解析a类博文
    :param selector:选择器对象
    :return: 返回解析内容列表生成器
    '''
    for each1 in selector.xpath("//div[@class='UG_contents']/ul"):
        for each_a in each1.xpath("./div[@class='UG_list_a']"):
            # 微博博文id
            a_id = each_a.xpath("./@mid")[0]
            # 微博正文
            div = each_a.xpath("./h3/div")[0]

            # 获取某个标签下的全部文字信息
            post = div.xpath("string(.)")
            # 剔除空格等
            post = post.replace('\n', '').replace('\t', '').replace(' ', '').replace(u'\xa0\xa0', '').replace(
                u'\xc2\xa0', '')
            # 发布人
            author = each_a.xpath("./div[2]/a[2]/span[1]/text()")
            # 发布时间
            s_time = each_a.xpath("./div[2]/span[1]/text()")
            # 分享的数量
            share_nums = each_a.xpath("./div[2]/span[6]/em[2]/text()")
            # 评论的数量
            comments_nums = each_a.xpath("./div[2]/span[4]/em[2]/text()")
            # 点赞的数量
            like_nums = each_a.xpath("./div[2]/span[2]/em[2]/text()")

            post = post.encode('raw_unicode_escape')
            post = post.replace('...展开全文c', '')
            a_id = a_id.encode('raw_unicode_escape')
            author = author[0].encode('raw_unicode_escape')
            s_time = s_time[0].encode('raw_unicode_escape')
            # 转换时间,微博显示是:今天,换成相同格式时间,如:1月2日
            open_time = ''
            if s_time.split(' ')[0] == '今天':
                l = s_time.split(' ')
                # 转换成localtime
                time_local = time.localtime(time.time())
                # 转换成新的时间格式(2016-05-05 20:28:54)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                lt = dt.split(' ')[0].split('-')
                open_time = lt[1] + '月' + lt[2] + '日' + ' ' + l[1]

            else:
                open_time = s_time
            share_nums = share_nums[0].encode('raw_unicode_escape')
            comments_nums = comments_nums[0].encode('raw_unicode_escape')
            like_nums = like_nums[0].encode('raw_unicode_escape')
            # global post_a
            if a_id.__contains__('1022'):
                continue
            else:
                print(a_id)
                comment_li_li = ParseComm(a_id)
                post_a = []
                for i in [a_id, post, author, open_time, share_nums, comments_nums, like_nums, comment_li_li]:
                    post_a.append(i)
                    # print(i)
                # ParseComm(a_id)
                # print('************************')
                yield post_a


def ParsePost_b(selector):
    '''
    解析b类博文
    :param selector:选择器对象
    :return: 返回解析内容列表生成器
    '''
    for each1 in selector.xpath("//div[@class='UG_contents']/ul"):
        for each_b in each1.xpath("./div[@class='UG_list_b']"):
            # 微博博文id
            b_id = each_b.xpath("./@mid")[0]
            # 获取某个标签下的全部文字信息
            h3 = each_b.xpath('.//h3')[0]
            post = h3.xpath("string(.)")
            # 剔除空格等
            post = post.replace('\n', '').replace('\t', '').replace(' ', '').replace(u'\xa0\xa0', '').replace(
                u'\xc2\xa0', '')
            # 发布人
            author = each_b.xpath("./div[@class='list_des']/div[1]/a[2]/span[1]/text()")
            # 发布时间
            s_time = each_b.xpath("./div[@class='list_des']/div[1]/span[1]/text()")
            # 分享的数量
            share_nums = each_b.xpath(
                "./div[@class='list_des']/div[2]/span[5]/em[2]/text() | ./div[@class='list_des']/div[1]/span[6]/em[2]/text()")
            # 评论的数量
            comments_nums = each_b.xpath(
                "./div[@class='list_des']/div[2]/span[3]/em[2]/text() | ./div[@class='list_des']/div[1]/span[4]/em[2]/text()")
            # 点赞的数量
            like_nums = each_b.xpath(
                "./div[@class='list_des']/div[2]/span[1]/em[2]/text() | ./div[@class='list_des']/div[1]/span[2]/em[2]/text()")

            post = post.encode('raw_unicode_escape')
            post = post.replace('...展开全文c', '')
            b_id = b_id.encode('raw_unicode_escape')
            author = author[0].encode('raw_unicode_escape')
            s_time = s_time[0].encode('raw_unicode_escape')
            # 转换时间,微博显示是:今天,换成相同格式时间,如:1月2日
            open_time = ''
            if s_time.split(' ')[0] == '今天':
                l = s_time.split(' ')
                # 转换成localtime
                time_local = time.localtime(time.time())
                # 转换成新的时间格式(2016-05-05 20:28:54)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                lt = dt.split(' ')[0].split('-')
                open_time = lt[1] + '月' + lt[2] + '日' + ' ' + l[1]

            else:
                open_time = s_time
            share_nums = share_nums[0].encode('raw_unicode_escape')
            comments_nums = comments_nums[0].encode('raw_unicode_escape')
            like_nums = like_nums[0].encode('raw_unicode_escape')
            # global post_b
            # 清除没有文字的不规则博文
            if b_id.__contains__('1022'):
                continue
            else:
                print(b_id)
                comment_li_li = ParseComm(b_id)
                post_b = []
                for i in [b_id, post, author, open_time, share_nums, comments_nums, like_nums, comment_li_li]:
                    post_b.append(i)
                    # print(i)
                    # print(type(i))
                # ParseComm(b_id)
                # print('************************')
                yield post_b
