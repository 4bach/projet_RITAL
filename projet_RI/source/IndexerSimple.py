#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:58:38 2019

@author: ykarmim
"""
from collections import Counter
from TextRepresenter import PorterStemmer
import math


class IndexerSimple:
    
    
    def __init__(self):
        self.index = None
        self.index_inv = None 
        self.tf_idf = None
        self.tf = None
        self.collection = None
        
    motvide = ["the", "a", "an", "on", "behind", "under", "there", "in", "on"]
    
    def setIndex(self,index):
        self.index = index
        
        
    def setIndex_inv(self,index_inv):
        self.index_inv = index_inv
    
    
    def setTf_idf(self,tf_idf):
        self.tf_idf = tf_idf
        
    
    def setTf(self,tf):
        self.tf = tf
        
    
    def getTfsForDoc(self,iddoc):
        return self.index[iddoc]
        
    
    def getTfIDFsForDoc(self,ind):
        return self.tf_idf[ind]
    
    def getTfsForStem(self,ind):
        return self.index_inv[ind]
    
    def getTfIDFsForStem(self,stem):
        dico = dict()
        for iddoc in self.index_inv[stem].keys():
            dico[iddoc] = self.tf_idf[int(iddoc)][stem]
        
        return dico
    
    def getStrDoc(self,iddoc):
        return self.collection[iddoc].getTexte()
    
    def getNbDoc(self):
        return len(self.index)
    
    def countWord(doc):
        ps = PorterStemmer()
        return dict(Counter([i for i in ps.getTextRepresentation(doc)]))
    
    def indexation(self,collection):
        self.collection = collection
  
        index=dict()
        index_inv=dict()
        tf_idf = dict()
        tf = dict()
        for i in range(len(collection)):            
            index[collection[str(i+1)].getID()-1] = IndexerSimple.countWord(collection[str(i+1)].getTexte())
            for j in index[i]:
                if j in index_inv:
                    index_inv[j][str(i)] = str(index[i][j])
                else:
                    index_inv[j] = {str(i):str(index[i][j])}
        
        
        for i in index:
            taille = len(index[i])
            tf[i] =  {mot:(index[i][mot]/taille) for mot in index[i]}
            tf_idf[i] = {mot:(index[i][mot]/taille)*math.log((1+len(collection))/(1+len(index_inv[mot]))) for mot in index[i]}
        
        self.setIndex(index)
        self.setIndex_inv(index_inv)
        self.setTf(tf)
        self.setTf_idf(tf_idf)
        

            