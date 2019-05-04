import math

class EvalMesure:

    def evalQuery(self, liste, Query):
        pass


class PrecisionAtK(EvalMesure):

    def __init__(self, k=1):
        self.k = k

    def evalQuery(self, liste, Query):

        resultat = 0
        pertinent = Query.getPertinents()
        for doc in range(min(len(liste), self.k)):
            if liste[doc] in pertinent:
                resultat += 1

        return resultat/self.k


class RappelAtK(EvalMesure):

    def __init__(self, k=1):
        self.k = k

    def evalQuery(self, liste, Query):

        resultat = 0
        pertinent = Query.getPertinents()
        if len(pertinent) is 0:
            return 0
        for doc in range(min(len(liste), self.k)):
            if liste[doc] in pertinent:
                resultat += 1

        return resultat/len(pertinent)


class FMesureAtK(EvalMesure):

    def __init__(self, k=1, beta=0.5):
        self.k = k
        self.beta = beta

    def evalQuery(self, liste, Query):

        p = PrecisionAtK(self.k).evalQuery(liste, Query)
        r = RappelAtK(self.k).evalQuery(liste, Query)

        return (1 + self.beta) * ((p * r) / (self.beta * p + r)) if p + r > 0 else 0


class AvgP(EvalMesure):

    def evalQuery(self, liste, Query):

        pertinent = Query.getPertinents()
        if len(pertinent) is 0:
            return 0

        resultat = 0
        truePositive = 0

        for i in range(len(liste)):
            if liste[i] in pertinent:
                truePositive += 1
                resultat += truePositive/ (i + 1)

        return resultat / len(pertinent)


class MAP:

    def evalQueries(self, l_liste, l_Query):

        resultat = 0
        mesure = AvgP()

        for i in range(len(l_liste)):
            resultat += mesure.evalQuery(l_liste[i], l_Query[i])

        return resultat / len(l_liste)


class reciprocalRank(EvalMesure):

    def evalQuery(self, liste, Query):
        return 1 / (1 + Query.getPertinents().index(liste[0])) if liste[0] in Query.getPertinents() else 0


class Ndcg(EvalMesure):

    def evalQuery(self, liste, Query):

        pertinent = Query.getPertinents()

        # Discounted Cumulative Gain
        dcg = 1 if liste[0] in pertinent else 0  # si le premiere resultat est pertinent alors 1 sinon 0
        idcg = 1  # Ideal Discounted Cumulative Gain

        for i in range(1, len(liste)):  # Pour chaque doc resultat

            if liste[i] in pertinent:  # Si le document i est pertinent
                dcg += 1 / math.log(i + 1, 2)  # On utilise en log en base 2
            idcg += 1 / math.log(i + 1, 2)

        return dcg / idcg