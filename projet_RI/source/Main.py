#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Parser import Parser

import IndexerSimple
import Weighter
import IRModel
from TextRepresenter import PorterStemmer

qry = "Computers Computers in Inspection Procedures Science Science"



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
    w5 = Weighter.Weighter5(indexer_simple)



    v1 = IRModel.Vectoriel(w1, False)
    s1 = v1.getScores(qry)
    sort = v1.getRanking(qry)
    print("s1:",s1)

    for t in sort:
        print("doc:", t[0], " score:", t[1])
    print()

    v2 = IRModel.Vectoriel(w2, False)
    s2 = v2.getScores(qry)
    sort = v2.getRanking(qry)
    print("s2:",s2)

    for t in sort:
        print("doc:", t[0], " score:", t[1])
    print()

    v3 = IRModel.Vectoriel(w3, False)
    s3 = v3.getScores(qry)
    sort = v3.getRanking(qry)

    print("s3:",s3)
    for t in sort:
        print("doc:", t[0], " score:", t[1])
    print()

    v4 = IRModel.Vectoriel(w4, False)
    s4 = v4.getScores(qry)
    sort = v4.getRanking(qry)

    print("s4:",s4)
    for t in sort:
        print("doc:", t[0], " score:", t[1])
    print()

    v5 = IRModel.Vectoriel(w5, False)
    s5 = v5.getScores(qry)
    sort = v5.getRanking(qry)

    print("s5:",s5)
    for t in sort:
        print("doc:", t[0], " score:", t[1])
    print()

    l = IRModel.Jelinek_Mercer(w1)
    l1 = l.getScores(qry)
    sort = l.getRanking(qry)

    print("l1:",l1)
    for t in sort:
        print("doc:", t[0], " score:", t[1])
    print()
