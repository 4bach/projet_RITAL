
class Info:
    """
    Une classe abstraite Info qui nous sert a stocker les element indispensable d'une page,
    C'est a dire un ID et un texte
    """

    def __init__(self):
        self.identifiant = -1 
        self.texte = ""
    
    def setID(self, identifiant):
        self.identifiant = identifiant
    
    def getID(self):
        return self.identifiant
    
    def setTexte(self, texte):
        self.texte = texte

    def addTexte(self, texte):
        self.texte += texte

    def getTexte(self):
        return self.texte


class Document(Info):

    def __init__(self):
        super().__init__()
        self.linkTo = dict()

    def addLinkTo(self, idDoc):
        self.linkTo[idDoc] = self.linkTo.get(idDoc, 0) + 1

    def getLinkTo(self):
        return self.linkTo

class Query(Info):

    def __init__(self):
        super().__init__()
        self.listPertinent = list()

    def addPertinent(self, idDoc):
        self.listPertinent.append(idDoc)

    def getPertinents(self):
        return self.listPertinent
