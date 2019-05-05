import Eval
import IndexerSimple
import IRModel
import PageRank
import Parser
import Weighter

import numpy as np


class EvalIRModel:

    def __init__(self, fichierQry, modelIR, k=1, beta=0.5, verbose=False):

        self.verbose = verbose
        self.k = k
        self.beta = beta

        self.model = modelIR

        self.collectionQry = Parser.Parser.buildQueryCollection(fichierQry) if type(fichierQry) is str else fichierQry
        self.print_verbose("Recuperation des queries effectué")

    def evalModel(self, k=None):

        if k is not None:
            self.k = k

        evaluation = [Eval.PrecisionAtK(self.k)
            , Eval.RappelAtK(self.k)
            , Eval.FMesureAtK(self.k, self.beta)
            , Eval.AvgP()
            , Eval.reciprocalRank()
            , Eval.Ndcg()]
        resultat = [[] for _ in range(len(evaluation))]

        for query in self.collectionQry:
            self.print_verbose('query =', self.collectionQry[query].getTexte())
            liste = [resultat[0] for resultat in self.model.getRanking(self.collectionQry[query].getTexte())]
            self.print_verbose(liste)
            for i in range(len(evaluation)):
                resultat[i].append(evaluation[i].evalQuery(liste, self.collectionQry[query]))
        self.print_verbose(resultat)
        return [(np.mean(l), np.std(l)) for l in resultat]

    def print_verbose(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    def __str__(self):
        return str(self.model)


class EvalAllIRModel:

    def __init__(self, fichier):

        collection = Parser.Parser.buildDocCollectionSimple(fichier + '.txt', pageRank=True)
        collectionQry = Parser.Parser.buildQueryCollection(fichier)

        index = IndexerSimple.IndexerSimple()
        index.indexation(collection)

        self.weighter = [Weighter.Weighter1(index), Weighter.Weighter2(index), Weighter.Weighter3(index),
                         Weighter.Weighter4(index), Weighter.Weighter5(index)]

        modelIR = [IRModel.Vectoriel, IRModel.Jelinek_Mercer, IRModel.Okapi]

        model = []

        for m in modelIR:
            for w in self.weighter:
                model.append(m(w))

        self.model = []

        for m in model:
            self.model.append(EvalIRModel(collectionQry, m))
            self.model.append(EvalIRModel(collectionQry, PageRank.PageRank(m.getWeighter(), m)))

    def evalAllModel(self, k=1):

        for m in self.model:
            print(m)
            print(m.evalModel(k))
            print()
