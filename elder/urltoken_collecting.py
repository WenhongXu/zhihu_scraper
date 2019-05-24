from functiontool.tiny_spider import antcolony_userV4
from functiontool.bloom import bloom
from functiontool.easyRelation import easyRelation
import traceback
import datetime
from functiontool.using_email import send
from functiontool.CanConnect import CanConnect
from functiontool.user_urlV4 import create_userV4

def urltoken_collecting():
    start = datetime.datetime.now()
    #使用过滤器
    mybloom = bloom()
    fordatabase = mybloom.get_from_shelve('token_in_temporary')
    relationbase = easyRelation()
    keys = ['id','url_token']
    print('初始化完成')
    try:
        while True:
            token = relationbase.getone()
            try:
                antcolony_userV4(token,'fensi',fordatabase,'id',relationbase,keylist=keys)
                antcolony_userV4(token,'guanzhu',fordatabase,'id',relationbase,keylist=keys)
            except BaseException as result:
                while True:
                    try:
                        send(traceback.format_exc() + '\n' + str(result) + '\n in ' + datetime.datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S'), __name__ + ' throw '+result.__class__.__name__, '2486296941@qq.com')
                        break
                    except:
                        continue
                while True:
                    if not CanConnect(create_userV4('fensi',token)):
                        continue
                    else:
                        break
            finally:
                relationbase.okone(token)
            if (datetime.datetime.now() - start).seconds > 300:
                print('down')
                break
    finally:
        relationbase.end()
        mybloom.save()
        mybloom.close()



def goo(times):
    p=0
    while p<times:
        try:
            print('第 {0} 次开始'.format(p+1))
            a = datetime.datetime.now()
            urltoken_collecting()
            b = (datetime.datetime.now()-a).seconds
            print('第 {0} 次结束，耗时{1}秒。'.format(p+1,b))
            print('\n\n\n')
            p +=1
            # send('完成了一轮 '+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'正常报告','2486296941@qq.com')
            print(datetime.datetime.now().strftime('%H:%M:%S'))
        except BaseException as result:
            while True:
                try:
                    send(traceback.format_exc()+'\n'+str(result)+' in mainloop at '+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'main error','2486296941@qq.com')
                    break
                except:
                    continue
    send('will stop '+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'Will stop','2486296941@qq.com')












