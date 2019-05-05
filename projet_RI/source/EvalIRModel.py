import Eval
import IndexerSimple
import IRModel
import PageRank
import Parser
import Weighter

import numpy as np


class EvalIRModel:

    def __init__(self, fichierQry, modelIR, k=5, beta=0.5, tailleTrain=0.8,verbose=False):

        self.verbose = verbose
        self.k = k
        self.beta = beta
        self.tailleTrain = 0.8

        self.model = modelIR

        self.collectionQry = Parser.Parser.buildQueryCollection(fichierQry) if type(fichierQry) is str else fichierQry
        self.print_verbose("Recuperation des queries effectué")

    def evalModel(self, k=None, beta=None):

        if k is not None:
            self.k = k

        if beta is not None:
            self.beta = beta

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

    def findParametreOptimaux(self, *args):
        # print(args)
        if len(args) == 0 or len(args) > 3:
            return
        self.tailleTrain = int(self.tailleTrain * len(self.collectionQry))

        train = dict()
        for qry in self.collectionQry:
            train[qry] = self.collectionQry[qry]
            if len(train) > self.tailleTrain:
                break

        self.collectionQry = {k: v for k, v in self.collectionQry.items() if k not in train}

        if len(args) == 1:  # Dans le Jelinek_Mercer
            resultat = []
            map = Eval.MAP()
            for parametre in args[0]:
                resultatModel = []
                # print(parametre)
                self.model.setParametre(parametre)
                for query in train:
                    resultatModel.append([resultat[0] for resultat in self.model.getRanking(train[query].getTexte())])

                resultat.append(map.evalQueries(resultatModel, train))
            # print(resultat)
            # print(max(resultat))
            # print(resultat.index(max(resultat)))
            # print("args[0][resultat.index(max(resultat))] = ", args[0][resultat.index(max(resultat))])
            self.model.setParametre(args[0][resultat.index(max(resultat))])

        if len(args) == 2:  # Dans le cas Okapi
            pass
        if len(args) == 3:
            pass

        print(args[0])

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
            self.model[-1].findParametreOptimaux(np.arange(0.8, 2, 0.1))
            self.model.append(EvalIRModel(collectionQry, PageRank.PageRank(m.getWeighter(), m)))

    def evalAllModel(self, k=1, beta=0.5):

        resultat = dict()
        for m in self.model:
            resultat[m] = m.evalModel(k, beta)

        precision = max(resultat.items(), key=lambda x: x[1][0][0])[0]
        print('Le modèle qui a la plus grande Precision a', k, 'est le', precision, 'pour, \nprecision =', resultat[precision][0][0], "en moyenne\net std =", resultat[precision][0][1])

        """
        evaluation = [Eval.PrecisionAtK(self.k)
            , Eval.RappelAtK(self.k)
            , Eval.FMesureAtK(self.k, self.beta)
            , Eval.AvgP()
            , Eval.reciprocalRank()
            , Eval.Ndcg()]
        
        """
