import IRModel
import random
import numpy as np


class PageRank(IRModel.IRModel):

    def __init__(self, weighter, model, damping=0, n=10, k=1):

        self.weighter = weighter
        self.model = model
        self.d = damping
        self.n = n
        self.k = k

    def getScores(self, Query, max_iter=50):

        seed = self.model.getRanking(Query)
        # prior = {page[0]: ((1 - self.d) * page[1]) for page in seed[:min(self.n, len(seed))]}
        # seed = [page[0] for page in seed[:min(self.n, len(seed))]]
        norm = sum([page[1] for page in seed[:min(self.n, len(seed))]])
        seed = {page[0]: (1 - self.d) * (page[1] / norm) for page in seed[:min(self.n, len(seed))]}

        graphe = self._initialiseGraphe(seed)
        print(len(graphe))
        print(len(seed))
        resultat = dict.fromkeys(graphe.keys(), 0)
        for _ in range(max_iter):

            print(resultat)
            for page in resultat:
                # print('page =', page)
                score = 0

                for pageFrom in graphe[page]:
                    score += resultat.get(pageFrom, 0) / len(self.weighter.getHyperlinksTo(pageFrom))
                # print(score)
                resultat[page] = seed.get(page, 0) + (self.d * score)

        print(len(resultat))
        print(sum([resultat[i] for i in resultat]))
        return resultat

    def _initialiseGraphe(self, seed):

        graphe = dict()

        for idDoc in seed:
            # graphe[idDoc] = seed[idDoc]
            graphe[idDoc] = set()
            for linkTo in self.weighter.getHyperlinksTo(idDoc):
                graphe[idDoc].add(linkTo)
                graphe[linkTo] = graphe.get(linkTo, set())


            linkFrom = self.weighter.getHyperlinksFrom(idDoc)

            for i in random.sample(linkFrom, min(len(linkFrom), self.k)):
                graphe[i] = graphe.get(i, set()) | {idDoc}

        return graphe




    # def getScores(self, Query, max_iter=10):
    #
    #     seed = self.model.getRanking(Query)
    #     # prior = {page[0]: ((1 - self.d) * page[1]) for page in seed[:min(self.n, len(seed))]}
    #     # seed = [page[0] for page in seed[:min(self.n, len(seed))]]
    #     seed = {page[0]: (1 - self.d) * page[1] for page in seed[:min(self.n, len(seed))]}
    #
    #     idpage, graphe = self._initialiseGraphe(seed)
    #     resultat = np.zeros(len(idpage))
    #     print(resultat.shape)
    #     print(graphe.shape)
    #
    #     for _ in range(max_iter):
    #
    #         resultat = np.dot(resultat, graphe)
    #         print(resultat)
    #         #
    #         # for page in range(len(idpage)):
    #         #
    #         #
    #         #
    #         #
    #         #     for pageFrom in self.weighter.getHyperlinksFrom(idpage[page]):
    #         #         score += graphe.get(pageFrom, 0) / len(self.weighter.getHyperlinksTo(pageFrom))
    #         #     graphe[page] = seed.get(page, 0) + (self.d * score)
    #         #
    #
    # def _initialiseGraphe(self, seed):
    #
    #     idpage = set()
    #     graphe = dict()
    #
    #     for idDoc in seed:
    #         print(idDoc)
    #         idpage.add(idDoc)
    #         graphe[idDoc] = []
    #         for linkTo in self.weighter.getHyperlinksTo(idDoc):
    #             idpage.add(linkTo)
    #             graphe[idDoc].append(linkTo)
    #             graphe[linkTo] = []
    #
    #         linkFrom = self.weighter.getHyperlinksFrom(idDoc)
    #
    #         for i in random.sample(linkFrom, min(len(linkFrom), self.k)):
    #             idpage.add(i)
    #             graphe[i] = graphe.get(i, []) + [idDoc]
    #
    #     print(graphe)
    #     idpage = list(idpage)
    #     print(len(idpage))
    #     resultat = []
    #     for page in idpage:
    #         resPage = [0 for _ in range(len(idpage))]
    #         for pageTo in graphe[page]:
    #             resPage[idpage.index(pageTo)] = 1
    #         resultat.append(resPage)
    #
    #     graphe = np.matrix(resultat)
    #     graphe.transpose()
    #     print(graphe)
    #     sumCol = graphe.sum(axis=1)
    #     print(sumCol)
    #     graphe = graphe/sumCol
    #
    #     return idpage, graphe
