from collections import Counter
from TextRepresenter import PorterStemmer
import math


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
        return {i:1 for i in ps.getTextRepresentation(query)}
    
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
        return dict(Counter([i for i in ps.getTextRepresentation(query)]))



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
        return {i:math.log((1+self.indexer.getNbDoc())/(1+len(self.indexer.getTfsForStem(i)))) for i in ps.getTextRepresentation(query)}


class Weighter4(Weighter):
    pass

class Weighter5(Weighter):
    pass
        










            