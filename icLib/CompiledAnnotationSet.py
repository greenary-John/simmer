import math
import time

import Logger

class CompiledAnnotationSet:

    def __init__(self,AnnSet,evCodes,ontman):
        self.count=0
        self.ontman=ontman
        self.evCodes=evCodes if isinstance(evCodes,list) else [evCodes]
        self.annset=AnnSet.evidenceFilter(self.evCodes)
        self.logger=Logger.Logger()
        self.Compute_obj2term()
        self.Compute_term2obj()
        self.Compute_term2IC()
        #self.Compute_pair2MICA()

    def Compute_term2obj(self):
        self.term2obj={}
        for x in self.annset.getAnnotatedTerms():
                temp=set([])
                for y in self.annset.ontology.closure[x]:
                    try:
                        for z in self.annset.annotsByID[y]:
                            try:
                                temp.add(z.annObj)
                            except KeyError:
                                continue
                    except KeyError:
                        continue
                self.term2obj[x]=temp

    def Compute_obj2term(self):
        self.obj2term={}
        for x in self.annset.getAnnotatedObjects():
            temp=[]
            for y in self.annset.annotsByObj[x]:
                temp.append(y.ontTerm)
            self.obj2term.setdefault(x,set([])).update(temp)

    def Compute_term2IC(self):
        self.annotationCardinality=len(self.annset.getAnnotatedObjects())
        self.term2IC={}
        for x in self.term2obj:
            if len(self.term2obj[x])==0:
                self.term2IC[x]=None
            else:
                self.term2IC[x]=math.log(self.annotationCardinality/float(len(self.term2obj[x])))
                
    def Compute_pair2MICA(self):
        self.pair2MICA={}
        for x in self.term2IC:
            for y in self.term2IC:
                if self.pair2MICA.has_key((y,x)):
                    continue
                else:                    
                    self.pair2MICA.update[(x,y)]=self.getMICAscore(x,y)
                    
    def maxIC(self,lst):
        return max([self.term2IC.get(x,0)for x in lst])if len(lst)>0 else 0

    def getMICAscore(self,termA,termB):
        self.count+=1
        return self.maxIC(self.annset.ontology.reverseClosure[termA]&self.annset.ontology.reverseClosure[termB])

    def rowMICA(self,termA,objB):
        #term to obj comparison
        return max([self.getMICAscore(termA,y)for y in self.obj2term[objB]])if len(self.obj2term[objB])>0 else 0

    def objCompare(self,objA,objB):
        #obj to obj comparison
        lst=([self.rowMICA(y,objB)for y in self.obj2term[objA]])
        return float(sum(lst))/len(lst) if len(lst)>0 else 0
        
    def resnikResults(self,objA,length):
        #BMA approach; obj to list of objs comparison
        start=time.time()
        resultsDict={}
        returnDict={}
        count=0
        for x in self.obj2term:
            resultsDict[x]=self.objCompare(objA,x)
        for x in sorted(resultsDict,key=lambda entry:resultsDict[entry],reverse=True):
            if count>=length:
                break
            returnDict[x]=resultsDict[x]
            count+=1
        self.logger.debug("".join(("\nFinished!\t\t\t",str(self.count)," MICA calculations\nactual runtime:\t\t",str(time.time()-start)," seconds\n")))
        return returnDict
