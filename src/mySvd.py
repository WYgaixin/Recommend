# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:27:50 2015

@author: h
"""
import random
import math
import time
data = []
train = []
test = []

P=dict()
Q=dict()
bu=dict()
bi=dict()
mu=0

def ReadFile(data):
    f = open('u.data','r')
    line = f.readline()
    while line:
        line_split = line.split('\t')
        data.append( ( int(line_split[0]), int(line_split[1]) , int(line_split[2]),long(line_split[3]) ) )
        line = f.readline()
    f.close()
    return
    
def SplitDataMix(data,train,test,M,k,seed):
    random.seed(seed)
    for user,item,rui, commentTime in data:
        if random.randint(0,M) == k:
            test.append((user,item,rui,commentTime))
        else:
            train.append((user,item,rui,commentTime))
    return
    
def SplitDataMix1(data,train,test,M,seed):
    random.seed(seed)
    for user,item,rui, commentTime in data:
        if random.randint(0,M) in [0,1]:
            test.append((user,item,rui,commentTime))
        else:
            train.append((user,item,rui,commentTime))
    return
        

def SplitDataNew(data,train,test):
    itemReleasedTime = {}
    for user,item,rui,commentTime in data:
        itemReleasedTime.setdefault(item,long(time.time()))
        if commentTime < itemReleasedTime[item]:
            itemReleasedTime[item] = commentTime
#将每部电影的最早评论时间存放在字典中，作为电影的发布时间
#循环遍历data数据集，如果该用户观看记录中用户评论时间与发布时间相差小于两个月，则作为看新电影的记录
    for user,item,rui,commentTime in data:
        if commentTime-itemReleasedTime[item]<60*60*24*60:
            train.append((user,item,rui,commentTime))   #以新电影观看行为作为训练集
        else:
            test.append((user,item,rui,commentTime))   #以老电影观看行为作为测试集
    return
    

def SplitDataOld(data,train,test):
    itemReleasedTime = {}
    for user,item,rui,commentTime in data:
        itemReleasedTime.setdefault(item,long(time.time()))
        if commentTime < itemReleasedTime[item]:
            itemReleasedTime[item] = commentTime
#将每部电影的最早评论时间存放在字典中，作为电影的发布时间
#循环遍历data数据集，如果该用户观看记录中用户评论时间与发布时间相差小于两个月，则作为看新电影的记录
    for user,item,rui,commentTime in data:
        if commentTime-itemReleasedTime[item]<60*60*24*60:
            test.append((user,item,rui,commentTime)) #以新电影观看行为作为测试集
        else:
            train.append((user,item,rui,commentTime)) #以老电影观看行为作为训练
    return 
    
    
def Predict(u,i,P,Q,bu,bi,mu):
    ret = mu + bu[u] + bi[i]
    ret += sum( P[u][f] * Q[i][f] for f in range(0,len(P[u])) )
    return ret
    
def learningLFM(train,P,Q,bu,bi,Alpha,Lambda,n,mu,F):
    InitLFM(train,F,P,Q,bu,bi)
    for step in range(0,n):
        for u,i,rui,commentTime in train:
            pui = Predict(u,i,P,Q,bu,bi,mu)
            eui = rui - pui
            bu[u] += Alpha * (eui - Lambda * bu[u])
            bi[i] += Alpha * (eui - Lambda * bi[i])
            for f in range(0,F):
                P[u][f] += Alpha * (Q[i][f] * eui - Lambda * P[u][f])
                Q[i][f] += Alpha * (P[u][f] * eui - Lambda * Q[i][f])
        Alpha *= 0.9    
       # print('step ', step, ' . ')
  #  print('P:',P)
  #  print('Q:',Q)
  #      print('bu : ', bu)
   #     print('bi : ', bi)
    #    print('mu : ', mu) 
    return       

def InitLFM(train,F,P,Q,bu,bi):
    for u,i,rui,commentTime in train:
        bu[u] = 0
        bi[i] = 0
        if u not in P:
            P[u] = [random.random()/math.sqrt(F) for x in range(0,F)]
        if i not in Q:
            Q[i] = [random.random()/math.sqrt(F) for x in range(0,F)]
    return
    
def TestDataRmse(test,data,train,P,Q,bu,bi,mu):
    rmse = 0
    for u,i,rui,commentTime in test:
        if((u in P) and (i in Q)):
            rmse += float((rui - Predict(u,i,P,Q,bu,bi,mu)) * (rui - Predict(u,i,P,Q,bu,bi,mu)))
    rmse = math.sqrt(rmse) / float(len(test))
    return rmse

def TestDataMae(test,data,train,P,Q,bu,bi,mu):
    mae = 0
    for u,i,rui,commentTime in test:
        if((u in P) and (i in Q)):
            mae += float(math.fabs(rui - Predict(u,i,P,Q,bu,bi,mu)))
    mae = mae/float(len(test))
    return mae

def RecommendItems(train,test,P,Q,bu,bi,mu,k):
#    FinishedItems  测试集中所有用户看过所有的电影
    FinishedItems = {}
    recommend = {}   
    for u, i ,rui,commentTime in test:
        if u not in FinishedItems.keys():
            for user,item,record,commentTime in train:
                if user != u:
                    continue
                else:
#如果这是个新用户，即训练集中没有这个用户，那么也不会给它推荐
#从训练集中得到用户u的所有的已经看过的电影
                    FinishedItems.setdefault(u,[])
                    FinishedItems[u].append(item)
#循环遍历存在观影记录的所有用户，如果该用户已经存在推荐列表，则不再计算
#循环遍历物品集Q，如果该物品不在用户的已观看的电影中，则计算该用户可能对它的评分
    for u in FinishedItems:
        if u not in recommend:
            for item in Q:
                if item not in FinishedItems[u]:
                    recommend.setdefault(u,{})
#得到的recommendations是所有用户对他们所有没有看过的电影的预测评分
                    recommend[u][item] = Predict(u,item,P,Q,bu,bi,mu)     
                    
    for u in recommend:
        recommend[u] = sorted(recommend[u].items(),key = lambda x:x[1],reverse = True)[0:k]
    #    recommend[u] = {recommend[u][f][0] : recommend[u][f][1] for f in range(0,k)}
    return recommend

def PrecisionAndRecall(recommendResult,test,k):
    hit = 0
    for u in recommendResult:
        recommendResult[u] = dict(recommendResult[u])
        for user,item,rui,commentTime in test:
            if user == u:
                if item in recommendResult[u].keys():
                    hit += 1
    recall = hit / float(len (test))
    precision = float(hit) / (len(recommendResult.keys()) * k)
    
    print 'hit:',hit
 #   print 'Recall : ',recall
    print ('Precision :', precision)
    print ('recall :', recall)
    return                

#def GiniIndex(p):
    
            
for kk in range(0,1):       
    
    ReadFile(data)
 #   SplitDataMix(data,train,test,8,1,1)
    if kk == 0:
        SplitDataMix1(data,train,test,4,1)
        print'混合推荐311'
#    if kk == 1:
#        SplitDataMix(data,train,test,2,1,1)
#        print'混合推荐211'
#    if kk == 2:
#        SplitDataMix(data,train,test,1,1,1)
#        print'混合推荐111'   
#    if kk == 3:
#        SplitDataMix(data,train,test,7,1,1)
#        print'混合推荐711'
#    if kk == 4:
#        SplitDataMix(data,train,test,6,1,1)
#        print'混合推荐611'   
#    if kk == 5:
#        SplitDataNew(data,train,test)
#        print'以用户看新电影的记录进行推荐'
#    if kk == 6:
#        SplitDataOld(data,train,test)
#        print'以用户看老电影的记录进行推荐'
    print '所有数据：' ,len(data)
    print '训练集个数',len(train)
    print '测试集个数' ,len(test)

    learningLFM(train,P=P,Q=Q,bu=bu,bi=bi,Alpha =0.04,Lambda =0.15 ,n =25 ,mu=mu,F=10)
    print('RMSE:' , TestDataRmse(test,data,train,P,Q,bu,bi,mu))
    print('MAE:' , TestDataMae(test,data,train,P,Q,bu,bi,mu))

#    for i in range(10,200,20):
#    
#        print 'k :',i
#        userRecommend = RecommendItems(train,test,P,Q,bu,bi,mu,k = i)
##print userRecommend
#        PrecisionAndRecall(userRecommend,test,k = i)
    data = []
    train = []
    test = []

    P=dict()
    Q=dict()
    bu=dict()
    bi=dict()
    mu=0

