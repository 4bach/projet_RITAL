import Eval
import IndexerSimple
import IRModel
import PageRank
import Parser
import Weighter

import numpy as np


class EvalIRModel:
    """
    
    """

    def __init__(self, fichierQry, modelIR, k=5, beta=0.5, tailleTrain=0.8, verbose=False):

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

    def print_verbose(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    def __str__(self):
        return str(self.model)


class EvalAllIRModel:

    def __init__(self, fichier, metrique="FMesure", tailleTrain=0.65):

        collection = Parser.Parser.buildDocCollectionSimple(fichier + '.txt', pageRank=True)
        self.collectionQry = Parser.Parser.buildQueryCollection(fichier)
        self.train = dict()
        self.separeTrainTest(tailleTrain)

        index = IndexerSimple.IndexerSimple()
        index.indexation(collection)

        self.weighter = [Weighter.Weighter1(index), Weighter.Weighter2(index), Weighter.Weighter3(index),
                         Weighter.Weighter4(index), Weighter.Weighter5(index)]

        modelIR = [IRModel.Vectoriel, IRModel.Jelinek_Mercer, IRModel.Okapi]

        model = []

        for w in self.weighter:
            for m in range(len(modelIR)):
                
                if m == 1:  # pour le modèle Jelinek_Mercer
                    jelinek = modelIR[m](w)
                    jelinek.findParametreOptimaux(np.arange(0, 1.4, 0.1), self.train, metrique)
                    model.append(jelinek)
                elif m == 2:  # pour le modèle Okapi
                    pass
                else:  # pour le modèle Vectoriel
                    model.append(modelIR[m](w))  # il n'y a pas de parametre a optimiser

        self.model = []

        for m in model:
            self.model.append(EvalIRModel(self.collectionQry, m))
            self.model.append(EvalIRModel(self.collectionQry, PageRank.PageRank(m.getWeighter(), m)))

    def separeTrainTest(self, tailleTrain=0.8):
                
        tailleTrain = int(tailleTrain * len(self.collectionQry))

        for qry in self.collectionQry:
            self.train[qry] = self.collectionQry[qry]
            if len(self.train) > tailleTrain:
                break

        self.collectionQry = {k: v for k, v in self.collectionQry.items() if k not in self.train}

    def evalAllModel(self, k=1, beta=0.5):

        resultat = dict()
        for m in self.model:
            resultat[m] = m.evalModel(k, beta)


        precision = max(resultat.items(), key=lambda x: x[1][0][0])[0]
        rappel = max(resultat.items(), key=lambda x: x[1][1][0])[0]
        print('Le modèle qui a la plus grande Precision a', k, 'est le', precision, 'pour, \nprecision =', resultat[precision][0][0], "en moyenne\net std =", resultat[precision][0][1])
        print('Le modèle qui a le plus grand rappel a', k, 'est le', rappel, 'pour, \nrappel =', resultat[rappel][0][0], "en moyenne\net std =", resultat[rappel][0][1])

        """
        evaluation = [Eval.PrecisionAtK(self.k)
            , Eval.RappelAtK(self.k)
            , Eval.FMesureAtK(self.k, self.beta)
            , Eval.AvgP()
            , Eval.reciprocalRank()
            , Eval.Ndcg()]
        
        """
