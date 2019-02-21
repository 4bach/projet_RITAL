#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from IndexerSimple import IndexerSimple
from Weighter import Weighter1
from Weighter import Weighter2
from Weighter import Weighter3
from IRModel import Vectoriel


from Parser import Parser

qry = "of the Use of Computers in Inspection"

if __name__=="__main__":
    D = Parser.buildDocCollectionSimple('/users/Etu3/3414093/Cours/M1S2/projet_RITAL/projet_RI/cacmShort-good.txt')
    indexer = IndexerSimple()
    indexer.indexation(D)
    w1 = Weighter1(indexer) 
    t=w1.getWeightsForQuery(qry)
    print(t)
    w2 = Weighter2(indexer) 
    t2=w2.getWeightsForQuery(qry)
    print(t2)
    w3 = Weighter3(indexer) 
    t3=w3.getWeightsForQuery(qry)
    print(t3)

    v1 = Vectoriel(w1)
    s1 = v1.getScores(qry)
    print(s1)   
    
    v3 = Vectoriel(w3)
    s3 = v3.getScores(qry)
    print(s3)