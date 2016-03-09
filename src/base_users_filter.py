# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 15:55:17 2015

@author: Administrator
"""

import random
import math
class UserBasedCF:
    def __init__(self,datafile = None):
        self.datafile = datafile
        self.readData()
        self.splitData(3,47)
    def readData(self,datafile = None):
        """
        read the data from the data file which is a data set
        读取数据从数据文件中
        """
        self.datafile = datafile or self.datafile
        self.data = []         #初始化为空的列表
        for line in open(self.datafile):       # f=open(self.datafile)  ,line=f.readline().
            userid,itemid,record,_ = line.split()     #分割
            self.data.append((userid,itemid,int(record)))  #在data尾部加新的对象
    def splitData(self,k,seed,data=None,M = 8): 
        """
        每次试验选取不同的k(0<k<M-1)   和相同的随机数种子seed,进行M次试验
        split the data set
        testdata is a test data set          “testdata 是测试集”
        traindata is a train set             “traindata 是训练集”
        test data set / train data set is 1:M-1   “比例  1：M-1”
        """
        self.testdata = {}      #初始化空字典
        self.traindata = {}
        data = data or self.data
        random.seed(seed)      # seed() 方法改变随机数生成器的种子，可以在调用其他随机模块函数之前调用此函数。
        for user,item, record in self.data:
            if random.randint(0,M) == k:   #随机生成一个整数，在0~M之间
                self.testdata.setdefault(user,{})  #初始化user为键，{}为值
                self.testdata[user][item] = record   #{‘user’：{‘item’：record}}
            else:
                self.traindata.setdefault(user,{})
                self.traindata[user][item] = record
    def userSimilarity(self,train = None):#余弦相似度
        """
        One method of getting user similarity matrix
        获得用户的相似矩阵。。。
        """
        train = train or self.traindata
        self.userSim = dict()                   #字典
        for u in train.keys():#u表示用户1，v表示其他的用户
            for v in train.keys():   #keys将字典中的键以列表形式返回
                if u == v:
                    continue         # 结束当前迭代
                self.userSim.setdefault(u,{})
                self.userSim[u][v] = len(set(train[u].keys()) & set(train[v].keys()))  #物品的交集
                self.userSim[u][v] /=math.sqrt(len(train[u]) * len(train[v]) *1.0) #物品的并集
    def userSimilarityBest(self,train = None):
        """
        the other method of getting user similarity which is better than above
        you can get the method on page 46
        获得用户的相似矩阵   的更好的方法。(使用倒排表的方法)
        In this experiment，we use this method
        """
        train = train or self.traindata
        self.userSimBest = dict()   #字典
        item_users = dict()         # 字典
        
        """
        建立一个倒排表
        """
        for u,item in train.items():      #返回键值u=key,item=value元组进行对字典的循环迭代
            for i in item.keys():
                item_users.setdefault(i,set())    # set() , 元素不重复且无序
                item_users[i].add(u) #购买了该物品的用户添加到item_users字典{item:(a,b,c)}
        
        user_item_count = dict()              #字典,用户喜欢的物品个数{'u':4}
        count = dict()#{'u1:{'u2':2,'u3':3}'}u1用户和u2用户有2个共同喜欢的电影，u1和u3有三个共同x的电影
        
        for item,users in item_users.items():        #同上一个for循环
            for u in users:
                user_item_count.setdefault(u,0)
                user_item_count[u] += 1               #用户u自己喜欢物品的个数
                for v in users:
                    if u == v:continue
                    count.setdefault(u,{})
                    count[u].setdefault(v,0)
                    count[u][v] += 1                   #用户u，v 共同喜欢物品的个数   
 
        for u ,related_users in count.items():         #  related_users = {'v':cuv}
            self.userSimBest.setdefault(u,dict())
            for v, cuv in related_users.items():       #  related_users       cuv表示个数
                self.userSimBest[u][v] = cuv / math.sqrt(user_item_count[u] * user_item_count[v] * 1.0)#uv共同喜欢的个数。u用户喜欢的个数，v喜欢的个数
 
    def recommend(self,user,train = None,k = 8,nitem = 40):
        """
        推荐  选取k=8个与其最相似的用户，  根据此，向其推荐前40件物品
        """
        train = train or self.traindata
        rank = dict()
        interacted_items = train.get(user,{})      #接受推荐的user喜欢的物品及评分      只获得值{物品：评分}
        
        for v ,wuv in sorted(self.userSimBest[user].items(),key = lambda x : x[1],reverse = True)[0:k]: #v是用户，wuv是user和v之间的相似度
            for i , rvi in train[v].items():      #得到" v "的物品和评分{'v用户':{'i物品':rvi评分}}
                if i in interacted_items:         #疑问 （interacted_items是字典， i是物品）该物品user已观看过，则不推荐
                    continue
                rank.setdefault(i,0)
                rank[i] += rvi*wuv               # i 被user评过，  同时也被与他相似的前八位顾客评的次数，rvi评分*wuv相似度
                
        return dict(sorted(rank.items(),key = lambda x :x[1],reverse = True)[0:nitem])     #评的最多的前40个
    def recallAndPrecision(self,train = None,test = None,k = 8,nitem = 10):
        """
        计算召回率( )和准确率(中的/总的推荐数)  推荐物品 nitem
        准确率是指命中物品数占推荐物品总数的比例
        召回率
        Get the recall and precision, the method you want to know is listed 
        in the page 43
        """
        train  = train or self.traindata
        test = test or self.testdata
        hit = 0
        recall = 0                        # 召回
        precision = 0                     # 准确
        
        for user in train.keys():         # 接受推荐的用户（ 所有的用户都会参与 ）
            tu = test.get(user,{})        # 用户测试集中的物品，评分
            rank = self.recommend(user, train = train,k = k,nitem = nitem) 
            for item,_ in rank.items():      #得到物品，和其被点评的次数（对此物品的喜爱程度）
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += nitem
            
        return (hit / (recall * 1.0),hit / (precision * 1.0))
    def coverage(self,train = None,test = None,k = 8,nitem = 10):
        """
        计算覆盖率
        """
        train = train or self.traindata
        test = test or self.testdata
        recommend_items = set()            #集合  无序
        all_items  = set()
        
        for user in train.keys():          # user 所有的用户
            for item in train[user].keys():
                all_items.add(item)
            rank = self.recommend(user, train, k = k, nitem = nitem)
            for item,_ in rank.items():
                recommend_items.add(item)
                
        return len(recommend_items) / (len(all_items) * 1.0)
    def popularity(self,train = None,test = None,k = 8,nitem = 10):
        """
        计算新颖度
        Get the popularity
        the algorithm on page 44
        """
        train = train or self.traindata
        test = test or self.testdata
        item_popularity = dict()
        
        for user ,items in train.items():
            for item in items.keys():
                item_popularity.setdefault(item,0)
                item_popularity[item] += 1
                
        ret = 0
        n = 0
        for user in train.keys():
            rank = self.recommend(user, train, k = k, nitem = nitem)
            for item ,_ in rank.items():
                ret += math.log(1+item_popularity[item])    # 推荐的 每个物品的流行度取对数
                n += 1
        return ret / (n * 1.0)
     
def testRecommend():
    """
    测试推荐效果
    """
    ubcf = UserBasedCF('u.data')      #初始类UserBaseCF的对象
    ubcf.readData()
    ubcf.splitData(4,100)
    ubcf.userSimilarityBest()
    user = "345"
    rank = ubcf.recommend(user,k = 3)    #3个相似用户
    
    for i,rvi in rank.items():            # ‘i’ 是物品
        items = ubcf.testdata.get(user,{})      #得到一个字典{}
        record = items.get(i,0)                #获得是对物品 ’i‘ 的评分 
        print "%5s: %.4f--%.4f" %(i,rvi,record)
        
def testUserBasedCF():
    """
    测试基于用户的协同过滤
    """
    cf  =  UserBasedCF('u.data')
    cf.userSimilarityBest()
    print "%3s%20s%20s%20s%20s" % ('K',"recall",'precision','coverage','popularity')
    for k in [5,10,20,40,80,160]:
        recall,precision = cf.recallAndPrecision( k = k)
        coverage = cf.coverage(k = k)
        popularity = cf.popularity(k = k)
        print "%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k,recall * 100,precision * 100,coverage * 100,popularity)
         
if __name__ == "__main__":
#    testRecommend()
    testUserBasedCF()
