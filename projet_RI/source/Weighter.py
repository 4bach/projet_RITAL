from collections import Counter
from TextRepresenter import PorterStemmer
import math
import IndexerSimple
import numpy as np


class Weighter:

    def __init__(self, indexer):
        self.indexer = indexer

    def getWeightsForDoc(self, idDoc):
        return self.indexer.getTfsForDoc(idDoc)

    def getWeightsForStem(self, stem):
        return self.indexer.getTfIDFsForStem(stem)

    def getNbDoc(self):
        return self.indexer.getNbDoc()

    def getWeightsForQuery(self, query):
        pass


class Weighter1(Weighter):
    """
        Premier schéma pour la ponderation des documents et des query.

    poid doc = tf
    poid query = 1 if terme in query else 0
    """

    def __init__(self, indexer):
        super().__init__(indexer)

    def getWeightsForQuery(self, query):
        return {terme: 1 for terme in self.indexer.countWord(query)}


class Weighter2(Weighter):
    """
        Deuxième schéma pour la ponderation des documents et des query.

    poid doc = tf
    poid query = tf
    """
    def __init__(self, indexer):
        super().__init__(indexer)

    def getWeightsForQuery(self, query):
        query_rep = self.indexer.countWord(query)
        taille_query_rep = sum([query_rep[n] for n in query_rep])
        return {terme: (query_rep[terme]/taille_query_rep) for terme in query_rep}


class Weighter3(Weighter):
    """
        troisième schéma pour la ponderation des documents et des query.

    poid doc = tf
    poid query = idf if terme in query else 0
    """
    def __init__(self, indexer):
        super().__init__(indexer)

    def getWeightsForQuery(self, query):

        resultat = dict()
        for terme in self.indexer.countWord(query):
            if terme in self.indexer.index_inv:
                resultat[terme] = math.log((1 + self.indexer.getNbDoc()) / (1 + len(self.indexer.index_inv[terme])))
        return resultat


class Weighter4(Weighter):

    def getWeightsForDoc(self, idDoc):
        tf_doc = self.indexer.getTfsForDoc(idDoc)
        return {terme: 1 + math.log(tf_doc[terme]) for terme in tf_doc}

    def getWeightsForStem(self, stem):
        tf_stem = self.indexer.getTfIDFsForStem(stem)
        return {terme: 1 + math.log(tf_stem[terme]) for terme in tf_stem}

    def getWeightsForQuery(self, query):

        resultat = dict()
        for terme in self.indexer.countWord(query):
            if terme in self.indexer.index_inv:
                resultat[terme] = math.log((1 + self.indexer.getNbDoc()) / (1 + len(self.indexer.index_inv[terme])))
        return resultat

class Weighter5(Weighter):
    pass
