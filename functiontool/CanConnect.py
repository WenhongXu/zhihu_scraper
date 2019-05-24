from functiontool.constant import getRequest, XHR_HEADER_WZ
'''
405:知乎反作弊
410:账号停用或注销
403:表明爬虫被ban
'''

def CanConnect(url,header = XHR_HEADER_WZ):
    '''
    测试连接是否被ban（即是否返回403状态码）
    url: 用于测试的链接
    header: 默认为www.zhihu.com主机，如果是api.zhihu.com必须更换
    '''
    req = getRequest()
    r = req.get(url,headers = header)
    if int(r.status_code) in [401,403]:
        return False
    else:
        return True
