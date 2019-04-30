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

    ####    TME 1 - Indexation    ####
    D = Parser.buildDocCollectionSimple('../cacmShort-good.txt')
    print(D)
    print("Texte du document 1 :", D[1].getTexte())
    print("Representation du même document :", PorterStemmer().getTextRepresentation(D[1].getTexte()))

    indexer_simple = IndexerSimple.IndexerSimple()
    indexer_simple.indexation(D)

    # [print(indexer_simple.getTfsForDoc(i)) for i in range(1, len(D))]
    [print(indexer_simple.getTfIDFsForDoc(i)) for i in range(1, len(D))]
    # print(indexer_simple.getTfsForStem('comput'))
    print(indexer_simple.getTfIDFsForStem('comput'))
    print(indexer_simple.getStrDoc(1))


    # ####    TME 2 - Appariment    ####
    #
    # w1 = Weighter1(indexer_simple)
    # t = w1.getWeightsForQuery(qry)
    # print("w1: ", t)
    # w2 = Weighter2(indexer_simple)
    # t2 = w2.getWeightsForQuery(qry)
    # print("w2: ", t2)
    # w3 = Weighter3(indexer_simple)
    # t3 = w3.getWeightsForQuery(qry)
    # print(w3.getWeightsForStem('comput'))
    # print("w3: ", t3)
    #
    # v1 = Vectoriel(w1, False)
    # s1 = v1.getScores(qry)
    # print("s1:",s1)
    #
    # v2 = Vectoriel(w2, False)
    # s2 = v1.getScores(qry)
    # print("s2:",s2)
    #
    # v3 = Vectoriel(w3, False)
    # s3 = v3.getScores(qry)
    # sort = v3.getRanking(qry)
    #
    # print("s3:",s3)