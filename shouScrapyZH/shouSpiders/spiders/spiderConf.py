# -*- coding: utf-8 -*-
SpiderConf=dict(
    ERIC=dict(
        alias_name="美国国家教育资源库",
        alias_en="ERIC",
        base_url="eric.ed.gov",
        start_urls=[
            "http://eric.ed.gov"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    HangZhouLLL=dict(
        alias_name="杭州终身教育网",
        alias_en="HangZhou Last Study",
        base_url="hzlll.cn",
        start_urls=[
            "http://www.hzlll.cn/course/explore?page=1",
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    HaoDaXue=dict(
        alias_name="好大学中国Mooc学习网",
        alias_en="cnmooc.org",
        base_url="cnmooc.org",
        start_urls=[
            "http://www.cnmooc.org/portal/frontCourseIndex/course.mooc"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    HaoKeWang=dict(
        alias_name="好课网",
        alias_en="class.cn",
        base_url="class.cn",
        start_urls=[
            "http://www.class.cn/search/search_do?index=class"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    ICDE2018=dict(
        alias_name="ICDE2018",
        alias_en="ICDE2018",
        base_url="icde2018.org",
        start_urls=[
            "https://icde2018.org/"
        ],
        type="multiple",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    ICETC=dict(
        alias_name="ICETC",
        alias_en="ICETC",
        base_url="icetc.org",
        start_urls=[
            "http://www.icetc.org/index.html"
        ],
        type="multiple",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    JSStudy =dict(
        alias_name="江苏终身学习网",
        alias_en="js-study.cn",
        base_url="js-study.cn",
        start_urls=[
            "http://www.js-study.cn/course/front/courseResourcesAll.bsh?firstCategory=&interId=&jobId=&siteId=e089405566cf4a539106cb198ff14b94&order=0&searchContent="
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    LaoNianRen=dict(
        alias_name="上海老年人学习网",
        alias_en="LaoNianRen",
        base_url="e60sh.com",
        start_urls=[
            "http://www.e60sh.com/Course/QueryList?TagIds=&Page=1"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    MoocCnOnline=dict(
        alias_name="中国Mooc在线",
        alias_en="MoocCnOnline",
        base_url="icourses.cn，icourse163.org",
        start_urls=[
            "http://www.icourses.cn/oc/"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    MoocOpen=dict(
        alias_name="中国Mooc开放课程",
        alias_en="MoocOpen",
        base_url="icourses.cn",
        start_urls=[
            "http://www.icourses.cn/dirQueryVCourse.action"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    SHLLL=dict(
        alias_name="上海学习网",
        alias_en="SHLLL",
        base_url="xinstudy.cn",
        start_urls=[
            "http://course.xinstudy.cn/course/coursesearch/p_1/1/A63B73AEB3B95A63"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    WanFang=dict(
        alias_name="万方数据检索",
        alias_en="WanFang Data",
        base_url="shuxiavip.com",
        start_urls=[
            'http://www.shuxiavip.com/course.html'
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    WangYiYun=dict(
        alias_name="网易云课堂",
        alias_en="WangYi open data class",
        base_url="163.com",
        start_urls=[
            'https://c.open.163.com/search/search.htm?query=&enc=%E2%84%A2#/search/course'
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    WASET=dict(
        alias_name="WASET",
        alias_en="WASET",
        base_url="waset.org",
        start_urls=[
            "http://www.waset.org"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    ZheJiangLLL=dict(
        alias_name="浙江终身学习网",
        alias_en="ZheJiangLLL",
        base_url="zjerc.cn",
        start_urls=[
            "http://www.zjerc.cn/Web/default.aspx"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    ZhiHuiShu=dict(
        alias_name="智慧树在线教育",
        alias_en="ZhiHuiShu",
        base_url="ocw.uci.edu",
        start_urls=[
            "http://www.zjerc.cn/Web/default.aspx"
        ],
        type="single",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
    ZhiWang=dict(
        alias_name="中国知网",
        alias_en="ZhiWang",
        base_url="cnki.net",
        start_urls=[
            'http://kns.cnki.net/kns/brief/brief.aspx?RecordsPerPage=50&QueryID=4&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=custommode&SortType=(FFD%2c%27RANK%27)+desc&PageName=ASP.brief_default_result_aspx&curpage='
        ],
        type="multiple",
        params=[
            "storeConf","limit_count","trash_data"
        ]
    ),
)