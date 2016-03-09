# -*- coding: utf-8 -*-
"""
Created on Mon Aug 04 19:48:49 2014

@author: liuqianyu
"""

from numpy import *
import math
from pandas import *
       
def SplitData(M=4,k=3):
    test={}                  #字典
    train={}                 
    data=[]                 #列表
    userList = []
    itemList = []
    recordList = []
   
    for line in open('user_ratedmovies-timestamps.dat'):
        user,item,record,time=line.split('	')
        data.append([user,item,float(record),long(time)])
        
        
#        print data
    for user ,item ,record,time in data:
         if random.randint(0,M) == k: 
                test.setdefault(user,{}) 
                test[user][item] =record
         else: 
                train.setdefault(user,{}) 
                train[user][item]= record                # user_item  字典
                  
    
#计算用户、物品个数
    for user ,items in train.items():
        if user in userList :
            continue
        else :            
            userList.append(user)                    # 总的用户数 userList
        for item ,record in items.items():
            if item in itemList :
                continue
            else :  
                itemList.append(item)              # 总的物品数 itemList
            if record in recordList :
                continue
            else :            
                recordList.append(record)         # 总的品论数  recordList
    print "ReLFM"    
    print "len(userlist) is ",len(userList)
    print 'len(itemlist) is',len(itemList)
#    print  recordList
    return dict(train),dict(test) ,userList,itemList,recordList

#    
#    print train
#    print "hello"
def splitnewData():
    timeset={} #字典
    data=[] #列表
    timeminset={}
    newmovie={}
    oldmovie={}
    userList = []
    itemList = []
    recordList = []

    for line in open('u.data'):
       user,item,record,time=line.split()
       data.append([user,item,float(record),int(time)])
#print data[0:1]
    for user,item,record,time in data:
       timeset.setdefault(item,[])  #{100：[3,5,6,7]}{电影：时间}
       timeset[item].append(time)
       
    #print timeset
    for item in timeset:
       timeminset[item] = sorted(timeset[item])[0] # 找到该电影最早评论的时间
#print timeminset

    for user,item,record,time in data:
        
      if time-timeminset[item]<60*24*60*60:
          
          newmovie.setdefault(user,{})
          newmovie[user][item]=record
          #print newmovie
      else:
          
          oldmovie.setdefault(user,{})
          oldmovie[user][item]=record
          #print oldmovie
#计算用户、物品个数
    for user ,items in oldmovie.items():
        if user in userList :
            continue
        else :            
            userList.append(user)                    # 总的用户数 userList
        for item ,record in items.items():
            if item in itemList :
                continue
            else :  
                itemList.append(item)              # 总的物品数 itemList
            if record in recordList :
                continue
            else :            
                recordList.append(record)         # 总的品论数  recordList
    print "ReLFM"    
    print "len(userlist) is ",len(userList)
    print 'len(itemlist) is',len(itemList)
#    print  recordList
    return dict(newmovie),dict(oldmovie) ,userList,itemList,recordList

def SplitDataNewOld():
    timeset={} #字典
    data=[] #列表
    timeminset={}
    Amovie={}
    amovie={}
    Bmovie={}
    Cmovie={}
    Dmovie={}
    Emovie={}
    movie={}
    dmovie={}
    
    
    for line in open('u.data'):
        user,item,record,time=line.split()
        data.append([user,item,float(record),int(time)])
        
    for user,item,record,time in data:
        timeset.setdefault(item,[])
        timeset[item].append(time)
        movie.setdefault(user,{})
        movie[user][item]=record
  
    for item in timeset:
       timeminset[item] = sorted(timeset[item])[0] # 找到该电影最早评论的时间 
    
    for user,item,record,time in data:
        
      if time-timeminset[item]<30*24*60*60:
          if random.randint(0,28)==3:
              Amovie.setdefault(user,{})
              Amovie[user][item]=record
          else:
              amovie.setdefault(user,{})
              amovie[user][item]=record

          #print newmovie
      elif(time-timeminset[item]>30*24*60*60) and (time-timeminset[item]<2*30*24*60*60):
          
          Bmovie.setdefault(user,{})
          Bmovie[user][item]=record
          
      elif(time-timeminset[item]<7*30*24*60*60) and (time-timeminset[item]>6*30*24*60*60):
          
          Cmovie.setdefault(user,{})
          Cmovie[user][item]=record
      elif time-timeminset[item]>7*30*24*60*60:
          if random.randint(0,7)==3:
              Dmovie.setdefault(user,{})
              Dmovie[user][item]=record
          else:
              dmovie.setdefault(user,{})
              dmovie[user][item]=record
          
          
      else:
          Emovie.setdefault(user,{})
          Emovie[user][item]=record
         
    print "len(movie) is ",len(movie)      
    print "len(Amovie) is ",len(Amovie)
    print "len(Bmovie) is ",len(Bmovie)
    print "len(Cmovie) is ",len(Cmovie)
    print "len(Dmovie) is ",len(Dmovie)
    print "len(Emovie) is ",len(Emovie)
    return dict(movie),dict(Amovie),dict(amovie),dict(Bmovie),dict(Cmovie),dict(Dmovie),dict(dmovie),dict(Emovie)

          
def countnumber(test): 
    userList = []
    itemList = []
    recordList = []
    for user ,items in test.items():
        if user in userList :
            continue
        else :            
            userList.append(user)                    # 总的用户数 userList
        for item ,record in items.items():
            if item in itemList :
                continue
            else :  
                itemList.append(item)              # 总的物品数 itemList
            if record in recordList :
                continue
            else :            
                recordList.append(record)         # 总的品论数  recordList
    print "ReLFM"    
    print "len(userlist) is ",len(userList)
    print 'len(itemlist) is',len(itemList)
#    print  recordList
    return userList,itemList,recordList
          
          
      
    
    
    
    
def Reverse(train):
    """
       建立一个倒排表
    """                     
    item_users = dict()               # 字典{item:{user:recoder}}
    for u,item in train.items(): 
        for i,r in item.items(): 
            item_users.setdefault(i,{}) 
            item_users[i][u]=r

    return item_users

def InitLFM(train,F):
    """
         F 表示隐类的个数
    """
    p=dict()
    q=dict()
   
    for u ,item in train.items():       # 用户      
         for i in train[u] :           #  train[u] 是一个字典，取得train[u]的 'key': 就是 ‘u’ 评论过得物品 i
            if u not in p :                
                p[u]=[random.random()/math.sqrt(F) for x in range(0,F)]   #  p矩阵 用户特征：m*f  初始化用户特征            
            if i not in q :               
                q[i]=[random.random()/math.sqrt(F) for x in range(0,F)]   #  q矩阵 特征物品：n*f  初始化物品特征
#    print p
    return p,q

#compute the number of predict
def Predict(u,i,p,q):
    ret = sum(p[u][f] * q[i][f] for f in range(0,len(p[u])))
#    print ret
#    print type(ret)
    return ret                                                            
    
    
    
def LearningLFM(train, F, n, alpha, lambd):
    print "diedaicishu",n                          #    迭代次数 n
    print "alpha",alpha                            #   学习速率 alpha()
    print "lamda",lambd                            #   正则化参数 ( 步 长 )
    p,q=InitLFM(train,F)                          # 函数调用，获得 p,q，以下就是
    for step in range(0,n):                      # 迭代次数 n
        for u ,items in train.items():
             for i,rui in items.items():
                 pui=Predict(u,i,p,q)          #第一次预测的评分是建立在随机产生的p、q矩阵中的值，以后进行迭代优化，产生误差最小的p、q矩阵
                 eui=rui-pui
                 for k in range(0,F):            #
                     p[u][k]+=alpha*(q[i][k]*eui-lambd*p[u][k])
                     q[i][k]+=alpha*(p[u][k]*eui-lambd*q[i][k])
        alpha*=0.9
    
#    ep=DataFrame(p).fillna(0)
#    ep.to_csv('pui.csv',encoding='utf_8')
#    eq=DataFrame(q).fillna(0)
#    eq.to_csv('qui.csv',encoding='utf_8')    
#    print  p.keys()
    print "the F is :",F
    return p,q
    
    
"""计算推荐的前n个""" 
def user_items(train,itemList,p,q,n):    
    rank={}  
    recomm={}
    for user,items in train.items():        
        for k in range(0,len(itemList)):      # itemList  物品列表
            item=itemList[k]                 # 第 k 个物品
            if item in train[user] :
                continue
            if item not in train[user] :
                if user not in rank:
                    rank[user]={}
                rank[user][item] = 0
                for f in range(0,len(p[user])):
                    rank[user][item] +=p[user][f]*q[item][f]       # 会 计算 每一个用的所有评论物品
#                    print rank
                    
    for user in rank:
        recomm[user] = {}
        for item,ru in sorted(rank[user].items(),key = lambda x:x[1],reverse = True)[0:n]:
            recomm[user][item] = ru
#    print 'the recommber number!',nn
    print "the n is:",n
#    print 'the recomm is done!',recomm
    return rank,recomm
            
   
def evaluateMAE(topN,test):
    """
       计算误差函数      topN 推荐的最相近的前 N 个：recomm{}
    """ 
    userMAE=0
    lens=0
    for user in test: 
        lens += len(test[user])         # the number of users
#    print lens
    bais=0
    for user ,items in test.items():
        for item ,rec in items.items():
            if user not in topN.keys():
                bais +=1                # bais 偏差
            if user in topN and (item not in topN[user]):
                bais +=1               #
            
    userMAE = bais*1.0/lens
    print "this is bais",bais
    print "this is MAE",userMAE
    return lens
                
def PrecisionAndRecall(topN,test,lens):
    """
        计算 准确率和召回率
    """
    hit = 0                       #  推荐准确的个数
    testCount = lens
    recommCount = 0               #  推荐的物品数
    for user in topN:
#        print len(topN[u])
        recommCount += len(topN[user])
        for item in topN[user]:
            if user in test and item in test[user]:
                hit += 1
    recall=hit / (testCount * 1.0)
    precisions=hit / (recommCount * 1.0)
#    F_measure=2.0*recall*precisions/(recall+precisions)                #
    print 'the hit, testCount and recommCount are: ',(hit,testCount,recommCount)    
    print 'the recall and precision is: ',(recall,precisions) 
#    print "the F_measure is :",F_measure       # 调和函数 ，综合 recall ， precisions 的评定指标
    #The F1 score can be interpreted as a weighted average of the precision and recall
 
             
def popular(train,item_users):
    """
         计算  新颖度/
    """
    u_item=0                  # 
    item_popular={}
    for user in train :
        u_item+=len(train[user])         #  所有用户评论过的 物品数 的总和 
    for i in item_users :                #  'i'  物品
        item=0
        item+=len(item_users[i])             #  倒排表 item_users ，评论物品 'i' 的用户数
        item_popular[i]=item*1.0/u_item      #  物品 i 的流行度
        """
            流行度=物品i被评论的人数/所有物品被评论次数的总和
        """
        
#    print recommend_items
#    print "the popular is !",item*1.0/u_item
    return item_popular
    
def Coverage(item_popular,recom):                      
    """
      覆盖率指标，基尼系数（Gini Index）,越小越好
    """ 
    itemList = []
    iPopu = {}
    G = 0
    Gini = 0
    j = 0
    #print urlPopular
    for user in recom:                       #  recomm[user][item] = ru  推荐topN
        for i in recom[user]:            
            iPopu[i]=0
            iPopu[i] = item_popular[i]       # 用户user 喜欢的  各个物品的流行度，
        itemList = sorted(iPopu.items(),key = lambda x : x[1],reverse = False)     #    流行度 从低到高
        lens = len(itemList)            # 物品数
        for k in range(lens):
            j = k + 1
            i = itemList[k][0]
            G += (2 * j - lens - 1) * iPopu[i]
        if lens == 1:
            G = 0
        else:
            Gini += G * 1.0 / (lens - 1)
        iPopu = {}
        itemList = []
    Gini = Gini * 1.0 /len(recom)
    print 'the coverage is: ', Gini 
    
def doEvaluateRMSE(train,itemList,test,p,q):
    Disum=0.0
    #count=0
    result=0.0
    rmse=0.0
    count =0.0
    for user,items in test.items():
        if user not in p.keys():
            continue
        if user in p.keys():
            for item,record in items.items():
                if item not in q.keys():
                    continue
                if item in q.keys():
                    
                   Disum+=math.pow(Predict(user,item,p,q)-record,2)
                   count+=1
    result=math.sqrt(Disum)/len(test)
    rmse = math.sqrt(Disum)/count
    print 'the RMSE is:', result
    print 'new rmse',rmse
    
def doEvluateMAE(train,itemList,test,p,q):
    mae1 = 0.0
    mae=0.0
    mae2=0.0
    count=0.0
    for user,items in test.items():
        if user not in p.keys():
            continue
        if user in p.keys():
            for item,record in items.items():
                if item not in q.keys():
                    continue
                if item in q.keys():
                    mae+=math.fabs(record-Predict(user,item,p,q))
                    count +=1
#                    print (record,Predict(user,item,p,q))
    mae1=mae/len(test)
    mae2=mae/count
    print 'newmae',mae2
    print 'count',count
    print len(test)
    print 'maemaemae is:',mae1
                        
                    
if __name__ == '__main__':
#    movie,Amovie,train,Bmovie,Cmovie,Dmovie,test,Emovie=SplitDataNewOld()
#    userList,itemList,recordList=countnumber(train)
#    userList,itemList,recordList=countnumber(dmovie)
#        
     train,test,userList,itemList,recordList = SplitData()
#    #test,train,userList,itemList,recordList = splitnewData()#老电影
#    #train,test,userList,itemList,recordList = splitnewData()#新电影
     item_users= Reverse(train)
     p,q = InitLFM(train,10)   
     p,q = LearningLFM(train, 10,1,0.0005,0.01)# 训练出矩阵1,0.005,0.01,0.5,10train, F, n, alpha, lambd):
     doEvaluateRMSE(train,itemList,test,p,q)
#     doEvluateMAE(train,itemList,test,p,q)
#    doEvaluateRMSE(train,itemList,train,p,q)
#     rank,recomm= user_items(train,itemList,p,q,4)  
#     lens= evaluateMAE(recomm,test)
#     PrecisionAndRecall(recomm,test,lens)
#     lens= evaluateMAE(recomm,train)
#    PrecisionAndRecall(recomm,train,lens)
#     item_popular=popular(train,item_users)
#     Coverage(item_popular,recomm)
#     popular(train,recomm)
#    
   
