#!/usr/bin/env python
# encoding: utf-8

###############################
# listener文件夹有5334个live的初始听众
# listenerEndIndex存有每个live的最后一次爬取听众的url和index以及高等级听众的uid列表
# 每次爬取听众时首先遍历每天更新的live_id.txt，找出此live最后爬取时的url和index
# 	如果有结果，从最后一次爬取的url开始爬取，大于index的听众为新听众，存入当天的文件夹中
# 	如果没有结果，从第一页开始爬取，存入当天的文件夹中
# 	之后将最新的url和index存入数据库
# 最后遍历第一页听众列表，根据数据库结果查看是否有新增高等级听众，如果有，将新的高等级听众存入当天数据，并更新数据库结果
###############################
# 计算每个live当天和前一天people_count的差值，如果大于0，保存这个live
# 获取live的最后一页听众的url
# 	如果有结果，从最后一次爬取的url开始爬取，存入当天的文件夹中
# 	如果没有结果，从第一页开始爬取，存入当天的文件夹中
# 	之后将最新的url存入数据库
# 最后遍历第一页听众列表，根据数据库结果查看是否有新增高等级听众，如果有，将新的高等级听众存入当天数据，并更新数据库结果
###############################

import requests
import json
import os
from functiontool import time
import pymysql as mysql
import pymysql.cursors
from datetime import datetime,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 以当天日期为名建立文件夹
today = time.strftime('%Y-%m-%d', time.localtime(int(time.time())))
before = (datetime.strptime(today,"%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
if not os.path.exists(today):
	os.mkdir(today)

# 连接数据库
conn = mysql.connect(host="219.224.134.214",user="root",password="",db="zyz",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
conn.autocommit(True)
cur = conn.cursor()
table = 'listenerEndIndex'

xhr_headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
	'Host':'api.zhihu.com',
	'Access-Control-Request-Method':'GET',
	'Connection':'keep-alive'
}

# 保存已存在的live的id到id_list以及过滤器
# b = ScalableBloomFilter(10000,0.001)
# id_list = []
# with open('live_id.txt','r+') as f:
# 	for line in f.readlines():
# 		id = line.strip()
# 		id_list.append(id)
# 		[b.add(id)]
# 查询当天和前一天live的people_count差值，只爬取听众数量差值大于0的
id_list = []
todayDict = {}
with open(today + '/live.json','r+') as f:
	for line in f.readlines():
		j = json.loads(line)
		todayDict.update({j['id']:j['people_count']})
		# try:
		# 	j = json.loads(line)
		# 	todayDict.update({j['id']:j['people_count']})
		# except Exception as e:
		# 	print line
beforeDict = {}
with open(before + '/live.json','r+') as f:
	for line in f.readlines():
		j = json.loads(line)
		beforeDict.update({j['id']:j['people_count']})
for each in todayDict.items():
	todayId = each[0]
	todayPeopleCount = int(each[1])
	try:
		beforePeopleCount = int(beforeDict[todayId])
	except:
		beforePeopleCount = 0
	new_people = todayPeopleCount - beforePeopleCount
	print(new_people)
	if new_people:
		id_list.append(todayId)

# 保存每个live的url和索引
sqlDict = {}
sql = 'select * from %s' % (table)
cur.execute(sql)
for each in cur.fetchall():
	sqlDict.update({each['live_id']:each})

for id in id_list:
	print(id)
	next = True
	# 找到这个live的听众列表最后一个url和最后一个听众的index
	try:
		url = sqlDict[id]['end_url']
		# index = sqlDict[id]['end_index']
		resEmpty = False
	except:
		sqlDict.update({id:{"live_id":id, "end_url":"", "end_index":0, "badges":""}})
		url = 'http://api.zhihu.com/lives/' + str(id) + '/members?limit=100&offset=0'
		# index = 0
		resEmpty = True

	while next:
		while True:
			try:
				print(url.replace("https","http"))
				r = requests.get(url,headers=xhr_headers)
				print(r)
				j = json.loads(r.text)
				j['data']
				break
			except:
				pass
		# num = 0
		for each in j['data']:
			# num += 1
			uid = each['member']['id']
			name = each['member']['name']
			badge = each['badge']['name']
			# if num > index:
			dict0 = {'uid':uid, 'name':name, 'badge':badge}
			with open(today + '/' + str(id) + '.json','a+') as f:
				f.write(json.dumps(dict0,ensure_ascii=False) + '\n')
		if j['paging']['is_end']:
			next = False
			# index = num
		else:
			url = j['paging']['next']
		time.sleep(2)
	# 更新这个live的听众列表最后一个url和最后一个听众的index
	sqlDict[id]["end_url"] = url
	# sqlDict[id]["end_index"] = index

	# 检查是否有新的高等级听众
	try:
		badgeList = sqlDict[id]['badges'].split(',')
	except:
		badgeList = []
	
	url1 = 'http://api.zhihu.com/lives/' + str(id) + '/members?limit=100&offset=0'
	while True:
		try:
			print(url1)
			r1 = requests.get(url1, headers=xhr_headers)
			print(r1)
			j1 = json.loads(r1.text)
			j1['data']
			break
		except:
			pass
	for each in j1['data']:
		if int(each['badge']['id']) != 0:
			if not each['member']['id'] in badgeList:
				badgeList.append(each['member']['id'])
				dict1 = {'uid':each['member']['id'], 'name':each['member']['name'], 'badge':each['badge']['name']}
				with open(today + '/' + str(id) + '.json','a+') as f1:
					f1.write(json.dumps(dict1,ensure_ascii=False) + '\n')
		else:
			break

	sqlDict[id]["badges"] = ','.join(badgeList)

for live_id in sqlDict.keys():
	try:
		sql3 = 'update %s set end_url="%s",end_index=%d,badges="%s" where live_id="%s"' % (table, sqlDict[live_id]["end_url"], sqlDict[live_id]["end_index"], sqlDict[live_id]["badges"], live_id)
		cur.execute(sql3)
	except:
		try:
			sql3 = 'insert into %s(live_id,end_url,end_index,badges) values("%s","%s",%d,"%s")' % (table, live_id, sqlDict[live_id]["end_url"], sqlDict[live_id]["end_index"], sql[live_id]["badges"])
			cur.execute(sql3)
		except:
			with open(today + '/sql.txt','a+') as f:
				f.write(sql3 + '\n')

cur.close()




'''

'''

