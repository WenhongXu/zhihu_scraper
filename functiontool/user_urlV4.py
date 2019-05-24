# -*- coding: utf-8 -*-
# @Author: Vincent Xu
# @E-mail: wenhong0815@qq.com
# For my Graduation Design about RS
'''
依据API的url构造
'''
from functiontool.exceptions import NoSuchLiveTag
from functiontool.constant import tags
from functiontool.constant import XHR_HEADER_API,XHR_HEADER_WZ
def create_userV4(domain, urltoken):
    '''
    domain: 请使用以下中文词汇的拼音[粉丝，关注，专栏，问题，收藏夹，答案，话题，活动]
    urltoken: 如变量名所示，你需要给出用户的url_token
    '''
    header_v4 = 'https://www.zhihu.com/api/v4/members/'
    user_dict = {
        'fensi': 'followers',
        'guanzhu': 'followees',
        'zhuanlan': 'following-columns',
        'wenti': 'following-questions',
        'shoucangjia': 'following-favlists',
        'daan': 'answers',
        'huati': 'following-topic-contributions',
        'huguan': 'relations/mutuals',
        'huodong':'activities'
    }
    if domain == 'lives':
        return 'https://api.zhihu.com/people/'+urltoken+'/lives'
    return header_v4 + urltoken+'/'+user_dict[domain]


def create_topic(id):
    return 'https://www.zhihu.com/api/v4/topics/' + id

def paging(offset:int = 0,limit:int = 10):
    return '?offset='+str(offset)+'&'+'limit='+str(limit)

def create_lives_from_people(id):
    return 'https://api.zhihu.com/people/'+id+'/lives'
def create_people(id:'token or id'):
    return 'https://api.zhihu.com/people/'+id
def create_live(id):
    return 'http://api.zhihu.com/lives/'+id
def create_live_review(id):
    return 'https://api.zhihu.com/lives/'+id+'/reviews'
def create_speciallist(id):
    return 'https://api.zhihu.com/lives/special_lists/'+id
def create_lives_in_speciallist(id):
    return 'https://api.zhihu.com/lives/special_lists/'+id+'/lives'


def create_live_list(tag):
    if int(tag) in tags:
        return 'http://api.zhihu.com/lives/ongoing?tags='+str(tag)
    else:
        raise NoSuchLiveTag(tags)
def create_speciallist_list(mode='special_list'):
    return 'https://api.zhihu.com/lives/special_lists?subtype='+mode


def judge_header(url:str):
    if 'api.zhihu.com' in url:
        return XHR_HEADER_API
    elif 'www.zhihu.com' in url:
        return XHR_HEADER_WZ
