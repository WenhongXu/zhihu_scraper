#!/usr/bin/env python
# encoding: utf-8

import requests
import json
from pybloom_live import ScalableBloomFilter
import os
from functiontool import time
from selenium import webdriver
from email.mime.text import MIMEText
import smtplib
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

today = time.strftime('%Y-%m-%d', time.localtime(int(time.time())))
if not os.path.exists(today):
    os.mkdir(today)

xhr_headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Host':'api.zhihu.com',
    'Access-Control-Request-Method':'GET',
    'Connection':'keep-alive'
}

# 保存已存在的people的id到id_list以及过滤器
b = ScalableBloomFilter(10000,0.001)
id_list = []
with open('peoples.txt','r+') as f:
    for line in f.readlines():
        id = line.strip()
        id_list.append(id)
        [b.add(id)]

#爬取主持人信息
# display = Display(visible=0, size=(1024, 768))
# display.start()
# driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.get('http://www.zhihu.com/signup?next=%2F#signin')
try:
    driver.find_element_by_xpath('//span[@data-reactid="93"]').click()
except:
    driver.find_element_by_xpath('//div[@class="SignContainer-switch"]/span').click()
driver.find_element_by_xpath('//input[@name="username"]').send_keys('18811748684')
driver.find_element_by_xpath('//input[@name="password"]').send_keys('liang960518')
# driver.find_element_by_xpath('//input[@name="username"]').send_keys('lanleo@126.com')
# driver.find_element_by_xpath('//input[@name="password"]').send_keys('lanleo1989')
driver.find_element_by_xpath('//button[@type="submit"]').click()
time.sleep(20)
req = requests.Session()
cookies = driver.get_cookies()
for cookie in cookies:
    req.cookies.set(cookie['name'],cookie['value'])

for people in id_list:
    print(people)
    people_url = 'http://api.zhihu.com/people/' + people
    r = req.get(people_url,headers=xhr_headers)
    print(r)
    j = json.loads(r.text)

    # try:
    #   error = j['error']
    # except:
    #   pass
    try:
        id = j['id']
    except Exception as e:
        with open("not_id.txt","a") as fw:
            fw.write(people+"\n")

        with open("peoples.txt","r") as fr:
            lines = fr.readlines()
        lines = lines[lines.index(people+"\n"):]
        with open("peoples.txt","w") as fw:
            for line in lines:
                fw.write(line)

        msg = MIMEText('hello, send by Python, the code is stopped', 'plain', 'utf-8')
        smtp = smtplib.SMTP() 
        smtp.connect('smtp.163.com') 
        smtp.login("17801034563@163.com", "20000423hua") 
        smtp.sendmail("17801034563@163.com", ["17801034563@163.com",], msg.as_string()) 
        smtp.quit()

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
    participated_live_count = j['participated_live_count']

    people_dict = {'id':id, 'name':name, 'gender':gender, 'follower_count':follower_count, \
                    'following_count':following_count, 'answer_count':answer_count, \
                    'question_count':question_count, 'articles_count':articles_count, \
                    'columns_count':columns_count, 'pins_count':pins_count, \
                    'voteup_count':voteup_count, 'thanked_count':thanked_count, \
                    'favorited_count':favorited_count, 'hosted_live_count':hosted_live_count, \
                    'live_count':live_count, 'participated_live_count':participated_live_count}
    # with open(today + '/people.json','a+') as f:
    with open(today + '/people.json','a+') as f:
        f.write(json.dumps(people_dict,ensure_ascii=False) + '\n')
    time.sleep(1)

try:
    driver.quit()
except:
    pass

'''

'''