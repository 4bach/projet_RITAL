#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Parser import Parser

import IndexerSimple
from IRModel import Vectoriel
from Weighter import Weighter1
from Weighter import Weighter2
from Weighter import Weighter3
from TextRepresenter import PorterStemmer

qry = "Computers in Inspection Procedures Science"

if __name__ == "__main__":

    ####    TME 1 - Indexation      ####
    D = Parser.buildDocCollectionSimple('../cacmShort-good.txt')
    print("Texte du document 1 :", D['1'].getTexte())
    print("Representation du même document :", PorterStemmer().getTextRepresentation(D['1'].getTexte()))

    indexer_simple = IndexerSimple.IndexerSimple()
    indexer_simple.indexation(D)

    print(indexer_simple.getTfsForDoc(1))
    print(indexer_simple.getTfIDFsForDoc(1))
    print(indexer_simple.getTfsForStem('comput'))
    print(indexer_simple.getTfIDFsForStem('comput'))

    # w1 = Weighter1(indexer)
    # t=w1.getWeightsForQuery(qry)
    # print("w1: ",t)
    # w2 = Weighter2(indexer)
    # t2=w2.getWeightsForQuery(qry)
    # print("w2: ",t2)
    # w3 = Weighter3(indexer)
    # t3=w3.getWeightsForQuery(qry)
    # print("w3: ",t3)
    #
    # v1 = Vectoriel(w1)
    # s1 = v1.getScores(qry)
    # print("s1:",s1)
    #
    # v2 = Vectoriel(w2)
    # s2 = v1.getScores(qry)
    # print("s2:",s2)
    #
    # v3 = Vectoriel(w3)
    # s3 = v3.getScores(qry)
    # sort = v3.getRanking(qry)
    #
    # print("s3:",s3)