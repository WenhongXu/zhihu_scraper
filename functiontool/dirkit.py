import os
from functiontool.templib import temp_stupid
def getdir(path,fil=None,pre='.txt',to='dir.txt',display = False):
    filePath = path
    lis=os.listdir(filePath)
    if pre:
        lis = [x.replace(pre,'') for x in lis]
    if fil:
        lis = list(filter((lambda x:True if x not in fil else False),lis))
    temp_stupid(to).update(lis)
    if display:
        print(lis)
    return lis

if __name__ =='__main__':
    getdir('./',['constant'],'.py')