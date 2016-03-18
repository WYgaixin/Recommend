# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 14:22:28 2016

@author: admin
"""
import random
import math
from pandas import *

def SplitData(M,K,seed):
    for line in open('user_ratedmovies-timestamps.dat'):
        user,item,record,time =line.split('	')
        data.append([int(user),int(item),float(record),long(time)])
    
    for line in open('movie_directors.dat'):
        item,director,directorname = line.split('	')
        item_director.append([int(item),director])
        
    for user,item,record,time in data:
        timeset.setdefault(item,[])
        timeset[item].append(time)
    
    for item in timeset:
        timeminset[item]=sorted(timeset[item])[0]
    
    random.seed(seed)
    for user,item,record,time in data:
        if random.randint(0,M)==K:
            test.append((user,item,record,time))
        else:
            train.append((user,item,record,time))
    
    return data,train,test,dict(timeset),dict(timeminset),item_director

def InitCMFdir(F):
    for u,i,record,time in train:
        bunew[u]=0
        binew[i]=0
        buold[u]=0
        biold[i]=0
        if time-timeminset[i]<60*24*60*60:
            if u not in p:
                p[u]=[random.random()/math.sqrt(F) for x in range(0,F)]
            if i not in qnew:
                qnew[i]=[random.random()/math.sqrt(F) for x in range(0,F)]
        else:
            if u not in p:
                p[u]=[random.random()/math.sqrt(F) for x in range(0,F)]
            if i not in qold:
                qold[i]=[random.random()/math.sqrt(F) for x in range(0,F)]
    
    for i,d in item_director:
        if i in qnew:
            if d not in dnew:
                dnew[d]=[random.random()/math.sqrt(F) for x in range(0,F)]
            else:
                continue
        elif i in qold:
            if d not in dold:
                dold[d]=[random.random()/math.sqrt(F) for x in range(0,F)]
            else:
                continue
        else:
            continue
    return p,qold,qnew,bunew,binew,buold,biold,dold,dnew

def Predictold(u,i,d,F,buold,biold,mu):
    ret=mu+buold[u]+biold[i]
    if d not in dold:
        ret+=sum(p[u][f]*qold[i][f] for f in range(0,len(p[u])))
    else:
        ret+=sum(p[u][f]*qold[i][f]+qold[i][f]*dold[d][f] for f in range(0,len(p[u])))  
    return ret

def Predictnew(u,i,d,F,bunew,binew,mu):
    ret=mu+bunew[u]+binew[i]
    if d not in dnew:
        ret+=sum(p[u][f]*qnew[i][f] for f in range(0,len(p[u])))
    else:
        ret+=sum(p[u][f]*qnew[i][f]+qnew[i][f]*dnew[d][f] for f in range(0,len(p[u]))) 
    return ret

def learningCMFd(F,n,alpha,lambd,w1,w2,w3,mu):
    print 'F:',F
    print 'n:',n
    print 'alpha',alpha
    print 'lambd',lambd
    p,qold,qnew,bunew,binew,buold,biold,dold,dnew = InitCMFdir(F)
    for step in range(0,n):
        for u,i,record,time in train:
            for i1,d in item_director:
                if time-timeminset[i]<60*24*60*60:
                    pui=Predictnew(u,i,d,F,bunew,binew,mu)
                    eui=record-pui
                    bunew[u]+=alpha*(eui-lambd*bunew[u])
                    binew[i]+=alpha*(eui-lambd*binew[i])
                    for k in range(0,F):
                        if d not in dnew:
                            qnew[i][k]+=alpha*(eui*w1*p[u][k]-lambd*qnew[i][k])
                        else:
                            qnew[i][k]+=alpha*(eui*w1*p[u][k]+eui*(1-w1-w2-w3)*dnew[d][k]-lambd*qnew[i][k])
                            dnew[d][k]+=alpha*(eui*(1-w1-w2-w3)*qnew[i][k]-lambd*dnew[d][k])
                        if i not in qold:
                            p[u][k]+=alpha*(eui*w2*qnew[i][k]-lambd*p[u][k])
                        else:
                            p[u][k]+=alpha*(eui*w1*qold[i][k]+eui*w2*qnew[i][k]-lambd*p[u][k])
                else:
                    pui=Predictold(u,i,d,F,buold,biold,mu)
                    eui=record-pui
                    buold[u]+=alpha*(eui-lambd*buold[u])
                    biold[i]+=alpha*(eui-lambd*biold[i])
                    for k in range(0,F):
                        if d not in dold:
                            qold[i][k]+=alpha*(eui*w1*p[u][k]-lambd*qold[i][k])
                        else:
                            qold[i][k]+=alpha*(eui*w1*p[u][k]+eui*w3*dold[d][k]-lambd*qold[i][k])
                            dold[d][k]+=alpha*(eui*w3*qold[i][k]-lambd*dold[d][k])
                        if i not in qnew:
                            p[u][k]+=alpha*(eui*w1*qold[i][k]-lambd*p[u][k])
                        else:
                            p[u][k]+=alpha*(eui*w1*qold[i][k]+eui*w2*qnew[i][k]-lambd*p[u][k])
    alpha*=0.9
    return p,qnew,qold,bunew,binew,buold,biold,dnew,dold
                    
                    
    
    
        

if __name__=='__main__':
    data=[]
    train=[]
    test=[]
    item_director=[]
    timeset=dict()
    timeminset=dict()
    p=dict()
    qold=dict()
    qnew=dict()
    dold=dict()#旧电影导演矩阵
    dnew=dict()#新电影导演矩阵
    bunew=dict()#对用户的偏置项
    binew=dict()#对新电影的偏置项
    buold=dict()#
    biold=dict()
    data,train,test,timeset,timeminset,item_director=SplitData(8,1,1)
#    print item_director
#    p,qold,qnew,bunew,binew,buold,biold,dold,dnew=InitCMFdir(5)
#    print dold
    p,qnew,qold,bunew,binew,buold,biold,dnew,dold=learningCMFd(5,10,0.003,0.01,0.25,0.25,0.25,0)
    print p
    
    
    