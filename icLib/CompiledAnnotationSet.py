import math
import time

import AnnotatedObject
import Logger
import Ontology

class CompiledAnnotationSet:

    def __init__(self,AnnSet,evCodes,ontman):
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
                        for z in self.annset.getAnnotsByTerm(y):
                            try:
                                temp.add(z.annObj)
                            except KeyError:
                                continue
                    except TypeError:
                        continue
                self.term2obj[x]=temp

    def Compute_obj2term(self):
        self.obj2term={}
        for x in self.annset.getAnnotatedObjects():
            temp=[]
            for y in self.annset.getAnnotsByObject(x):
                temp.append(y.ontTerm)
            self.obj2term.setdefault(x,set([])).update(temp)

    def Compute_term2IC(self):
        self.term2IC={}
        for x in self.term2obj:
            if len(self.term2obj[x])==0:
                self.term2IC[x]=None
            else:
                self.term2IC[x]=math.log(len(self.term2obj[self.annset.ontology.getRoots(x.namespace)[0]])/float(len(self.term2obj[x])))
                
    def Compute_pair2MICA(self):
        self.pair2MICA={}
        for x in self.term2IC:
            for y in self.term2IC:
                if self.pair2MICA.has_key((y,x)):
                    continue
                else:                    
                    self.pair2MICA.update[(x,y)]=self.getMICAscore(x,y)
                    
    def maxIC(self,lst):
        return max([self.term2IC.get(x,0)for x in lst])if len(lst)>0 else 0.0

    def getMICAscore(self,termA,termB,namespace):
        if termA.namespace!=namespace or termB.namespace!=namespace:
            return
        self.MICAcount+=1
        return self.maxIC(self.annset.ontology.reverseClosure[termA]&self.annset.ontology.reverseClosure[termB])

    def rowMICA(self,termA,objB,namespace):
        #term to obj comparison
        ret=max([self.getMICAscore(termA,y,namespace)for y in self.obj2term[objB]])
        if ret==None:
            return
        else:
            return ret

    def objCompare(self,objA,objB,namespace):
        #obj to obj comparison
        lst=[self.rowMICA(y,objB,namespace)for y in self.obj2term[objA]]
        #return float(sum(lst))/len(lst) if len(lst)>0 else 0
        if len([x for x in lst if x!=None])>0:
            return float(sum([x for x in lst if x!=None]))/len([x for x in lst if x!=None])
        else:
            return 0.0

    def listCompare(self,listA,objB,namespace):
        #list to obj comparison
        lst=[self.rowMICA(y,objB,namespace)for y in listA]
        if len([x for x in lst if x!=None])>0:
            return float(sum([x for x in lst if x!=None]))/len([x for x in lst if x!=None])
        else:
            return 0.0
        
    def resnikBMA(self,qType,query,namespace,length):
        #BMA approach; obj to list of objs comparison
        #eventually normalize for the maximum (identity) score to equal 1
        start=time.time()
        self.MICAcount=0
        resultsDict={}
        returnDict={}
        count=0
        if qType=="object":
            for x in self.obj2term:
                resultsDict[x]=self.objCompare(query,x,namespace)
        else:
            for x in self.obj2term:
                resultsDict[x]=self.listCompare(query,x,namespace)
        for x in sorted(resultsDict,key=lambda entry:resultsDict[entry],reverse=True):
            if count>=length:
                break
            returnDict[x]=resultsDict[x]
            count+=1
        self.logger.debug("".join(("\nFinished!\tresnikBMA\t",str(self.MICAcount)," MICA calculations\nactual runtime:\t\t",str(time.time()-start)," seconds\n")))
        return returnDict

    def jaccardExt(self,qType,que,namespace,length):
        start=time.time()
        resultsDict={}
        returnDict={}
        count=0
        query=set([])
        if qType=="object":
            for x in self.obj2term[que]:
                if x.namespace==namespace:
                    query|=self.annset.ontology.reverseClosure[x]
        else:
            for x in que:
                if x.namespace==namespace:
                    query|=self.annset.ontology.reverseClosure[x]
        for x in self.annset.getAnnotatedObjects():
            test=set([])
            for y in self.obj2term[x]:
                if y.namespace==namespace:
                    test|=self.annset.ontology.reverseClosure[y]
            if len(query|test)==0:
                resultsDict[x]=0.0
            else:
                resultsDict[x]=float(len(query&test))/len(query|test)
        for x in sorted(resultsDict,key=lambda entry:resultsDict[entry],reverse=True):
            if count>=length:
                break
            returnDict[x]=resultsDict[x]
            count+=1
        self.logger.debug("".join(("\nFinished!\tjaccardExt\t",str(time.time()-start)," seconds\n")))
        return returnDict

    def gicExt(self,qType,que,namespace,length):
        start=time.time()
        resultsDict={}
        returnDict={}
        count=0
        query=set([])
        if qType=="object":
            for x in self.obj2term[que]:
                if x.namespace==namespace:
                    query|=self.annset.ontology.reverseClosure[x]
        else:
            for x in que:
                if x.namespace==namespace:
                    query|=self.annset.ontology.reverseClosure[x]
        for x in self.annset.getAnnotatedObjects():
            test=set([])
            for y in self.obj2term[x]:
                if y.namespace==namespace:
                    test|=self.annset.ontology.reverseClosure[y]
            if sum([self.term2IC.get(d,0)for d in query|test])==0:
                resultsDict[x]=0.0
            else:
                resultsDict[x]=sum([self.term2IC.get(z,0)for z in query&test])/sum([self.term2IC.get(d,0)for d in query|test])
        for x in sorted(resultsDict,key=lambda entry:resultsDict[entry],reverse=True):
            if count>=length:
                break
            returnDict[x]=resultsDict[x]
            count+=1
        self.logger.debug("".join(("\nFinished!\tgicExt\t",str(time.time()-start)," seconds\n")))
        return returnDict
