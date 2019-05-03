
class Document:
    """
    Une classe Document qui nous sert a stocker un document,
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

    def getTexte(self):
        return self.texte


class Query(Document):

    def __init__(self):
        super().__init__()
        self.listPertinent = list()

    def addPertinent(self, idDoc):
        self.listPertinent.append(idDoc)

    def getPertinent(self):
        return self.listPertinent
