# -*- coding: utf-8 -*-
# @Author: Vincent Xu
# @E-mail: wenhong0815@qq.com
# For my Graduation Design about RS
# import sqlite3
# conn = sqlite3.connect('temporary.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE id2token
#        (ID CHAR(100) PRIMARY KEY     NOT NULL,
#        TOKEN           char(100)   NOT NULL  UNIQUE)''')
# conn.commit()
# conn.close()
import sqlite3
from pybloom_live import ScalableBloomFilter

class easyRelation():
    '''
    顾名思义，简单的关系数据库，使用sqlite数据库，仅仅适用于“简单的关系”
    主要是因为对于大量数据而言，使用python的列表或者队列都很耗内存，且查询低效
    故有此类，多为二元表+状态标识
    但是因为比较easy，也没有更多功能
    '''

    def __init__(self):
        self.conn = sqlite3.connect('temporary.db')
        self.c = self.conn.cursor()
        print(__name__+' need to end')
        

    def getCursor(self):
        '''
        返回游标和数据库连接
        可以用于执行其他的sql语句
        '''
        return (self.c,self.conn)

    def insertID_TOKEN(self, uid, url_token):
        '''
        插入一个id和token的对应关系
        '''
        try:
            self.c.execute(
                'INSERT INTO id2token (ID,TOKEN) VALUES (\'{0}\',\'{1}\')'.format(uid, url_token))
            self.conn.commit()
        except:
            self.conn.close()
            self.conn = sqlite3.connect('temporary.db')
            self.c = self.conn.cursor()

    def insert(self,dic):
        '''
        与insertID_TOKEN的区别只是接收一个字典为参数
        字典键包括 id url_token
        '''
        uid = dic['id']
        url_token = dic['url_token']
        try:
            self.c.execute(
                'INSERT INTO id2token (ID,TOKEN,ISPROCESS) VALUES (\'{0}\',\'{1}\',0)'.format(uid, url_token))
            self.conn.commit()
        except:
            self.conn.close()
            self.conn = sqlite3.connect('temporary.db')
            self.c = self.conn.cursor()
    def delone(self,token):
        '''
        按照token删除一条记录
        '''
        self.c.execute('DELETE FROM id2token where TOKEN=\''+token+'\'')
        self.conn.commit()

    def createindex(self):
        '''
        创建索引
        '''
        self.c.execute('create index if not exists idindex on id2token(ID);')
        self.conn.commit()
        self.c.execute('create index if not exists tokenindex on id2token(TOKEN);')
        self.conn.commit()
        self.c.execute('create index if not exists isindex on id2token(ISPROCESS);')
        self.conn.commit()
    def getone(self):
        '''
        在未处理的数据中取一条来处理
        '''
        cur = self.c.execute(
            'SELECT TOKEN from id2token WHERE ISPROCESS=0 LIMIT 1')
        c=None
        for row in cur:
            c=row[0]
            break
        return c

    def okone(self,token):
        '''
        标识该记录已经被处理过
        '''
        self.c.execute('update id2token set ISPROCESS=1 where TOKEN = \'' + token + '\'')
        self.conn.commit()


    def getResult(self, key, mood='VIA_TOKEN'):
        '''
        查询
        '''
        if mood == 'VIA_TOKEN':
            cur = self.c.execute(
                'SELECT ID from id2token WHERE TOKEN=\'' + str(key)+ '\'')
            for row in cur:
                return row[0]
        elif mood == 'VIA_ID':
            cur = self.c.execute(
                'SELECT TOKEN from id2token WHERE ID=\'' + str(key) + '\'')
            for row in cur:
                return row[0]

    def __del__(self):
        pass

    def end(self):
        '''
        应该被显式的关闭
        '''
        self.conn.close()
        self.__del__()
    def total(self):
        '''
        返回目前数据库中的记录总数
        '''
        cc = self.c.execute('''SELECT * FROM id2token''')
        r = cc.fetchall()
        return len(r)
    def fiktergenerator(self,mode):
        '''
        从数据库某一字段读取生成过滤器
        '''
        if 'token' in mode:
            mode = 'TOKEN'
        if 'id' in mode:
            mode = 'ID'
        cc = self.c.execute('SELECT '+mode+' FROM id2token')
        r = cc.fetchall()
        bloom = ScalableBloomFilter(100000000,0.001)
        for i in r:
            bloom.add(i[0])
        return bloom




if __name__ == '__main__':
    ea = easyRelation()
    # # ea.insertID_TOKEN('aaaaaaaaaaa','aaaaaaaaaaaaaa')
    # print(ea.getResult('aaaaaaaaaaa', mood='VIA_ID'))
    ea.fiktergenerator('url_token')
