# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 09:33:58 2015

@author: ssw
"""

import random
import math
from pandas import *

def SplitData(M,k,seed):
    for line in open('user_ratedmovies-timestamps.dat'):
        user,item,record,time=line.split('	')
        data.append([int(user),int(item),float(record),long(time)])
        
    for user,item,record,time in data:
        timeset.setdefault(item,[])
        timeset[item].append(time) #记录电影的时间
    
    for item in timeset:
        timeminset[item]=sorted(timeset[item])[0] #找到电影最早评论的时间，看做是电影的上映时间，即最早时间
        
    random.seed(seed)
    for user,item,record,time in data:
        if random.randint(0,M) == k:
            test.append((user,item,record,time))
        else:
            train.append((user,item,record,time))
        
#    for user,item,record,time in data:
#        if time-timeminset[item]<60*24*60*60: #将电影按时间分类
#            newmovie.setdefault(user,{})
#            newmovie[user][item]=record
#            
#        else:
#            oldmovie.setdefault(user,{})
#            oldmovie[user][item]=record
    
    print "data number：",len(data)
    print "train number：",len(train)
    print "test numer",len(test)
#    print timeminset
    return data,train,test,dict(timeset),dict(timeminset)
    

def InitCMF(F): #初始化特征向量，F个隐类
    for u,i,record,time in train:
        if time-timeminset[i]<60*24*60*60: #新电影
            if u not in p:
                p[u]=[random.random()/math.sqrt(F) for x in range(0,F)]
            if i not in qnew:
                qnew[i]=[random.random()/math.sqrt(F) for x in range(0,F)]
#            if i=='1497':
#                print 'i not in qnew',qnew[i]
        else:#旧电影
            if u not in p:
                p[u]=[random.random()/math.sqrt(F) for x in range(0,F)]
            if i not in qold:
                qold[i]=[random.random()/math.sqrt(F) for x in range(0,F)]
    print ('**********************')
#    print 'i not in qnew',qnew['1497']
            
#    print 'dddd',qnew.get('1497')
    return p,qnew,qold

def InitCMFmu(F):
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
    return p,qold,qnew,bunew,binew,buold,biold
    
                

    
def predict(u,i,p,qold):
    rat=0
    for f in range(0,len(p[u])):
        rat+=p[u][f]*qold[i][f]
    return rat
    
def predictqold(u,i,F):# 预测评分
    ret=sum(p[u][f]*qold[i][f] for f in range(0,len(p[u])))     
    return ret
#    rat=0.0
#    for f in range(0,F):
#        if u not in p :
#            p.setdefault(u,0)
#        elif i not in qold:
#            qold.setdefault(i,0)
#        else:
#            rat+=p[u][f]*qold[i][f]    
#    return rat
    
def predictqnew(u,i,F):# 预测评分
    ret=sum(p[u][f]*qnew[i][f] for f in range(0,len(p[u]))) 
    return ret

def Predictold(u,i,F,buold,biold,mu):
    ret = mu + buold[u] + biold[i]
    ret += sum(p[u][f] * qold[i][f] for f in range(0,len(p[u])))
    return ret
    
def Predictnew(u,i,F,bunew,binew,mu):
    ret = mu + bunew[u] + binew[i]
    ret += sum(p[u][f]*qnew[i][f] for f in range(0,len(p[u])))
    return ret
    
#    if i=='242':
#        print 'qnew is',qnew.get(i)      
#    rat=0.0
#    for f in range(0,F):
#        if u not in p:
#            p.setdefault(u,0)
#        elif i not in qnew:
#            qnew.setdefault(i,0)
#        else:
#           rat+=p[u][f]*qnew[i][f]
#    return rat

    
def learningCMF1(data,train,timeminset,n,alpha,lambd,w,F):
    print "diedaicishu",n
    print "quangzhong",w
    print "alpha",alpha
    print "lambd",lambd
    p,qold,qnew=InitCMF(train,data,timeminset,F)
    try:
         for step in range(0,n):
              for u,i,record,time in train:
                   if time-timeminset[i]<60*24*60*60:#new
                          pui=predictqnew(u,i,F)
                          eui=record-pui
                          for k in range(0,F):
                              qnew[i][k]+=alpha*(eui*p[u][k]-lambd*qnew[i][k])
                              if i in qold[i]:
                                 p[u][k]+=alpha*((qold[i][k]*eui*w)+(1-w)*eui*qnew[i][k]-lambd*p[u][k])
                              else:
                                  p[u][k]+=alpha*((1-w)*eui*qnew[i][k]-lambd*p[u][k])
                                  
#                              p[u][k]+=alpha*((qold[i][k]*eui*w)-lambd*p[u][k])                    
                              
                   else:#old
                       pui=predictqold(u,i,F)
                       eui=record-pui
                       for k in range(0,F):
                           qold[i][k]+=alpha*(eui*p[u][k]-lambd*qold[i][k])
                           if i in qnew[i]:
                              p[u][k]+=alpha*((qold[i][k]*eui*w)+(1-w)*eui*qnew[i][k]-lambd*p[u][k])
                           else:
                              p[u][k]+=alpha*((qold[i][k]*eui*w)-lambd*p[u][k])
                                
#                           p[u][k]+=alpha*((qold[i][k]*eui*w)-lambd*p[u][k])
                            

              alpha*=0.9
    except KeyError:
        pass
        return p,qold, qnew

def learningCMF2(n,alpha,lambd,w,F):
    print "diedaicishu",n
    print "quangzhong",w
    print "alpha",alpha
    print "lambd",lambd
   
    p,qnew,qold=InitCMF(F)
#    print ('1497 value is',qnew['1497'])
    
    for step in range(0,n):
        for u,i,record,time in train:    
           if time-timeminset[i]<60*24*60*60:
               pui=predictqnew(u,i,F) 
               eui=record-pui
               for k in range(0,F):
#                   if i not in qnew:
#                       qnew.setdefault(i,0)
#                   else:
                   qnew[i][k]+=alpha*(eui*p[u][k]-lambd*qnew[i][k])              
                   if i not in qold:
                       p[u][k]+=alpha*((1-w)*eui*qnew[i][k]-lambd*p[u][k])                     
                   else:
                       p[u][k]+=alpha*((qold[i][k]*eui*w)+(1-w)*eui*qnew[i][k]-lambd*p[u][k])
                        
        else:
            pui=predictqold(u,i,F)
            eui=record-pui
            for k in range(0,F):
                qold[i][k]+=alpha*(eui*p[u][k]-lambd*qold[i][k])
                if i in qnew:
                    p[u][k]+=alpha*((qold[i][k]*eui*w)+(1-w)*eui*qnew[i][k]-lambd*p[u][k])
                else:
                    p[u][k]+=alpha*((qold[i][k]*eui*w)-lambd*p[u][k])

    alpha*=0.9
    return p,qnew,qold

def learningCMF3(n,alpha,lambd,w,F,mu):
    print 'n:',n
    print 'alpha:',alpha
    print 'lambd:',lambd
    print 'w:',w
    print 'F:',F
    print 'mu:',mu
    p,qold,qnew,bunew,binew,buold,biold = InitCMFmu(F)
    for step in range(0,n):
        for u,i,record,time in train:
            if time-timeminset[i]<60*24*60*60:
                pui=Predictnew(u,i,F,bunew,binew,mu)
                eui=record-pui
                bunew[u] +=alpha*(eui-lambd*bunew[u])
                binew[i] +=alpha*(eui-lambd*binew[i])
                for k in range(0,F):
                    qnew[i][k]+=alpha*(eui*p[u][k]-lambd*qnew[i][k])              
                    if i not in qold:
                        p[u][k]+=alpha*((1-w)*eui*qnew[i][k]-lambd*p[u][k])                        
                    else:
                        p[u][k]+=alpha*((qold[i][k]*eui*w)+(1-w)*eui*qnew[i][k]-lambd*p[u][k])
            else:
                pui=Predictold(u,i,F,buold,biold,mu)
                eui=record-pui
                buold[u] +=alpha*(eui-lambd*buold[u])
                biold[i] +=alpha*(eui-lambd*biold[i])
                for k in range(0,F):
                    qold[i][k]+=alpha*(eui*p[u][k]-lambd*qold[i][k])
                    if i in qnew:
                        p[u][k]+=alpha*((qold[i][k]*eui*w)+(1-w)*eui*qnew[i][k]-lambd*p[u][k])
                    
                    else:
                        p[u][k]+=alpha*((qold[i][k]*eui*w)-lambd*p[u][k])
    alpha*=0.9
    return p,qnew,qold,bunew,binew,buold,biold
                    
                
           
                       
                    
    
    
        
def TestDataRMSE(F):
    rmse = 0.0
    for u,i,record,time in test:
        if time-timeminset[i]<60*24*60*60:
            if((u in p) and (i in qnew)): 
#               rmse += float((record - predictqnew(u,i,F)) * (record - predictqnew(u,i,F)))
               rmse += float(math.pow((record - predictqnew(u,i,F)),2))
            else:
                continue
#               m += float(math.fabs(record-predictqnew(u,i,F)))
        else:
            if((u in p) and (i in qold)):
                rmse += float(math.pow((record - predictqold(u,i,F)),2))
            else:
                continue
#                m += float(math.fabs(record-predictqold(u,i,F)))
#                rmse += float((record - predictqold(u,i,F)) * (record - predictqold(u,i,F)))
    rmse = math.sqrt(rmse / float(len(test)))
#    m =m / float(len(test))
#    print 'm',m
    return rmse 

def MAE(F):
    mae=0.0
    count = 0
    for u,i,record,time in test:
        count+=1
        if time-timeminset[i]<60*24*60*60:#新电影
            if((u in p) and (i in qnew)):
                mae += float(math.fabs(record-predictqnew(u,i,F)))
            else:
                continue
        else:
            if ((u in p) and (i in qold)):
                mae += float(math.fabs(record-predictqold(u,i,F)))
            else:
                continue
    mae=mae/count
    print 'len(test)',len(test)
    print 'count',count
    return mae 
#def learningCMF(data,oldmovie,newmovie,n,alpha,lambd,w,F):
#    print "diedaicishu",n
#    print "quanzhong",w
#    print "alpha",alpha
#    print "lambd",lambd
#    p,qold,qnew=InitCMF(oldmovie,newmovie,data,F)
##    print qold
#    for step in range(0,n):
#        for u,items in oldmovie.items():
#            for i,rui in items.items():
#                pui=predict(u,i,p,qold)
#                eui=rui-pui
#            for k in range(0,F):    
#                p[u][k]+=alpha*((qold[i][k]*eui*w)+(1-w)*eui*qnew[i][k]-lambd*p[u][k])
#                qold[i][k]+=alpha*(eui*p[u][k]-lambd*qold[i][k])
#                qnew[i][k]+=alpha*(eui*p[u][k]-lambd*qnew[i][k])
#                         
#       
#           
#        for u,items in newmovie.items():
#           for i,rui in items.items():
#               pui=predict(u,i,p,qnew)
#               eui=rui-pui
#           for k in range(0,F):  
#               p[u][k]+=alpha*((qold[i][k]*eui*w)+(1-w)*eui*qnew[i][k]-lambd*p[u][k])#这里有问题
#               qold[i][k]+=alpha*(eui*p[u][k]-lambd*qold[i][k])
#               qnew[i][k]+=alpha*(eui*p[u][k]-lambd*qnew[i][k])
#                
#        alpha*=0.9
#    print p,qold,qnew
           
            
                    
    
    
  
if __name__ == '__main__':
    p=dict()  # 全部用户特征
    qold=dict() #老电影特征
    qnew=dict()  #新电影特征
    data=[]
    train=[]
    test=[]
    bunew=dict()
    binew=dict()
    buold=dict()
    biold=dict()
    mu=0
  
    timeset={}
    timeminset={}
    data,train,test,timeset,timeminset=SplitData(8,1,1)
    p,qnew,qold,bunew,binew,buold,biold=learningCMF3(1,0.005,0.01,0.5,50,0)#n,alpha,lambd,w,F,mu
    
    print bunew
    
#    e=0
#    for u,i,record,time in qnew:
#         if i=='1497':
#             e+=1
#             print (u,i,record,time)
#    print e
#         else:
#            print 'no result'
        
#    p,qnew,qold=InitCMF(train,data,timeminset,50)
#    print qnew.get('1497')
#    e=0
#    for i ,f in qnew.items():
#        if i=='1497':
#            print qnew[i]
#            e+=1
#    print e
#    p,qnew,qold=learningCMF2(10,0.005,0.01,0.1,80)#n,alpha,lambd,w,F):
#    rmse=TestDataRMSE(5)
#    print "F:",80
#    print "the rmse is:",rmse
#    mae=MAE(5)
#    print "the mae is:",mae
     
#    newmovie,oldmovie,data=SplitData()
#    p,qold,qnew=InitCMF(oldmovie,newmovie,data,50)
#    learningCMF(data,oldmovie,newmovie,10,0.0005,0.001,0.5,50)
#    print "%3s%20s%20s" % ('F',"rmse",'mae')
#    for F in [5,10]:
#        learningCMF2(1,0.005,0.01,0.5,F = F)
#        mae=MAE(5)
#        rmse=TestDataRMSE(5)
#        print "%3d%19.3f%%%19.3f" % (F,rmse * 100,mae * 100)


        
    
    
        
                       
            
            
    
    
        

    
    

