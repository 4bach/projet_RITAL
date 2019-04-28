#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from IndexerSimple import IndexerSimple
from Weighter import Weighter1
from Weighter import Weighter2
from Weighter import Weighter3
from IRModel import Vectoriel


from Parser import Parser

qry = "Computers in Inspection Procedures Science"

if __name__=="__main__":
    D = Parser.buildDocCollectionSimple('../cacmShort-good.txt')
    print(D)
    indexer = IndexerSimple()
    indexer.indexation(D)
    w1 = Weighter1(indexer) 
    t=w1.getWeightsForQuery(qry)
    print("w1: ",t)
    w2 = Weighter2(indexer) 
    t2=w2.getWeightsForQuery(qry)
    print("w2: ",t2)
    w3 = Weighter3(indexer) 
    t3=w3.getWeightsForQuery(qry)
    print("w3: ",t3)

    v1 = Vectoriel(w1)
    s1 = v1.getScores(qry)
    print("s1:",s1)   
    
    v2 = Vectoriel(w2)
    s2 = v1.getScores(qry)
    print("s2:",s2)   
    
    v3 = Vectoriel(w3)
    s3 = v3.getScores(qry)
    sort = v3.getRanking(qry)
    
    print("s3:",s3)