#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Parser import Parser

import IndexerSimple
import Weighter
from IRModel import Vectoriel
# from Weighter import Weighter1
# from Weighter import Weighter2
# from Weighter import Weighter3
from TextRepresenter import PorterStemmer

qry = "Computers in Inspection Procedures Science Science"

if __name__ == "__main__":

    ####    TME 1 - Indexation    ####
    D = Parser.buildDocCollectionSimple('../cacmShort-good.txt')
    # print(D)
    # print("Texte du document 1 :", D[1].getTexte())
    # print("Representation du même document :", PorterStemmer().getTextRepresentation(D[1].getTexte()))

    indexer_simple = IndexerSimple.IndexerSimple()
    indexer_simple.indexation(D)

    # [print(indexer_simple.getTfsForDoc(i)) for i in range(1, len(D))]
    # [print(indexer_simple.getTfIDFsForDoc(i)) for i in range(1, len(D))]
    # print(indexer_simple.getTfsForStem('comput'))
    # print(indexer_simple.getTfIDFsForStem('comput'))
    # print(indexer_simple.getStrDoc(1))


    # ####    TME 2 - Appariment    ####

    w1 = Weighter.Weighter1(indexer_simple)
    t = w1.getWeightsForQuery(qry)
    # print("w1: ", t)
    w2 = Weighter.Weighter2(indexer_simple)
    t2 = w2.getWeightsForQuery(qry)
    # print("w2: ", t2)
    w3 = Weighter.Weighter3(indexer_simple)
    t3 = w3.getWeightsForQuery(qry)
    # print("w3: ", t3)
    w4 = Weighter.Weighter4(indexer_simple)
    t4 = w4.getWeightsForDoc(1)
    # print("w4: ", t4)
    t4 = w4.getWeightsForStem('comput')
    # print("w4: ", t4)
    t4 = w4.getWeightsForQuery(qry)
    # print("w4: ", t4)


    v1 = Vectoriel(w1, False)
    s1 = v1.getScores(qry)
    print("s1:",s1)
    sort = v1.getRanking(qry)

    for t in sort:
        print("doc:", t[0], " score:", t[1])
    v2 = Vectoriel(w2, False)
    s2 = v1.getScores(qry)
    print("s2:",s2)
    sort = v2.getRanking(qry)

    for t in sort:
        print("doc:", t[0], " score:", t[1])

    v3 = Vectoriel(w3, False)
    s3 = v3.getScores(qry)
    sort = v3.getRanking(qry)

    print("s3:",s3)
    for t in sort:
        print("doc:", t[0], " score:", t[1])

    v4 = Vectoriel(w4, False)
    s4 = v4.getScores(qry)
    sort = v4.getRanking(qry)

    print("s4:",s4)
    for t in sort:
        print("doc:", t[0], " score:", t[1])