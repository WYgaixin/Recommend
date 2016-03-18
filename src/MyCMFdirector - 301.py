# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:33:47 2016

@author: ssw
"""

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
    
    for line in open('movie_directors.dat'):
        item,director,directorname = line.split('	')
        item_director.append([int(item),director])
        
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
    
#    print "data number：",len(data)
#    print "train number：",len(train)
#    print "test numer",len(test)
#    print item_director
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
    
    for i,d in item_director:
        if d not in s:
            s[d]=[random.random()/math.sqrt(F) for x in range(0,F)]
#    print ('ssssssssssssssssss')
#    print s
#    print ('**********************')
#    print 'i not in qnew',qnew['1497']
            
#    print 'dddd',qnew.get('1497')
#    print 'ssssss',s.get('john_lasseter')
#    print 'ppppp',p.get(3315)
#    print 'qnewqnew',qnew.get(3315)
#    print 'qoldqold',qold.get(3315)
    return p,qnew,qold,s
                
def predictdirectorold(u,i,d,F):
    if u not in p:
        ret=0.0
    elif i not in qold:
        ret=0.0
    elif d not in s:
        ret=0.0
    else:
        ret=sum(p[u][f]*qold[i][f]*s[d][f] for f in range(0,F))
    return ret

def predictdirectornew(u,i,d,F):
    if u not in p:
        ret=0.0
    elif i not in qnew:
        ret=0.0
    elif d not in s:
        ret=0.0
    else:
        ret=sum(p[u][f]*qnew[i][f]*s[d][f] for f in range(0,F))
    return ret
    
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
    print ('******************************')
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

def learningCMF3(n,alpha,lambd,w,F):
    InitCMF(F)
    for step in range(0,n):
        for u,i,record,time in train :
            for i1,d in item_director:
                if i == i1:                    
                    if time-timeminset[i]<60*24*60*60:
                        pui=predictdirectornew(u,i,d,F)
                        eui=record-pui
                        for k in range(0,F):
                            qnew[i][k]+=alpha*(eui*p[u][k]*s[d][k]-lambd*qnew[i][k])
                            if i not in qold:
                                p[u][k]+=alpha*((1-w)*eui*qnew[i][k]*s[d][k]-lambd*p[u][k])
                                s[d][k]+=alpha*((1-w)*eui*qnew[i][k]*p[u][k]-lambd*s[d][k])
                            else:
                                p[u][k]+=alpha*(w*eui*qold[i][k]*s[d][k]+(1-w)*eui*qnew[i][k]*s[d][k]-lambd*p[u][k])
                                s[d][k]+=alpha*(w*eui*p[u][k]*qold[i][k]+(1-w)*eui*qnew[i][k]*s[d][k]-lambd*s[d][k])
                    else:
                        pui=predictdirectorold(u,i,d,F) 
                        eui=record-pui
                        for k in range(0,F):
                            qold[i][k]+=alpha*(eui*p[u][k]*s[d][k]-lambd*qold[i][k])
                            if i not in qnew:
                                p[u][k]+=alpha*((1-w)*eui*qold[i][k]*s[d][k]-lambd*p[u][k])
                                s[d][k]+=alpha*((1-w)*eui*qold[i][k]*p[u][k]-lambd*s[d][k])
                            else:
                                p[u][k]+=alpha*(w*eui*qold[i][k]*s[d][k]+(1-w)*eui*qnew[i][k]*s[d][k]-lambd*p[u][k])
                                s[d][k]+=alpha*(w*eui*p[u][k]*qold[i][k]+(1-w)*eui*qnew[i][k]*s[d][k]-lambd*s[d][k])
                else:
                    pass
                       
    alpha*=0.9
    return p,qnew,qold,s

def TestDataRMSE(F):
    rmse = 0
    for u,i,record,time in test:
        if time-timeminset[i]<60*24*60*60:
            if((u in p) and (i in qnew)): 
               rmse += float((record - predictqnew(u,i,F)) * (record - predictqnew(u,i,F)))
        else:
            if((u in p) and (i in qold)):
                rmse += float((record - predictqold(u,i,F)) * (record - predictqold(u,i,F)))
    rmse = math.sqrt(rmse) / float(len(test))
    return rmse

def RMSE(F):#加入导演后
    rmse = 0
    for u,i,record,time in test:
        for i1,d in item_director:
            if i1 == i:
                if time-timeminset[i]<60*24*60*60:
                    if((u in p) and (i in qnew) and (d in s)):
                        rmse+=float((record-predictdirectornew(u,i,d,F))*(record-predictdirectornew(u,i,d,F)))
                else:#老电影
                    if((u in p) and (i in qold) and (d in s)):
                        rmse+=float((record-predictdirectorold(u,i,d,F))*(record-predictdirectorold(u,i,d,F)))           
            else:
                pass
                
    rmse = math.sqrt(rmse/float(len(test)))
    return rmse

def MAE(F):
    mae = 0
    for u,i,record,time in test:
        for i1,d in item_director:
            if i1 == i:
                if time-timeminset[i]<60*24*60*60:
                    if((u in p) and (i in qnew) and (d in s)):
                        mae+=float(math.fabs(record-predictdirectornew(u,i,d,F)))
                else:
                    if ((u in p) and (i in qold) and (d in s)):
                        mae+=float(math.fabs(record-predictdirectorold(u,i,d,F)))
            else:
                pass
    mae=mae/float(len(test))
    return mae
    
                
def RecommendItems(k,m,r):
    for u,i,r,t in test:
        if u not in user_items.keys():
            for user,item,record,time in train:#如果该用户在训练集中不存在，则不给其推荐。
                if user!=u:
                    continue
                else:
                    user_items.setdefault(u,[])
                    user_items[u].append(i) #测试集中用户看的电影
#    print user_items
    for u in user_items:#遍历用户物品集中的用户
        if u not in recommend:#该推荐列表里没有该用户，所以要给其推荐
            for item in timeminset.keys():#遍历全部的电影
                if item not in user_items[u]:    #该用户没有看过的电
                    recommend.setdefault(u,{})
                    if item in qold:
                        if item in qnew:
                            recommend[u][item]=r*predictqold(u,item,k)+(1-r)*predictqnew(u,item,k)
                        else:
                            recommend[u][item]=predictqold(u,item,k)
                    else:
                        if item in qnew:
                            recommend[u][item]=predictqnew(u,item,k)
                        else:
                            pass
    for u in recommend:
        recommend[u]=sorted(recommend[u].items(),key = lambda x:x[1],reverse = True)[0:m]
    return recommend

def PrecisionAndRecall(m):
    hit = 0       
    for u in recommend:
        recommend[u]=dict(recommend[u])
        for user,item,record,time in test:
            if user == u:
                if item in recommend[u].keys():
                    hit += 1
    recall = hit / float(len(test))
    precision = float(hit) / (len(recommend.keys()) * m)
    
    print 'hit:',hit
    print 'Precision :', precision
    print 'recall :', recall
    return precision,recall
        
                        
                        
                    
                        
                        
                        
                    
                
                    
                
                
                    
                    
    
                   
                
                
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
    s=dict()   #导演特征
    data=[]
    train=[]
    test=[]
    item_director=[]
    timeset={}
    timeminset={}
    user_items={}#用户物品集
    recommend={}#推荐集合
    testitemrecord={}#推荐结果
    
    
    data,train,test,timeset,timeminset=SplitData(8,1,1)

#    RecommendItems(5,4,0.2)
         

    learningCMF3(10,0.005,0.01,0.5,10)
    
    
#    RecommendItems(5,4,0.2)
#    PrecisionAndRecall(4)

#    print recommend
    rmse=RMSE(5)
    print "the rmse is:",rmse
    
    
    mae=MAE(5)
    print "the mae is:",mae

#
#    p,qnew,qold=learningCMF2(50,0.005,0.01,0.5,50)
#    rmse=TestDataRMSE(50)
#    print "the rmse is:",rmse
     



        
    
    
        
                       
            
            
    
    
        

    
    

