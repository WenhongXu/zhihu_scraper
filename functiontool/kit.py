import pandas as pd


def dis_percent(li,ele):
    print(str((li.index(ele)+1)/len(li)*100)+'%')

def distinct(li):
    s=pd.Series(li).drop_duplicates()
    return list(s)

if __name__=='__main__':
    print(distinct([1,2,2,2,3]))
