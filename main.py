# -*- coding: utf-8 -*-
# Author : richard


import os
import re
import time
import random
import requests
import json
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine


# 初始化数据库连接，使用pymysql模块
engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}"
                       .format('root',
                               'localhost',
                               '127.0.0.1：3306',
                               'sinatopsearchdata',
                               'utf8')
                      )

#请求头
headers_list = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'},
    {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
    {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)'},
    {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)'},
    {'User-Agent': 'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5'},
    {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
    {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52'},

]



# 配置链接数据库信息
db_config = {
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'sinatopsearchdata',
    'username': 'root',
    'password': '1234'
}
# 数据库链接地址
db_url = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(**db_config)
# 创建数据库引擎
engine = create_engine(db_url)
# 创建数据库链接


def loads_jsonp(_jsonp):
    """
    解析jsonp数据格式为json
    :return:
    """
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def get_the_page(url, params=None, headers=None,proxy=None, n=0):
    try:
        session = requests.Session()
        session.headers = headers
        url = 'https://passport.weibo.com/visitor/genvisitor'
        data = {
            'cb': 'gen_callback',
            'fp': '{"os":"1","browser":"Chrome91,0,4451,0","fonts":"undefined","screenInfo":"1920*1080*24","plugins":""}',
        }
        response = session.post(url, data=data)
        result = loads_jsonp(response.text)


        url = 'https://passport.weibo.com/visitor/visitor'
        params = {
            'a': 'incarnate',
            't': result['data']['tid'],
            'w': '2',
            'c': '095',
            'gc': '',
            'cb': 'cross_domain',
            'from': 'weibo',
            '_rand': random.random(),
        }
        session.get(url, params=params)
        url = 'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6'
        response = session.get(url, params=params, headers=headers, proxies=proxy, timeout=(30, 30) )
        response.encoding = 'utf8'

        if response.status_code == 200:
            return response.text
        else:
            if n < 3:
                n = n + 1
                return get_the_page(url, params=params, proxy=proxy, n=n)
            else:
                return None
    except:
        if n < 3:
            n = n + 1
            return get_the_page(url, params=params, proxy=proxy, n=n)
        else:
            return None


def get_the_page2(url1, params=None, headers=None,proxy=None, n=0):
    try:
        session = requests.Session()
        session.headers = headers
        url = 'https://passport.weibo.com/visitor/genvisitor'
        data = {
            'cb': 'gen_callback',
            'fp': '{"os":"1","browser":"Chrome91,0,4451,0","fonts":"undefined","screenInfo":"1920*1080*24","plugins":""}',
        }
        response = session.post(url, data=data)
        result = loads_jsonp(response.text)


        url = 'https://passport.weibo.com/visitor/visitor'
        params = {
            'a': 'incarnate',
            't': result['data']['tid'],
            'w': '2',
            'c': '095',
            'gc': '',
            'cb': 'cross_domain',
            'from': 'weibo',
            '_rand': random.random(),
        }
        session.get(url, params=params)

        response = session.get(url1, params=params, headers=headers, proxies=proxy, timeout=(30, 30) )
        response.encoding = 'utf8'

        if response.status_code == 200:
            return response.text
        else:
            if n < 3:
                n = n + 1
                return get_the_page2(url1, params=params, proxy=proxy, n=n)
            else:
                return None
    except:
        if n < 3:
            n = n + 1
            return get_the_page2(url1, params=params, proxy=proxy, n=n)
        else:
            return None


def pattern_return(pattern_str, html):#正则匹配方式
    '''
    :param pattern_str:
    :param html:
    :return:
    '''
    try:
        pattern = re.compile(pattern_str, re.S)
        items = re.findall(pattern, html)
        if len(items) <= 1:
            items = items[0]
    except:
        items = None
    return items




def get_url_list(html):#
    data_list = []
    tbody = pattern_return('<tbody>(.*?)</tbody>', html)
    items = pattern_return('<tr.*?>(.*?)</tr>', tbody)
    for item in items:
        ranktop = pattern_return('class="td-01.*?>(.*?)</td>', item)
        if ranktop == '<i class="icon-top"></i>':
            ranktop = 'Top'
        href = pattern_return('class="td-02.*?>.*?<a.*?href.*?="(.*?)"', item)
        title = pattern_return('<a.*?>(.*?)</a>', item)
        heat = pattern_return('<span>(.*?)</span>',item)
        icon = pattern_return('class="td-03.*?><i.*?>(.*?)</i></td>', item)
        time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        dic = dict(zip(['排名', '热搜标题','热度','链接', '标识','抓取时间'], [ranktop, title,heat,'https://s.weibo.com' + href,  icon,time1]))
        data_list.append(dic)
    return data_list
     


def parse_the_page(html):#解析话题页
    read = pattern_return('<span>今日阅读(.*?)</span>', html)
    if isinstance(read, list):
        read = read[0]
    discuss = pattern_return('<span>今日讨论(.*?)</span>', html)
    if isinstance(discuss, list):
        discuss = discuss[0]
    head = pattern_return('class="title">话题主持人<.*?info.*?<a.*?>(.*?)</a>', html)
    classification = pattern_return('card-wrap.*?分类：.*?<dd>(.*?)</dd>', html)
    area = pattern_return('card-wrap.*?地区：.*?<dd>(.*?)</dd>', html)
    if classification:
        classification = pattern_return('<a.*?>(.*?)</a>', classification)
    if area:
        area = pattern_return('<a.*?>(.*?)</a>', area)
        if area:
            if isinstance(area, list):
                area = '; '.join(area)
    dic = {
        '阅读': read,
        '讨论': discuss,
        '主持人': head,
        '分类': classification,
        '地区': area
    }
    return dic





if __name__ == '__main__':
    while True:
        try:
            begin_time = time.perf_counter()
            url = 'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6'
            api = 'http://FQWH123.v4.dailiyun.com/query.txt?key=NPA2F4B388&word=&count=17&rand=false&ltime=0&norepeat=false&detail=false'
            api_r = requests.get(api)
            api_r.encoding = 'gb2312'
            ip = api_r.text
            ip_list = [{'http': ip} for ip in ip.split(':57114\r\n') if ip]
            proxy1 = random.choice(ip_list)
            headers = random.choice(headers_list)
            html = get_the_page(url,proxy = proxy1)

            #代理IP的API
            api = 'http://FQWH123.v4.dailiyun.com/query.txt?key=NPA2F4B388&word=&count=17&rand=false&ltime=0&norepeat=false&detail=false'
            api_r = requests.get(api)
            api_r.encoding = 'gb2312'
            ip=api_r.text
            ip_list = [{'http': ip} for ip in ip.split(':57114\r\n') if ip]
            #print(ip_list)

            if html:
                data_list = []
                url_list = get_url_list(html)
                #print(url_list)
                hwx = 0 #谨以此变量献给该方法的提出者黄文轩sensei

                for url_dict in url_list:
                    hwx = hwx + 1
                    hwx2 = hwx % 17

                    # proxy = random.choice(proxy_list)
                    myproxy = ip_list[hwx2]
                    headers = random.choice(headers_list)

                    url1 = url_dict.get('链接')
                    #print(url)

                    time.sleep(0.5)
                    html = get_the_page2(url1,proxy=myproxy,headers=headers)

                    #print(myproxy)
                    #print(headers)
                    #print(html)

                    if html:
                        #print(url1)
                        dic = parse_the_page(html)#解析话题页
                        #print(dic)
                        dic = {**url_dict, **dic,
                               **{'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}}
                        print(dic)
                        data_list.append(dic)
                    else:
                        print(f'话题页请求失败\n{url_dict}')
                        # pass
                if data_list:
                    df = pd.DataFrame(data_list)
                    filename = 'topsearch' + time.strftime("%Y%m%d")

                    df.to_sql(filename, engine, if_exists='append', index=False)
                    text1 = time.strftime("%Y%m%d %H:%M:%S")
                    print(text1 + '数据写入成功')
            else:
                print('热搜页请求失败')
            end_time = time.perf_counter()
            run_time = end_time - begin_time
            print(run_time)

            if (run_time < 60):
                time.sleep(60 - run_time)
            else:
                time.sleep(0)
        except Exception as e:
            print(e)
            textwarning = time.strftime("%Y%m%d %H:%M:%S")
            print(textwarning+'执行失败')
            time.sleep(1)


