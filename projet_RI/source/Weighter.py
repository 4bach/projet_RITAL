from collections import Counter
from TextRepresenter import PorterStemmer
import math
import numpy as np


class Weighter:
    
    def __init__(self,indexer):
        self.indexer = indexer
        
        
    def getWeightsForDoc(self,idDoc):
        pass
        
    
    def getWeightsForStem(self,stem):
        pass
    
    def getNbDoc(self):
        pass
        
    def getWeightsForQuery(self,query):
        pass
    
    
        
    

class Weighter1(Weighter):
    
    def __init__(self,indexer):
        super().__init__(indexer)
        
        
    def getWeightsForDoc(self,idDoc):
        return self.indexer.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.indexer.getTfIDFsForStem(stem)
    

    def getWeightsForQuery(self,query): 
        ps = PorterStemmer()
        q_count=ps.getTextRepresentation(query)
        res=dict()
        for item in self.indexer.index_inv.keys():
            if item in q_count.keys():
                res[item]=1
#            else:
#                res[item]=0
        return res
    
    def getNbDoc(self):
        return self.indexer.getNbDoc()
        
        
        
        """
        qry = [porter.stem(i.lower()) for i in query.split() if i.lower() not in self.indexer.motvide]
        score = dict()
        for i in range(self.indexer.getNbDoc()):
            score[i]=0
            for j in qry:
                if j in self.indexer.getTfsForDoc(i):
                    score[i]+=1
            if len(qry)==score[i]:
                score[i] = 1 
            else:
                score[i] = 0
        return score
        """
        
    
        
    
class Weighter2(Weighter):
    
    def __init__(self,indexer):
        super().__init__(indexer)
        
        
    def getWeightsForDoc(self,idDoc):
        return self.indexer.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.indexer.getTfIDFsForStem(stem)
    
    def getNbDoc(self):
        return self.indexer.getNbDoc()

    def getWeightsForQuery(self,query):  
        ps = PorterStemmer()
        
        q_count=ps.getTextRepresentation(query)
        poids=dict()
        for item in self.indexer.index_inv.keys():
            if item in q_count.keys():
                poids[item]=q_count[item]
#            else:
#                res[item]=0
        return poids



class Weighter3(Weighter):
      
    def __init__(self,indexer):
        super().__init__(indexer)
        
        
    def getWeightsForDoc(self,idDoc):
        return self.indexer.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.indexer.getTfIDFsForStem(stem)
        
    def getNbDoc(self):
        return self.indexer.getNbDoc()

    def getWeightsForQuery(self,query): 
        ps = PorterStemmer()
         
        q_count=ps.getTextRepresentation(query)
        poids=dict()
        for item in self.indexer.index_inv.keys():
            if item in q_count.keys():
                poids[item]=np.log((self.indexer.getNbDoc()+1)/(1+len(self.indexer.getTfsForStem(item))))
#            else:
#                res[item]=0
        return poids
        


class Weighter4(Weighter):
    pass

class Weighter5(Weighter):
    pass
        










            