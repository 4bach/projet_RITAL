class IRModel:
    
    def __init__(self,weighter):
        self.weighter = weighter
        
    def getScores(self,query):
        pass
    
    def getRanking(self,query):
        pass
    
    
class Vectoriel(IRModel):
    
    def __init__(self,weighter):
        super().__init__(weighter)
                        
    def getScores(self,query,normalized=False):
        
        query = self.weighter.getWeightsForQuery(query)
        
        score = dict()
        Y = []
        for doc in range(self.weighter.getNbDoc()):
            score[doc]=0
        for mot in query:
            for docu in self.weighter.getWeightsForStem(mot):
                
                y = float(self.weighter.getWeightsForStem(mot)[docu])
                Y.append(y)
                score[int(docu)]+=(query[mot]*y)
        
        if normalized:
            return 
        else:
            return score
    
    def getRanking(self,query):
        pass