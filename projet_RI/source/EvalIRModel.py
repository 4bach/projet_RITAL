import Eval
import IndexerSimple
import IRModel
import Parser
import Weighter


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

        s = 0
        for query in self.collectionQry:
            self.print_verbose('query =', self.collectionQry[query].getTexte())
            liste = [resultat[0] for resultat in self.model.getRanking(self.collectionQry[query].getTexte())]
            self.print_verbose(liste)
            PrecisionAtK = Eval.PrecisionAtK().evalQuery(liste, self.collectionQry[query])
            self.print_verbose("score =", PrecisionAtK)
            s += PrecisionAtK
        self.print_verbose(s)
        print(s/len(self.collectionQry))

    def print_verbose(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)