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
                self.term2obj.update({x:temp})

    def Compute_obj2term(self):
        self.obj2term={}
        for x in self.annset.getAnnotatedObjects():
            temp=set([])
            for y in self.annset.annotsByObj[x]:
                temp.update(self.annset.ontology.reverseClosure[y.ontTerm])
            self.obj2term.setdefault(x,set([])).update(temp)

    def Compute_term2IC(self):
        self.annotationCardinality=len(self.annset.getAnnotatedObjects())
        self.term2IC={}
        for x in self.term2obj:
            try:
                self.term2IC.update({x:math.log(self.annotationCardinality/float(len(self.term2obj[x])))})
            except ZeroDivisionError:
                self.term2IC.update({x:None})
                
    def Compute_pair2MICA(self):
        self.pair2MICA={}
        for x in self.term2IC:
            for y in self.term2IC:
                if self.pair2MICA.has_key((y,x)):
                    continue
                else:                    
                    self.pair2MICA.update({(x,y):self.MICA(x,y)})
                    
    def maxIC(self,lst):
        maximum=0
        for x in lst:
            if self.term2IC.has_key(x):
                if self.term2IC[x]>maximum:
                    maximum=self.term2IC[x]
            else:
                continue
        return maximum

    def MICA(self,termA,termB):
        self.count+=1
        return self.maxIC(self.annset.ontology.reverseClosure[termA]&self.annset.ontology.reverseClosure[termB])

    def rowMICA(self,termA,objB):
        #term to obj comparison
        maximum=0
        count=0
        if len(self.obj2term[objB])>0:
            for y in set.union(self.obj2term[objB]):
                if self.MICA(termA,y)>maximum:
                    maximum=self.MICA(termA,y)
                    count+=1
        return maximum

    def objCompare(self,objA,objB):
        #obj to obj comparison
        lst=[]
        count=0
        if len(self.obj2term[objA])>0:
            for y in set.union(self.obj2term[objA]):
                lst.append(self.rowMICA(y,objB))
                count+=1
            return sum(lst)/len(lst)
        return 0

    def resnikResults(self,objA,length):
        #BMA approach; obj to list of objs comparison
        start=time.time()
        resultsDict={}
        returnDict={}
        count=0
        count2=0
        for x in self.obj2term:
            resultsDict.update({x:self.objCompare(objA,x)})
            count2+=1
            if count2%1000==0:
                self.logger.debug("".join(("\n",str(count2)," of ",str(len(self.obj2term))," iterations\t",str(self.count)," MICA calculations\nprojected runtime:\t",str(((float(len(self.obj2term))/count2)*(time.time()-start))+1)," seconds\n")))
        for x in sorted(resultsDict,key=lambda entry:resultsDict[entry],reverse=True):
            if count>=length:
                break
            returnDict.update({x:resultsDict[x]})
            count+=1
        self.logger.debug("".join(("\nFinished!\t\t\t",str(self.count)," MICA calculations\nactual runtime:\t\t",str(time.time()-start)," seconds")))
        return returnDict
