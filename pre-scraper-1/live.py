#!/usr/bin/env python
# encoding: utf-8

import requests
import json
from pybloom_live import ScalableBloomFilter
import os
import time
# 以当天日期为名建立文件夹
today = time.strftime('%Y-%m-%d', time.localtime(int(time.time())))
if not os.path.exists(today):
    os.mkdir(today)

xhr_headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Host':'api.zhihu.com',
    'Access-Control-Request-Method':'GET',
    'Connection':'keep-alive'
}

# 保存已存在的live的id到id_list以及过滤器
b = ScalableBloomFilter(10000,0.001)
id_list = []
with open('live_id.txt','r+') as f:
    for line in f.readlines():
        id = line.strip()
        id_list.append(id)
        [b.add(id)]

# 保存已存在的people的id到过滤器
bb = ScalableBloomFilter(10000,0.001)
with open('peoples.txt','r+') as f:
    for line in f.readlines():
        id = line.strip()
        if not id in bb:
            [bb.add(id)]

# # 找出所有最新的live，去重，存在id_list和过滤器以及文件中

tag_list = [101,102,103,104,105,106,107,108,109,201,202,203,301,302,303,304,305]
for tag in tag_list:
    url = 'http://api.zhihu.com/lives/ongoing?tags=' + str(tag) + '&limit=1000&offset=0'
    r = requests.get(url,headers=xhr_headers)

    j = json.loads(r.text)
    data = j['data']

    for d in data:
        id = d['id']
        if not id in b:
            [b.add(id)]
            id_list.append(id)
            with open('live_id.txt','a+') as f:
                f.write(id + '\n')

#爬取详细信息
for id in id_list:
    print(id)
    live_url = 'http://api.zhihu.com/lives/' + str(id)
    r = requests.get(live_url, headers=xhr_headers)
    print(r)
    j = json.loads(r.text)
    try:
        error = j['error']
        continue
    except:
        pass
    id = j['id']
    subject = j['subject']
    attachment_count = j['attachment_count']
    audio_duration = int(j['audio_duration']/60)
    reply_message_count = j['reply_message_count']
    speaker_audio_message_count = j['speaker_audio_message_count']
    speaker_message_count = j['speaker_message_count']
    if j['tags']:
        tags = [each['name'] for each in j['tags']]
    else:
        tags = []
    speaker = j['speaker']['member']['id']
    if not speaker in bb:
        [bb.add(speaker)]
        with open('peoples.txt','a+') as f:
            f.write(speaker + '\n')
    if j['cospeakers']:
        cospeakers = [each['member']['id'] for each in j['cospeakers']]
    else:
        cospeakers = []
    description = j['description_html']
    created_at = time.strftime('%Y-%m-%d', time.localtime(j['created_at']))
    starts_at = time.strftime('%Y-%m-%d', time.localtime(j['starts_at']))
    ends_at = time.strftime('%Y-%m-%d', time.localtime(j['ends_at']))
    original_price = j['fee']['original_price']/100
    fee = j['fee']['amount']/100
    purchasable = j['purchasable']
    is_refundable = j['is_refundable']
    in_promotion = j['in_promotion']
    has_audition = j['has_audition']
    liked_num = j['liked_num']
    people_count = j['seats']['taken']
    review_count = j['review']['count']
    review_score = j['review']['score']
    feedback_score = j['feedback_score']
    live_dict = {'id':id, 'subject':subject, 'attachment_count':attachment_count, \
                    'audio_duration':str(audio_duration), 'reply_message_count':reply_message_count, \
                    'speaker_audio_message_count':speaker_audio_message_count, \
                    'tags':tags, 'speaker':speaker, 'cospeakers':cospeakers, \
                    'speaker_message_count':speaker_message_count, \
                    'description':description, 'created_at':created_at, \
                    'starts_at':starts_at, '​ends_at':ends_at, \
                    'original_price':original_price, 'fee':fee, \
                    'purchasable':purchasable, 'is_refundable':is_refundable, \
                    'in_promotion':in_promotion, 'has_audition':has_audition, \
                    'liked_num':liked_num, 'people_count':people_count, \
                    'review_count':review_count, 'review_score':review_score, \
                    'feedback_score':feedback_score}

    # with open(today + '/live.json','a+') as f:
    with open(today + '/live.json','a+') as f:
        f.write(json.dumps(live_dict,ensure_ascii=False) + '\n')

# msg = MIMEText('The live.py has finisied, live_id.txt is formal', 'plain', 'utf-8')
# smtp = smtplib.SMTP() 
# smtp.connect('smtp.163.com') 
# smtp.login("bhxg_zl@163.com", "liang180310") 
# smtp.sendmail("bhxg_zl@163.com", ["bhxg_zl@163.com",], msg.as_string()) 
# smtp.quit()