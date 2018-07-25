#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/7/25 00:29
# @Author  : capton
# @FileName: ip_source.py
# @Software: PyCharm
# @Blog    : http://ccapton.cn
# @Github  : https://github.com/ccapton
# @Email   : chenweibin1125@foxmail.com

from bs4 import BeautifulSoup
import requests
import json
import time


class IpLocationFinder:
    def __init__(self,url):
        self.url = url
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
    def get_response(self):
        return ''

    def get_ip_address(self):
        return '',''

    def cost_time(self):
        return 0.000000

    def is_chinese_ip(self):
        return False


# ip 查询源 一
# Request URL: http://ip.chinaz.com/getip.aspx
# Request Method: GET
# Status Code: 200 OK
# Remote Address: 103.205.5.66:80
# Referrer Policy: no-referrer-when-downgrade

# Cache-Control: private
# Content-Encoding: gzip
# Content-Length: 195
# Content-Type: text/html; charset=utf-8
# Date: Tue, 24 Jul 2018 16:17:19 GMT
# Server: Microsoft-IIS/8.5
# Vary: Accept-Encoding
# X-AspNet-Version: 4.0.30319
# X-Powered-By: ASP.NET
# Provisional headers are shown

# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

# http://ip.chinaz.com/getip.aspx
class Finder1(IpLocationFinder):
    def get_response(self):
        return  requests.get(self.url,headers = self.headers).content.decode(encoding='utf8')

    def get_ip_address(self):
        source = self.get_response()
        items = source[1:len(source) - 1].split(',')
        ip = ''
        address = ''
        for item in items:
            key = item.split(':')[0]
            value = item.split(':')[1].replace('\'', '')
            if key == 'ip':
                ip = value
            if key == 'address':
                address = value
        return ip,address

# ip 查询源 一
# https://ip.cn/index.php
# Request URL: https://ip.cn/
# Request Method: GET
# Status Code: 200
# Remote Address: 104.16.24.88:443

# Referrer Policy: unsafe-url
# cf-ray: 43f7c8245924770c-LAX
# content-encoding: br
# content-type: text/html; charset=UTF-8
# date: Tue, 24 Jul 2018 16:32:16 GMT
# expect-ct: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
# server: cloudflare
# status: 200

# :authority: ip.cn
# :method: GET
# :path: /
# :scheme: https
# accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# accept-encoding: gzip, deflate, br
# accept-language: zh-CN,zh;q=0.9,en;q=0.8
# cache-control: max-age=0
# cookie: __cfduid=d95b2f1efccdfa1270d087c0ef8ae8dba1532449486; UM_distinctid=164cd1b84d5797-0e56e7b9544419-16396952-13c680-164cd1b84d62bc; CNZZDATA123770=cnzz_eid%3D1343145752-1532447771-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1532447771
# referer: https://ip.cn/
# upgrade-insecure-requests: 1
# user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

# 关键 <div id="result"><div class="well"><p>您现在的 IP：<code>183.12.236.117</code></p><p>所在地理位置：<code>广东省深圳市 电信</code></p><p>GeoIP: Shenzhen, Guangdong, China</p></div>

# https://ip.cn/index.php  get 参数 id =
class Finder2(IpLocationFinder):
    def get_response(self):
        # self.headers[':authority'] = 'ip.cn'
        # self.headers[':method'] = 'GET'
        # self.headers[':scheme'] = 'https'
        self.headers['cache-control'] = 'max-age=0'
        self.headers['referer'] = 'https://ip.cn/'
        self.headers['upgrade-insecure-requests'] = '1'
        response = requests.get(self.url,headers = self.headers,params={'id':'45.63.124.188'})
        if response.status_code == 200:
            return response.content
        return ''

    def get_ip_address(self):
        source = self.get_response()
        soup = BeautifulSoup(source, 'html.parser')
        print(source)
        ip_and_addr =  soup.find('div', attrs={'id': 'result'}).find_all('code')
        ip =ip_and_addr[0].text
        address = ip_and_addr[1].text
        return ip,address

    def is_chinese_ip(self):
        try:
           source = self.get_response()
           soup = BeautifulSoup(source, 'html.parser')
           #well_text = soup.find('div', attrs={'class': 'well'})
           print(soup.text)
           print(soup.text.find('China'))
           if soup.text.find('China') != -1:
               return True
           else:
               return False
        except Exception as e:
            print(e)
            print('xx'*30)
        return True


def is_chinese_user():
    locationFinder2 = Finder2('https://ip.cn/index.php')
    result = locationFinder2.is_chinese_ip()
    return result



if __name__ == '__main__':
    print(is_chinese_user())
    #print('美国'.find('China'))








