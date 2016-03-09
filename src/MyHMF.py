# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random
import math
from pandas import *


#划分数据
def SplitData(M,k,seed):
    for line in open('user_ratedmovies-timestamps.dat'):#将数据放在data列表里
        user,item,record,time =line.split('	')
        data.append([int(user),int(item),float(record),long(time)])
#    print data[10]
        
    for user,item,record,time in data:
        timeset.setdefault(item,[])
        timeset[item].append(time)#记录电影的时间
    
    for item in timeset:
        timeminset[item]=sorted(timeset[item])[0]#找到电影最早的时间
#    print timeminset[item]
        
    random.seed(seed)
    for user,item,record,time in data:
        if random.randint(0,M) == k:
            test.append((user,item,record,time))
        else:
            train.append((user,item,record,time))
    a=9151236610000L
    for i in timeminset:
        if timeminset[i]<a:
            a=timeminset[i]
    print a
        
    return data,train,test,dict(timeset),dict(timeminset)


    


if __name__ == '__main__':    
    data=[]
    train=[]
    test=[]
    timeset={}#{item:time}
    timeminset={}#{item:mintime}
    SplitData(4,1,1)
    
    
    