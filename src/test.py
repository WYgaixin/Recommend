# -*- coding: utf-8 -*-
"""
Created on Thu Nov 05 22:04:30 2015

@author: ssw
"""
def q(i,j):
    
    w={'a':{'A':1,'B':1,'C':1},'b':{'A':2,'B':2},'a':{'A':3,'B':3,'C':3}}
    t={}
    for r in w[i]:
        
        if r in w[j]:
            
            t[r]=1
    sum1=sum(w[i][it] for it in t)
    return sum1
if __name__ == '__main__':
   print q('a','b')