import operator
import numpy as np


class IRModel:

    def __init__(self, weighter):
        self.weighter = weighter

    def getScores(self, query):
        pass

    def getRanking(self, query):
        s = self.getScores(query)
        sort = sorted(s.items(), key=operator.itemgetter(1), reverse=True)
        return sort


class Vectoriel(IRModel):

    def __init__(self, weighter, normalized=False):
        super().__init__(weighter)
        self.normalized = normalized

    def getScores(self, query):

        query = self.weighter.getWeightsForQuery(query)
        print('query =', query)

        score = dict()

        if self.normalized:
            pass

        else:
            for stem in query:
                weights_stem = self.weighter.getWeightsForStem(stem)
                for doc in weights_stem:
                    score[doc] = score.get(doc, 0) + weights_stem[doc] * query[stem]

        return score


class Jelinek_Mercer(IRModel):

    def __init__(self, weighter, lambda_=0.2):
        super().__init__(weighter)
        self.lambda_ = lambda_

    def getScores(self, query):

        tailleCorpus = self.weighter.getLengthDocs()
        query = self.weighter.getWeightsForQuery(query)
        print('query =', query)

        score = dict()

        for stem in query:
            tf_total = (1 - self.lambda_) * sum(nb for _, nb in self.weighter.getTfsForStem(stem).items()) / tailleCorpus

            weights_stem = self.weighter.getWeightsForStem(stem)

            for doc in weights_stem:
                score[doc] = score.get(doc, 0) + (self.lambda_ * (weights_stem[doc] / self.weighter.getLengthDoc(doc))) + tf_total

        return score

class Langue(IRModel):

    def __init__(self, index, Weighter, alpha):
        self.weighter = Weighter
        self.index = index
        self.alpha = alpha

    def getScores(self, query):
        return self.score_langue(query, 1,self.weighter, self.alpha)

    def m_score_langue(self, query, weighter, alpha):
        q_count = weighter.getWeightsForQuery(query)
        list_id_doc = set()
        for item in q_count.keys():
            for doc in weighter.index.index_inv[item].keys():
                list_id_doc.add(doc)
        list_id_doc = list(list_id_doc)
        res = dict()
        for doc in list_id_doc:
            res[doc] = self.score_langue(q_count, doc, weighter, alpha)
        return res

    def score_langue(self, q_count, d, weighter, alpha):
        prod1 = 1
        prod2 = 1
        # print(weighter.index.index[d])
        somme1 = sum(weighter.indexer.index[d].values())
        print(somme1)
        somme2 = sum([sum(weighter.index.index_inv[w].values()) for w in weighter.index.index_inv.keys()])
        for word in q_count.keys():
            if word in weighter.index.index[d].keys():
                prod1 *= weighter.index.index[d][word] / somme1
                prod2 *= sum(weighter.index.index_inv[word].values()) / somme2

        return alpha * prod1 + (1 - alpha) * prod2


class okapi(IRModel):

    def __init__(self, index, Weighter, b, k1):
        self.index = index
        self.weighter = Weighter
        self.b = b
        self.k1 = k1

    def getScores(self, query):

        return self.score_okapi(query, self.weighter, self.b, self.k1)

    def m_score_okapi(self, query, weighter, b, k1):
        q_count = weighter.getWeightsForQuery(query)
        list_id_doc = set()
        for item in q_count.keys():
            for doc in weighter.index.index_inv[item].keys():
                list_id_doc.add(doc)
        list_id_doc = list(list_id_doc)
        res = dict()

        ldmoy = 0
        for doc in weighter.index.index.keys():
            ldmoy += sum(weighter.index.index[doc].values())
        ldmoy /= len(weighter.index.index.keys())

        for doc in list_id_doc:
            res[doc] = self.score_okapi(q_count, doc, weighter, b, k1, ldmoy)
        return res

    def score_okapi(self, q_count, d, weighter, b, k1, ldmoy):
        somme = 0
        N = len(weighter.index.index)
        ld = sum(weighter.index.index[d].values())
        ld /= ldmoy

        for word in q_count.keys():
            if word in weighter.index.index[d].keys():
                n = len(weighter.index.index_inv[word])
                idf = np.log(N / n)
                tfyd = weighter.index.index[d][word]
                denominateur = tfyd + k1 * (1 - b + b * ld)
                somme += idf * tfyd / denominateur

        return somme
