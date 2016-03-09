# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 10:26:33 2015

@author: Administrator
"""
import random
import math
class ItemBasedCF:
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
    def itemSimilarity(self,train = None):
        """
        One method of getting user similarity matrix
        获得用户的相似矩阵。。。
        """
        train = train or self.traindata
        self.itemSim = dict()   #字典
#        item_users = dict()         # 字典
        C=dict()
        N=dict()
        for u,items in train.items():#返回元组('u1','item1')('u2','item2')('u3','item3')
            for i in items:#[item1，ITem2，item3]
                N.setdefault(i, 0);
                N[i]+=1
                for j in items:
                    if i==j:
                        continue
                    C.setdefault(i, {})
                    C[i].setdefault(j, 0)
                    C[i][j]+=1
                    
        for i,related_items in C.items():#related_item是字典{j:3,j2:4}
            self.itemSim.setdefault(i, {})
            for j,cij in related_items.items():#cij 物品i和j的用户个数
                self.itemSim[i].setdefault(j, 0)
                self.itemSim[i][j]=cij/math.sqrt(N[i]*N[j])
        
        
#        """
#        建立一个倒排表
#        """
#        for u,item in train.items():      #返回键值u=key,item=value元组进行对字典的循环迭代
#            for i in item.keys():
#                item_users.setdefault(i,set())
#                item_users[i].add(u)
##        print item_users
#                          
#        for i in item_users.keys():
#            for j in item_users.keys():   #keys将字典中的键以列表形式返回
#                if i == j:
#                    continue         # 结束当前迭代
#                self.itemSim.setdefault(i,{})
#                self.itemSim[i][j] = len(set(item_users[i]) & set(item_users[j]))  #物品的集合
#                self.itemSim[i][j] /=math.sqrt(len(set(item_users[i])) * len(set(item_users[j])) *1.0)
##        print 'itemSim',self.itemSim
        
    def recommend(self,user,train = None,k = 3,nitem=10):
        """
        推荐
        """
        train = train or self.traindata
        rank = dict()                             # 字典
        interacted_items = train.get(user,{})  #接受推荐的user       只获得值{物品：评分}
        
        for i,pi in interacted_items.items():
            for j,wj in sorted(self.itemSim[i].items(),key = lambda x : x[1],reverse = True)[0:k]:
                if j in interacted_items:
                    continue
                rank.setdefault(j,0)
                rank[j] +=pi*wj         #有问题  
                
        return dict*(sorted(rank.items(), key = lambda x:x[1], reverse = True)[0:nitem])
#        print 'rank',rank
        
    def recallAndPrecision(self,train = None,test = None,k = 8,nitem=10):
        """
        计算召回率( )和准确率(中的/总的推荐数)  推荐物品 nitem
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
            rank = self.recommend(user, train = train,k = k,nitem=nitem) 
            for item,_ in rank.items():      #得到物品，和其被点评的次数（对此物品的喜爱程度）
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += nitem
            
        return (hit / (recall * 1.0),hit / (precision * 1.0))
        
    def coverage(self,train = None,test = None,k = 8,nitem=10):
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
            rank = self.recommend(user, train, k = k,nitem=nitem)
            for item,_ in rank.items():
                recommend_items.add(item)
                
        return len(recommend_items) / (len(all_items) * 1.0)
        
    def popularity(self,train = None,test = None,k = 8,nitem=10):
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
            rank = self.recommend(user, train, k = k,nitem=nitem)
            for item ,_ in rank.items():
                ret += math.log(1+item_popularity[item])    # 推荐的 每个物品的流行度取对数
                n += 1
        return ret / (n * 1.0)
                
def testRecommend():
    """
    测试推荐效果
    """
    ibcf = ItemBasedCF('u.data')      #初始类UserBaseCF的对象
    ibcf.readData()
    ibcf.splitData(4,100)
    ibcf.itemSimilarity()
    user = "196"
    rank = ibcf.recommend(user,k = 40,nitem=10)    #3个相似用户
    for i,rvi in rank.items():            # ‘i’ 是物品   rui  感兴趣度
        items = ibcf.testdata.get(user,{})      #得到一个字典{}
        record = items.get(i,0)                #获得是对物品 ’i‘ 的评分 
        print "%5s: %.4f--%.4f" %(i,rvi,record)
        
def testItemBasedCF():
    """
    测试基于物品的协同过滤
    """
    cf  =  ItemBasedCF('u.data')
    cf.itemSimilarity()
    print "%3s%20s%20s%20s%20s" % ('K',"precision",'recall','coverage','popularity')
    for k in [5,10,20,40,80,160]:
        recall,precision = cf.recallAndPrecision( k = k)
        coverage = cf.coverage(k = k)
        popularity = cf.popularity(k = k)
        print "%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k,precision * 100,recall * 100,coverage * 100,popularity)
    
if __name__=='__main__':
    testItemBasedCF()
#    testRecommend()

        