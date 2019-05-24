# -*- coding: utf-8 -*-
# @Author: Vincent Xu
# @E-mail: wenhong0815@qq.com
# For my Graduation Design about RS

from functiontool.exceptions import ReadOnlyError, WriteOnlyError,NoMoreLine,BadTemp
import json

class temp_stupid:
    '''
    临时文件操作，取名为stupid是因为内存未优化，逻辑暴力
    '''

    def __init__(self, message=None):
        '''
        store temporary list via txt file
        message: 文件名
        '''
        self.message = message

    def save(self,ob):
        '''
        保存新增内容
        ob: 一个一维列表
        '''
        li = list(ob)
        li = [str(x) for x in li]
        w = open(self.message, 'a',encoding='utf-8')
        w.write('\n'.join(li))
        w.write('\n')
        w.close()

    def update(self,ob):
        '''
        更新整个文件
        ob: 一个一维列表
        '''
        li = list(ob)
        li = [str(x) for x in li]
        w = open(self.message, 'w',encoding='utf-8')
        w.write('\n'.join(li))
        w.write('\n')
        w.close()

    def read(self):
        '''
        读取整个文件，以列表形式返回
        '''
        fi = open(self.message, 'r',encoding='utf-8')
        po = []
        while True:
            line = fi.readline()
            if not line:
                break
            else:
                if not str(line).strip() == '':
                    po.append(str(line).strip())
        fi.close()
        return po

    def clear(self):
        '''
        清空文件内容
        '''
        fi = open(self.message, 'w',encoding='utf-8')
        fi.close()
        
class tempflow:
    '''
    实现的功能与temp_stupid相同，只不过没那么暴力
    用来一个一个的读取文件行，所以命名中有flow
    '''

    def __init__(self, message, mode):
        '''
        message: name of file
        mode: 'a','w','r' and so on
        '''
        self.file = open(message, mode,encoding='utf-8')
        self.canw = True
        self.canr = True
        if 'r' == mode:
            self.canw = False
        if 'w' == mode or 'a' == mode:
            self.canr = False

    def __del__(self):
        '''
        delete the instance of the class explicitly
        '''
        pass

    def writein(self, li):
        '''
        write in list
        '''

        if self.canw is False:
            raise ReadOnlyError(
                'tempFileProcess || using tempflow, this file is Read only, you can use readone()')
        self.canr = False

        li = [str(x) for x in li]
        self.file.write('\n'.join(li))
        self.file.write('\n')

    def readone(self):
        if self.canr is False:
            raise WriteOnlyError(
                'tempFileProcess || using tempflow, this file is Write only, you can use writein()')
        self.canw = False
        line = self.file.readline()
        if not line:
            raise NoMoreLine
        elif not str(line).strip() == '':
            value = str(line).strip()
        else:
            value = self.readone()
        return value

    def end(self):
        self.file.close()
        self.__del__()

def tempjson2csv(fro,to,singlequotation=False):
    x=temp_stupid(fro).read()
    p=[]
    for i in x:
        try:
            if singlequotation:
                i = i.replace('\'','\"')
            p.append(json.loads(i))
        except:
            raise BadTemp(str(i))
    import pandas as pd
    pd.DataFrame(p).to_csv(to,index=False)




if __name__ == '__main__':
    li = [1, 2, 3, 4]
    tem = tempflow('test', 'r')
    while True:
        c = tem.readone()
        if not c:
            break
        print(c)
    tem.writein(li)
