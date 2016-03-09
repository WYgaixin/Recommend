# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 17:17:43 2016

@author: ssw
"""

import random
import math
from pandas import *
import pandas as pd
#import file_util
#import pprint



def SplitData():
    for line in open('movie_directors.data'):
        item,director,directorname = line.split('	')
        data1.append([item,director])
#    print data1[1:20]
#    for item,director in data1:
#        item_director.setdefault(item,{})
#        item_director[item][director]=1
#    print item_director

def initCMF(F):
    for i,d in data1:
        if i not in q:
            q[i]=[random.random()/math.sqrt(F) for x in range(0,F)]
        if d not in s:
            s[d]=[random.random()/math.sqrt(F) for x in range(0,F)]
#    print q
#    print '*************************'
#    print '*************************'
#    print s
        
    
def pridict(i,d,F):
    ret=sum(q[i][f]*s[d][f] for f in range(0,F))
    print ret
    
def learning(n,alpha,lambd,w,F):
    initCMF(F)
    for i,d in data1:
        pridict(i,d,F)
    
if __name__ == '__main__':
    data1=[]
    item_director={}
    q={}#全部电影的隐类
    s={}#导演的隐类
    SplitData()
#    initCMF(50)
    learning(10,0.01,0.1,2,50)

        