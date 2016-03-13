# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 13:15:28 2016

@author: admin
"""


from numpy import *
import math
from pandas import *

def SplitData(M,k,seed):
    for line in open('user_ratedmovies-timestamps.dat'):
        user,item,record,time=line.split('	')
        data.append([int(user),int(item),float(record)])
    
    random.seed(seed)
    for user,item,record in data:
        if random.randint(0,M) == k:
            test.append((user,item,record))
        else:
            train.append((user,item,record))
    
    print 'len(data)',len(data)
    print 'len(test)',len(test)
    print 'len(train)',len(train)
    return data,test,train
  
def InitLFM(F):
     for u,i,record in train:
         if u not in p:
             p[u]=[random.random()/math.sqrt(F) for x in range(0,F)]
         if i not in q:
             q[i]=[random.random()/math.sqrt(F) for x in range(0,F)]
     return p,q

def InitLFMui(F):
    for u,i,record in train:
        bu[u]=0
        bi[i]=0
        if u not in p:
            p[u]=[random.random()/math.sqrt(F) for x in range(0,F)]
        if i not in q:
            q[i]=[random.random()/math.sqrt(F) for x in range(0,F)]
    return p,q,bu,bi
      
def Predict(u,i,F):
    ret=0.0
    for f in range(0,len(p[u])):
        ret+=p[u][f]*q[i][f]
    return ret

def Predictui(u,i,F,bu,bi,mu):
    ret=mu+bu[u]+bi[i]
    ret+=sum(p[u][f]*q[i][f] for f in range(0,len(p[u])))
    return ret

def LearningLFM(F,n,alpha,lambd):
    print "diedaicishu",n
#    print "quangzhong",w
    print "alpha",alpha
    print "lambd",lambd
    p,q=InitLFM(F)
    for step in range(0,n):
        for u,i,record in train:
            pui=Predict(u,i,F)
            eui=record-pui
            for k in range(0,F):
                p[u][k]+=alpha*(q[i][k]*eui-lambd*p[u][k])
                q[i][k]+=alpha*(p[u][k]*eui-lambd*q[i][k])
        alpha*=0.9
    return p,q

def LearingLFMui(F,n,alpha,lambd,mu):
    print 'F:',F
    print 'n:',n
    print 'alpha:',alpha
    print 'lambd:',lambd
    p,q,bu,bi=InitLFMui(F)
    for step in range(0,n):
        for u,i,record in train:
           
            pui=Predictui(u,i,F,bu,bi,mu)
            eui=record-pui
            bu[u] +=alpha*(eui-lambd*bu[u])
            bi[i] +=alpha*(eui-lambd*bi[i])
            for k in range(0,F):
                p[u][k]+=alpha*(q[i][k]*eui-lambd*p[u][k])
                q[i][k]+=alpha*(p[u][k]*eui-lambd*q[i][k])
        alpha*=0.9
    return p,q,bu,bi
                
    

def RMSE(F):
    rmse=0.0
    for u,i,record in test:
        if ((u in p) and(i in q)):
            rmse+=float(math.pow((record - Predict(u,i,F)),2))
        else:
            continue
    rmse = math.sqrt(rmse / float(len(test)))
    return rmse
def RMSEui(F):
    rmse=0.0
    for u,i,record in test:
        if((u in p) and (i in q)):
            rmse+=float(math.pow((record-Predictui(u,i,F,bu,bi,mu)),2))
        else:
            continue
    rmse=math.sqrt(rmse/float(len(test)))
    return rmse 
def MAE(F):
    mae=0.0
    for u,i,record in test:
        if((u in p) and(i in q)):
            mae+=float(math.fabs(record - Predict(u,i,F)))
        else:#测试集里有训练集中没有的数据
            continue
    mae =mae/float(len(test))
    return mae

def MAP(F):
    mp=0.0
    rc=0.0
    for u,i,record in test:
        if((u in p) and (i in q)):
            mp+=float(math.fabs(record - Predict(u,i,F)))
            rc+=record
        else:
            continue
    mp =mp/rc
    return mp
            
    
        

if __name__ == '__main__':
    data=[]
    train=[]
    test=[]
    p=dict()
    q=dict()
    bu=dict()
    bi=dict()
    data,test,train=SplitData(8,1,1)
    p,q=LearningLFM(10,5,0.005,0.5)
    p,q,bu,bi=LearingLFMui(10,5,0.005,0.5,0)
    rmse=RMSEui(5)
#    mp=MAP(5)
#    print 'mp:',mp
#    rmse=RMSE(5)
#    mae=MAE(5)
#    InitLFM(50)
    print 'rmse',rmse
#    print 'mae',mae
