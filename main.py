# from urltoken_collecting import *
# goo(60)
# from functiontool.using_email import send
# from functiontool.bloom import bloom
# # bl = bloom()

from livecollect import forlive
import time
while True:
    forlive(100)
    print('#############  wait another turn  ##############')
    time.sleep(3)

# from functiontool.temp_stupid import temp_stupid
# import json
# x = temp_stupid('ouruser.txt').read()
# x=x[:33]
# t=[]
# for i in x:
#     if i.startswith(u'\ufeff'):
#         i = i.encode('utf8')[3:].decode('utf8')
#     t.append(i)
# print(t)
# import shelve
# x=shelve.open('bloom')
# print(list(x.keys()))
# import pandas as pd
# from functiontool.templib import temp_stupid
# seed = pd.read_csv('count.csv',header=0,index_col='uid',names=['inde','times','uid'])
# del seed['inde']
# seedsorted=seed.sort_values(by='times',ascending=False)
# seedsorted=seedsorted[seedsorted.times>3]
# x = list(seedsorted[seedsorted.times==18].index)
# temp_stupid('is18.txt').update(x)
# from functiontool.templib import temp_stupid
# from functiontool.dirkit import getdir
# from pybloom_live import ScalableBloomFilter
# import datetime
# import json
# x = temp_stupid('5livelist.txt').read()
# p = getdir('./gooduser/',['xxx.txt'],pre = None)
# bloom = ScalableBloomFilter(100000,0.001)
# for i in x:
#     data = []
#     for j in p:
#         if i in [json.loads(x.replace('\'','\"'))['id'] for x in temp_stupid('./gooduser/'+j).read()]:
#             data.append(j.replace('.txt',''))
#             print(j)
#     temp_stupid('./goodlive/'+i+'.txt').update(data)
#     print(i)
# for i in p:
#     print(i)
#     for j in [json.loads(x.replace('\'','\"'))['id'] for x in temp_stupid('./gooduser/'+i).read()]:
#         temp_stupid('./goodlive/'+j+'.txt').save([i.replace('.txt','')])



            


