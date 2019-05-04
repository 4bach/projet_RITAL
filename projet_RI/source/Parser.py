import re
import Document


class Parser:

    @staticmethod
    def buildDocCollectionSimple(fichier, baliseText='.T'):
        """
            Construit l'index a partir d'une base de documents contenus dans fichier,
        On lit les lignes du fichier une par une, et on repère les balises texte .T
        et les balises id .I (les balises texte pour une requete sont .W)

        :type fichier: String
        :param fichier: Le fichier qui contient les documents que l'on veut indexé

        :type baliseText: String
        :param baliseText: La balise que l'on va utilier pour recuperer le texte, .T pour un doc, .W pour une requête

        :return: Un dictionnaire de d'object Document, dont les clef sont les id des
                Document.
                {"id1": Document1, "id2": Document2, ...}
        """

        resultat = dict()
        lireID = -1
        text = ""
        inT = False  # Boolean qui nous indique si l'on est dans une balise texte
        d = Document.Document() if baliseText == '.T' else Document.Query()
        f = open(fichier, 'r')
        for l in f.readlines():  # Pour chaque ligne du fichier
            
            if inT:  # Si on est déjà dans une balise de texte

                if l.startswith("."):  # Et Si la ligne courante commence par un .
                    inT = False                # Alors cela signifie que l'on sort de la texte
                    d.setTexte(text)           # On va ajouter le texte que l'on a trouver dans notre document
                    resultat[lireID] = d  # On ajoute notre document a notre dictionnaire resultat
                    lireID = -1

                else:                  # Sinon, c'est que l'on toujour dans notre balise texte
                    text = text + l 
                
            if lireID > 0:  # Si a deja lu une balise id, mais pas encore de balise texte
                if l.startswith(baliseText):  # Et que la ligne courante commence par un .T
                    inT = True  # alors on est dans une balise texte
                    text = ""
                
            if l[:2] == ".I":  # Si on a pas vue de balise id et que la ligne courante commence par .I
                lireID = int(l[3:])
                d = Document.Document() if baliseText == '.T' else Document.Query()
                d.setID(lireID)  # Auquel on lui donne son id
                resultat[lireID] = ""

        f.close()
        return resultat

    @staticmethod
    def buildDocumentCollectionRegex(fichier):
        """
            Construit l'index a partir d'une base de documents contenus dans fichier,
        On lit le fichier en entier et on utilise des expressions régulières pour
        récupère le contenu des balises

        :type fichier: String
        :param fichier: Le fichier qui contient les documents que l'on veut indexé

        :return: Un dictionnaire de d'object Document, dont les clef sont les id des
                Document.
                {"id1": Document1, "id2": Document2, ...}
        """
        resultat = dict()
        
        f = open(fichier, 'r')
        doc = f.read()
        docs = doc.split(".I")
    
        for di in range(1, len(docs)):
            d = Document.Document()
            id_doc = re.search(r'(\d*|$)', docs[di][1:]).group(0)
            d.setID(int(id_doc))
            m = re.search(r'\.T(.*?)\.', docs[di], re.DOTALL)
            if m is not None:
                d.setTexte(m.group(1).replace('\n', ' '))
                
            else:
                d.setTexte("")
            
            resultat[id_doc] = d
        f.close()
        return resultat

    @staticmethod
    def buildQueryCollection(fichierQry, fichierRel=None):

        if fichierRel is None:
            fichierRel = fichierQry + '.rel'
            fichierQry = fichierQry + '.qry'

        collection = Parser.buildDocCollectionSimple(fichierQry, ".W")
        Parser.buildPertinenceQuery(collection, fichierRel)

        return collection

    @staticmethod
    def buildPertinenceQuery(collection, fichierRel):

        f = open(fichierRel, 'r')
        for ligne in f.readlines():  # Pour chaque ligne du fichier

            pertinence = [int(n) for n in re.findall('\d+', ligne)]
            collection[pertinence[0]].addPertinent(pertinence[1])


