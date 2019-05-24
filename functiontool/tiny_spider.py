# coding: utf-8
'''
本文件以函数形式给出全部的个体爬虫
以tiny开头的爬虫用于一次获取基本信息
以worn开头的爬虫用于处理翻页操作，目前还没能变为生成器，后续如有必要，可做优化
以上所述的函数都是有返回值的
以antcolony开头的爬虫没有返回值，传入数据库对象，它会自动插入，因此内存开销少一些，但也缺乏
没有经过调试
'''
import json
import time
from functiontool.constant import getRequest, XHR_HEADER_API, XHR_HEADER_WZ
from functiontool.user_urlV4 import *
from functiontool.exceptions import *
from pybloom_live import ScalableBloomFilter
import time


def tiny_people(req, people, xhr_headers=XHR_HEADER_API):
    print(people)
    people_url = 'http://api.zhihu.com/people/' + people

    r = req.get(people_url, headers=xhr_headers, timeout=5)
    print('gotten')
    if int(r.status_code) in [403,405,401]:
        raise WrongStatuCode(str(r.status_code)+': '+people_url)
    j = json.loads(r.text,encoding='utf-8')
    if 'error' in j:
        raise ErrorInJson(__name__+": from url="+'http://api.zhihu.com/lives/'+'\n  msg='+str(j['error']))
    name = j['name']
    gender = j['gender']
    follower_count = j['follower_count']
    following_count = j['following_count']
    answer_count = j['answer_count']
    question_count = j['question_count']
    articles_count = j['articles_count']
    columns_count = j['columns_count']
    pins_count = j['pins_count']
    voteup_count = j['voteup_count']
    thanked_count = j['thanked_count']
    favorited_count = j['favorited_count']
    hosted_live_count = j['hosted_live_count']
    live_count = j['live_count']
    id = j['id']
    participated_live_count = j['participated_live_count']
    url_token = j['url_token']
    people_dict = {'id': id, 'name': name, 'url_token': url_token, 'gender': gender, 'follower_count': follower_count,
                   'following_count': following_count, 'answer_count': answer_count,
                   'question_count': question_count, 'articles_count': articles_count,
                   'columns_count': columns_count, 'pins_count': pins_count,
                   'voteup_count': voteup_count, 'thanked_count': thanked_count,
                   'favorited_count': favorited_count, 'hosted_live_count': hosted_live_count,
                   'live_count': live_count, 'participated_live_count': participated_live_count}
    return people_dict


def tiny_live(id, req, xhr_headers=XHR_HEADER_API):
    '''
    几乎复制了学长的代码，返回字段也是类似的
    '''
    print(id)
    live_url = 'http://api.zhihu.com/lives/' + str(id)
    r = req.get(live_url, headers=xhr_headers)
    if int(r.status_code) ==400:
        raise ErrorInJson(str(r.status_code)+': '+live_url)
    if int(r.status_code) >300:
        raise WrongStatuCode(str(r.status_code)+': '+live_url)
    print(r.text)
    j = json.loads(r.text,encoding='utf-8')
    if 'error' in j:
        raise ErrorInJson(__name__+": from url="+'http://api.zhihu.com/lives/'+'\n  msg='+j['error'])
    id = j['id']
    subject = j['subject']
    outline = j['outline']
    attachment_count = j['attachment_count']
    audio_duration = int(j['audio_duration'] / 60)
    reply_message_count = j['reply_message_count']
    speaker_audio_message_count = j['speaker_audio_message_count']
    speaker_message_count = j['speaker_message_count']
    if j['tags']:
        tags = [each['name'] for each in j['tags']]
    else:
        tags = []
    speaker = j['speaker']['member']['id']
    if j['cospeakers']:
        cospeakers = [each['member']['id'] for each in j['cospeakers']]
    else:
        cospeakers = []
    description = j['description_html']
    created_at = time.strftime('%Y-%m-%d', time.localtime(j['created_at']))
    starts_at = time.strftime('%Y-%m-%d', time.localtime(j['starts_at']))
    ends_at = time.strftime('%Y-%m-%d', time.localtime(j['ends_at']))
    original_price = j['fee']['original_price'] / 100
    fee = j['fee']['amount'] / 100
    purchasable = j['purchasable']
    is_refundable = j['is_refundable']
    in_promotion = j['in_promotion']
    has_audition = j['has_audition']
    liked_num = j['liked_num']
    people_count = j['seats']['taken']
    review_count = j['review']['count']
    review_score = j['review']['score']
    feedback_score = j['feedback_score']
    live_dict = {'id': id, 'subject': subject, 'attachment_count': attachment_count,
                 'audio_duration': str(audio_duration), 'reply_message_count': reply_message_count,
                 'speaker_audio_message_count': speaker_audio_message_count,
                 'tags': tags, 'speaker': speaker, 'cospeakers': cospeakers,
                 'speaker_message_count': speaker_message_count,
                 'description': description, 'created_at': created_at,
                 'starts_at': starts_at, '​ends_at': ends_at,
                 'original_price': original_price, 'fee': fee,
                 'purchasable': purchasable, 'is_refundable': is_refundable,
                 'in_promotion': in_promotion, 'has_audition': has_audition,
                 'liked_num': liked_num, 'people_count': people_count,
                 'review_count': review_count, 'review_score': review_score,
                 'feedback_score': feedback_score,'outline':outline}
    return json.dumps(live_dict,ensure_ascii=False)


def tiny_topic(id, req, xhr_headers=XHR_HEADER_WZ):

    url = 'https://www.zhihu.com/api/v4/topics/' + id
    r = req.get(url, headers=xhr_headers)
    if int(r.status_code) >300:
        raise WrongStatuCode(str(r.status_code)+': '+url)
    j = json.loads(r.text,encoding='utf-8')
    if 'error' in j:
        raise ErrorInJson(__name__+": from url="+'https://www.zhihu.com/api/v4/topics/'+'\n  msg='+j['error'])
    return j

def tiny_speciallist(id, req, xhr_headers=XHR_HEADER_API):
    url = 'https://api.zhihu.com/lives/special_lists/' + id
    r = req.get(url, headers=xhr_headers)
    if int(r.status_code) >300:
        raise WrongStatuCode(str(r.status_code)+': '+url)
    j = json.loads(r.text,encoding='utf-8')
    if 'error' in j:
        raise ErrorInJson(__name__+": from url="+'https://api.zhihu.com/lives/special_lists/'+'\n  msg='+j['error'])
    return j

def worm_userV4(token,domain,keylist=None,bloom=None,lamda=20,xhr_headers=XHR_HEADER_API):
    def keyconvert(keys,dict):
        c={}
        for key in dict.keys():
            if key in keys:
                c[key]=dict[key]
        return c
    def convert(bloom,data):
        def istrue(bloom,ok):
            if ok['url_token'] in bloom:
                return False
            else:
                return True
        c=[]
        for i in data:
            if istrue(bloom,i):
                c.append(i)
        return c
    urlhead = create_userV4(domain,token)
    req = getRequest()
    people_url = urlhead+paging(0,5)
    r = req.get(people_url, headers=xhr_headers)
    if int(r.status_code) >300:
        raise WrongStatuCode(str(r.status_code)+': '+people_url)
    j = json.loads(r.text)
    if 'error' in j:
        raise ErrorInJson(__name__+": from url="+urlhead+'\n  msg='+j['error'])
    print(j['paging'])
    alldata=[]
    try:
        total = int(j['paging']['totals'])
    except:
        total = None
    if total:
        print(total)
        print(round(total / lamda))
        for i in range(round(total / lamda) + 1):
            urll = urlhead+paging(i*lamda,lamda)
            r = req.get(urll, headers=xhr_headers)
            # print(r)
            jc = json.loads(r.text,encoding='utf-8')
            data = jc['data']
            if keylist:
                data = [keyconvert(keylist,x) for x in data]
            if bloom:
                data = convert(bloom,data)
            print(data)
            alldata=alldata+data
    else:
        i=0
        while True:
            urll = urlhead + paging(int(i*lamda),lamda)
            r = req.get(urll, headers=xhr_headers)
            jc = json.loads(r.text, encoding='utf-8')
            data = jc['data']
            if len(data) == 0:
                break
            if keylist:
                data = [keyconvert(keylist,x) for x in data]
            if bloom:
                data = convert(bloom,data)
            print(data)
            alldata=alldata+data
            i=i+1
    return alldata

def antcolony_userV4(token,domain,bloom:ScalableBloomFilter,key:str,dataobject,keylist=None,lamda=20,xhr_headers=XHR_HEADER_WZ):
    def keyconvert(keys,dict):
        c={}
        for key in dict.keys():
            if key in keys:
                c[key]=dict[key]
        return c
    urlhead = create_userV4(domain,token)
    req = getRequest()
    people_url = urlhead+paging(0,5)
    print(people_url)
    print('before r')
    r = req.get(people_url, headers=xhr_headers)
    print('after r')
    if int(r.status_code) == 410:
        dataobject.delone(token)
        return 0
    if int(r.status_code) >300:
        raise WrongStatuCode(str(r.status_code)+': '+people_url)
    j = json.loads(r.text)
    if 'error' in j:
        raise ErrorInJson(__name__+": from url="+urlhead+'\n  msg='+j['error'])
    print(j['paging'])
    try:
        total = int(j['paging']['totals'])
    except:
        total = None
    if total:
        print(total)
        print(round(total / lamda))
        for i in range(round(total / lamda) + 1):
            urll = urlhead+paging(i*lamda,lamda)
            r = req.get(urll, headers=xhr_headers)
            # print(r)
            jc = json.loads(r.text,encoding='utf-8')
            data = jc['data']

            if keylist:
                data = [keyconvert(keylist,x) for x in data]
            for i in data:
                if i[key] not in bloom:
                    dataobject.insert(i)
                    bloom.add(i[key])
                    print('data import ' + i[key])
                else:
                    print('pass')
    else:
        i = 0
        while True:
            urll = urlhead + paging(int(i*lamda),lamda)
            r = req.get(urll, headers=xhr_headers)
            jc = json.loads(r.text, encoding='utf-8')
            data = jc['data']
            if len(data) == 0:
                break
            if keylist:
                data = [keyconvert(keylist,x) for x in data]
            for c in data:
                if c[key] not in bloom:
                    dataobject.insert(c)
                    bloom.add(c[key])
                    print('data import ' + c[key])
                else:
                    print('pass')
            i+=1








if __name__ == '__main__':
    req = getRequest()
    print(tiny_speciallist('1020409341244997632', req, XHR_HEADER_API))
