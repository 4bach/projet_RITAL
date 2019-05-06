#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:58:38 2019

@author: ykarmim
"""
import math
import TextRepresenter


class IndexerSimple:

    def __init__(self):
        self.index = None
        self.index_inv = None
        self.tf_idf = None
        self.tf = None
        self.collection = None

    def setIndex(self, index):
        self.index = index

    def setIndex_inv(self, index_inv):
        self.index_inv = index_inv

    def setTf_idf(self, tf_idf):
        self.tf_idf = tf_idf

    def setTf(self, tf):
        self.tf = tf
        
    def getIndex(self):
        return self.index

    def getTfsForDoc(self, iddoc):
        return self.index[iddoc]

    def getTfIDFsForDoc(self, ind):
        return self.tf_idf[ind]

    def getTfsForStem(self, stem):
        if stem not in self.index_inv:
            return dict()
        return self.index_inv[stem]
        # return {i: self.tf[i][stem] for i in self.index_inv[stem]}

    def getTfIDFsForStem(self, stem):
        if stem not in self.index_inv:
            return dict()
        dico = dict()
        for iddoc in self.index_inv[stem].keys():
            dico[iddoc] = self.tf_idf[int(iddoc)][stem]
        return dico

    def getIdfForStem(self, stem):
        return math.log((1 + self.getNbDoc()) / (1 + len(self.index_inv[stem])))

    def getStrDoc(self, iddoc):
        return self.collection[iddoc].getTexte()

    def getNbDoc(self):
        return len(self.index)

    def getLengthDocs(self):
        return sum(len(self.collection[doc].getTexte()) for doc in self.collection)

    def getHyperlinksFrom(self, idDoc):
        return self.collection[idDoc].getHyperlinksFrom()

    def getHyperlinksTo(self, idDoc):
        return self.collection[idDoc].getHyperlinksTo()

    @staticmethod
    def countWord(doc):
        """
            On fait appel a la methode getTextRepresentation qui nous donne la representation d'un doc, et qui compte
        le nombre d'occurence de charque mot lemmatisé

        :type doc: String
        :param doc: le document que dont on veux la representation
        :return: un dictionnaire qui reprensente le doc
        """
        return TextRepresenter.PorterStemmer().getTextRepresentation(doc)

    def indexation(self, collection):
        self.collection = collection

        index = dict()
        index_inv = dict()
        tf_idf = dict()
        tf = dict()
        for id in collection:
            index[collection[id].getID()] = IndexerSimple.countWord(collection[id].getTexte())
            for j in index[id]:
                if j in index_inv:
                    index_inv[j][id] = index[id][j]
                else:
                    index_inv[j] = {id: index[id][j]}

        for i in index:
            taille = sum([index[i][n] for n in index[i]])

            tf[i] = {mot: (index[i][mot] / taille) for mot in index[i]}
            tf_idf[i] = {mot: (index[i][mot] / taille) * math.log((1 + len(collection)) / (1 + len(index_inv[mot]))) for
                         mot in index[i]}

        self.setIndex(index)
        self.setIndex_inv(index_inv)
        self.setTf(tf)
        self.setTf_idf(tf_idf)
