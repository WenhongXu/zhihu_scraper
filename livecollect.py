import pandas as pd
import numpy as np
from functiontool.templib import temp_stupid,tempflow
from functiontool.tiny_spider import tiny_live
from functiontool.constant import getRequest,XHR_HEADER_API
import json
from functiontool.using_email import send
import traceback
import datetime
from functiontool.bloom import bloom
from functiontool.CanConnect import CanConnect
from functiontool.user_urlV4 import create_live
from pybloom_live import ScalableBloomFilter
from functiontool.exceptions import WrongStatuCode,ErrorInJson
# seed = pd.read_csv('count.csv',header=0,index_col='uid',names=['inde','times','uid'])
# del seed['inde']
# seedsorted=seed.sort_values(by='times',ascending=False)
# x = list(seedsorted[seedsorted.times>3].index)
# print(len(x))
def forlive(num):
    bloom = ScalableBloomFilter(1000000,0.001)
    havedone = temp_stupid('live.txt').read()
    error = temp_stupid('errorlive.txt').read()
    for i in havedone:
        try:
            ii=json.loads(i)['id']
        except:
            continue
        bloom.add(ii)
    for i in error:
        bloom.add(i)
    temp = temp_stupid('need.txt')
    see = temp.read()
    sc = tempflow('live.txt','a')
    seed=[]
    for i in see:
        if i not in bloom:
            seed.append(i)
    for i in seed[:num]:
        #tempp=temp_stupid(i+'txt')
        if i.startswith(u'\ufeff'):
            i = i.encode('utf8')[3:].decode('utf8')
        try:
            userdict = tiny_live(i,getRequest())
            sc.writein([userdict])
            print(i)
        except ErrorInJson as result:
            temp_stupid('errorlive.txt').save([i])
        except BaseException as result:
            for e in range(10):
                try:
                    send(traceback.format_exc() + '\n' + str(result) + '\n in ' + datetime.datetime.now().strftime(
                        '%Y-%m-%d %H:%M:%S'), __name__ + ' throw '+result.__class__.__name__, '2486296941@qq.com')
                    break
                except BaseException as res:
                    print(res)
                    continue
            while True:
                if not CanConnect(create_live(i),XHR_HEADER_API):
                    continue
                else:
                    break
    sc.end()