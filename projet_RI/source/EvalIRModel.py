import Eval
import IndexerSimple
import Parser

import numpy as np


class EvalIRModel:

    def __init__(self, fichier, modelIR, k=1, beta=0.5, verbose=False):

        self.verbose = verbose
        self.k = k
        self.beta = beta

        self.fichier = fichier
        self.model = modelIR

        self.collectionQry = Parser.Parser.buildQueryCollection(self.fichier)
        self.print_verbose("Recuperation des queries effectué")

    def evalModel(self):

        eval = [Eval.PrecisionAtK(self.k)
                , Eval.RappelAtK(self.k)
                , Eval.FMesureAtK(self.k, self.beta)
                , Eval.AvgP()
                , Eval.reciprocalRank()
                , Eval.Ndcg()]
        resultat = [[] for _ in range(len(eval))]

        for query in self.collectionQry:
            self.print_verbose('query =', self.collectionQry[query].getTexte())
            liste = [resultat[0] for resultat in self.model.getRanking(self.collectionQry[query].getTexte())]
            self.print_verbose(liste)
            for i in range(len(eval)):
                resultat[i].append(eval[i].evalQuery(liste, self.collectionQry[query]))
        self.print_verbose(resultat)
        return [(np.mean(l), np.std(l)) for l in resultat]

    def print_verbose(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)


