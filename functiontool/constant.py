# -*- coding: utf-8 -*-
# @Author: Vincent Xu
# @E-mail: wenhong0815@qq.com
# For my Graduation Design about RS
import requests
from functiontool.constant_cookies import COOKIES_V4 as cookies
XHR_HEADER_WZ = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Host': 'www.zhihu.com',
    'Access-Control-Request-Method': 'GET',
    'Connection': 'keep-alive'
}

XHR_HEADER_API = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Host': 'api.zhihu.com',
    'Access-Control-Request-Method': 'GET',
    'Connection': 'keep-alive'
}

def getRequest(havecookie=True):
    '''
    返回一个request.session对象
    该函数存在的意义是设置cookie
    '''
    req = requests.Session()
    if havecookie is False:
        return req
    for cookie in cookies:
        req.cookies.set(cookie['name'], cookie['value'])
    return req

tags = [101, 102, 103, 104, 105, 106, 107, 108,109, 201, 202, 203, 301, 302, 303, 304, 305]
