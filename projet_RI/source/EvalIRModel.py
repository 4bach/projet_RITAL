import Eval
import IndexerSimple
import Parser

import numpy as np


class EvalIRModel:

    def __init__(self, fichier, modelIR, weighter, verbose=False):

        self.verbose = verbose
        self.fichier = fichier

        self.collectionDoc = Parser.Parser.buildDocCollectionSimple(self.fichier + '.txt')
        self.collectionQry = Parser.Parser.buildQueryCollection(self.fichier)
        self.print_verbose("Recuperation des documents, et des query effectué")

        self.index = IndexerSimple.IndexerSimple()
        self.index.indexation(self.collectionDoc)
        self.print_verbose("Indexation de la collection fait")

        self.weighter = weighter(self.index)

        self.model = modelIR(self.weighter)

    def evalModel(self):

        PrecisionAtK = []
        RappelAtK = []
        for query in self.collectionQry:
            self.print_verbose('query =', self.collectionQry[query].getTexte())
            liste = [resultat[0] for resultat in self.model.getRanking(self.collectionQry[query].getTexte())]
            self.print_verbose(liste)
            PrecisionAtK.append(Eval.PrecisionAtK(10).evalQuery(liste, self.collectionQry[query]))
            RappelAtK.append(Eval.RappelAtK(10).evalQuery(liste, self.collectionQry[query]))
            self.print_verbose("score PrecisionAtK=", PrecisionAtK[-1])
        self.print_verbose(PrecisionAtK, RappelAtK)
        print(np.mean(PrecisionAtK))
        print(np.mean(RappelAtK))

    def print_verbose(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)