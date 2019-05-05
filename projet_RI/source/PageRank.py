import IRModel
import random


class PageRank(IRModel.IRModel):

    def __init__(self, weighter, model, damping=0, n=10, k=1):

        self.weighter = weighter
        self.model = model
        self.d = damping
        self.n = n
        self.k = k

    def getScores(self, Query, max_iter=50):

        seed = self.model.getRanking(Query)
        norm = sum([page[1] for page in seed[:min(self.n, len(seed))]])
        seed = {page[0]: (1 - self.d) * (page[1] / norm) for page in seed[:min(self.n, len(seed))]}

        graphe = self._initialiseGraphe(seed)
        # print(len(graphe))
        # print(len(seed))
        resultat = dict.fromkeys(graphe.keys(), 0)
        for _ in range(max_iter):

            # print(resultat)
            for page in resultat:
                # print('page =', page)
                score = 0

                for pageFrom in graphe[page]:
                    score += resultat.get(pageFrom, 0) / len(self.weighter.getHyperlinksTo(pageFrom))
                # print(score)
                resultat[page] = seed.get(page, 0) + (self.d * score)

        # print(len(resultat))
        # print(sum([resultat[i] for i in resultat]))
        return resultat

    def _initialiseGraphe(self, seed):

        graphe = dict()

        for idDoc in seed:
            graphe[idDoc] = set()
            for linkTo in self.weighter.getHyperlinksTo(idDoc):
                graphe[idDoc].add(linkTo)
                graphe[linkTo] = graphe.get(linkTo, set())

            linkFrom = self.weighter.getHyperlinksFrom(idDoc)

            for i in random.sample(linkFrom, min(len(linkFrom), self.k)):
                graphe[i] = graphe.get(i, set()) | {idDoc}

        return graphe

    def __str__(self):
        return "Page Rank sur le " + str(self.model)

