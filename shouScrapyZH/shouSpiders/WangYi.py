# -*- coding=utf-8 -*-
import requests

url = "https://c.open.163.com/dwr/call/plaincall/OpenSearchBean.searchCourse.dwr"

payload = "callCount=1\nscriptSessionId=${scriptSessionId}190\nhttpSessionId=\nc0-scriptName=OpenSearchBean\nc0-methodName=searchCourse\nc0-id=0\nc0-param0=string:\nc0-param1=number:3\nc0-param2=number:20\nbatchId=1507729229005"
headers = {
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
    'cookie': "mail_psc_fingerprint=b98d53b9a03092e94f93fa4faf3d26ef; _ntes_nnid=8d63a00e17eac68f6fe33653e8a7efb6,1487146966421; _ntes_nuid=8d63a00e17eac68f6fe33653e8a7efb6; NTES_CMT_USER_INFO=8025510%7C179564369%7Chttps%3A%2F%2Fsimg.ws.126.net%2Fe%2Fimg5.cache.netease.com%2Ftie%2Fimages%2Fyun%2Fphoto_default_62.png.39x39.100.jpg%7Cfalse%7CejMwNjIyMzU1OEAxNjMuY29t; usertrack=ZUcIhViti+ccr1dYA1tXAg==; vjuids=18755ba10.15c7c578b9f.0.dcbbfeeb062a4; __gads=ID=c545d00d56c36cd6:T=1496734732:S=ALNI_MbZ533W9YUyHHN3E63dZWTzLBvfTg; UM_distinctid=15c7c5cf423ac-0e2654bf69577-30657509-1fa400-15c7c5cf4251c8; __s_=1; _ga=GA1.2.235581014.1487768553; P_INFO=z306223558@163.com|1506678215|0|other|11&14|shh&1504370037&gbox-lushi#shh&null#10#0#0|131160&0||z306223558@163.com; Province=021; City=021; vjlast=1496734731.1507729099.11; ne_analysis_trace_id=1507729099230; vinfo_n_f_l_n3=7822ab8d01b9ca88.1.12.1496735087228.1507609696703.1507729099459; s_n_f_l_n3=7822ab8d01b9ca881507729099235; __utma=187553192.235581014.1487768553.1501145566.1507729100.2; __utmb=187553192.3.10.1507729100; __utmc=187553192; __utmz=187553192.1507729100.2.2.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/ted/; __oc_uuid=71efe830-ae89-11e7-8920-6f292c2ba499; __utma=130438109.235581014.1487768553.1507729117.1507729117.1; __utmb=130438109.2.10.1507729117; __utmc=130438109; __utmz=130438109.1507729117.1.1.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/ocw/",
    'postman-token': "7eb438c8-1504-00a0-4c39-b0981e67ce91"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)