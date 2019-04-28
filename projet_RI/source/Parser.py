import re
from Document import Document 


class Parser:
    
    def buildDocCollectionSimple(fichier):
        """
            Construit l'index a partir d'une base de documents contenus dans fichier,
        On lit les lignes du fichier une par une, et on repère les balises texte .T
        et les balises id .I

        :type fichier: String
        :param fichier: Le fichier qui contient les documents que l'on veut indexé

        :return: Un dictionnaire de d'object Document, dont les clef sont les id des
                Document.
                {"id1": Document1, "id2": Document2, ...}
        """

        resultat = dict()
        lireID = ""
        text = ""
        inT = False  # Boolean qui nous indique si l'on est dans une balise texte
        d = Document()
        f = open(fichier, 'r')
        for l in f.readlines():  # Pour chaque ligne du fichier
            
            if inT:  # Si on est déjà dans une balise de texte

                if l.startswith("."):  # Et Si la ligne courante commence par un .
                    inT = False                # Alors cela signifie que l'on sort de la texte
                    d.setTexte(text)           # On va ajouter le texte que l'on a trouver dans notre document
                    resultat[lireID[:-1]] = d  # On ajoute notre document a notre dictionnaire resultat
                    lireID = ""

                else:                  # Sinon, c'est que l'on toujour dans notre balise texte
                    text = text + l 
                
            if len(lireID) > 0:  # Si a deja lu une balise id, mais pas encore de balise texte
                if l.startswith(".T"):  # Et que la ligne courante commence par un .T
                    inT = True  # alors on est dans une balise texte
                    text = ""
                
            if l[:2] == ".I":  # Si on a pas vue de balise id et que la ligne courante commence par .I
                lireID = l[3:]
                d = Document()  # On cree un nouveau document
                d.setID(int(lireID))  # Auquel on lui donne son id
                resultat[lireID[:-1]] = ""

        f.close()
        return resultat

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
            d = Document()
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
        
        
            