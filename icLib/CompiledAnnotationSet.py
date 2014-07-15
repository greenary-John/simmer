import math

class CompiledAnnotationSet:

    def __init__(self,AnnSet,evCodes,ontman):
        self.ontman=ontman
        self.annset=AnnSet
        self.evCodes=evCodes if isinstance(evCodes,list) else [evCodes]
        self.AnnotationSetEvidenceFilter(self.evCodes)
        self.term2obj()
        self.obj2term()
        self.term2IC()
        #print "\nlen(term2IC)\n",len(self.term2IC)
        #self.pair2MICA()

    def AnnotationSetEvidenceFilter(self,evCodes):
        #input of annotation set and desired evidence codes to REMOVE
        filtered={}
        for item in self.annset.annotsByID:
            temp=[]
            for ann in self.annset.annotsByID[item]:
                if not ann.details["EvidenceCode"] in evCodes:
                    temp.append(ann)
            filtered.update({item:temp})
        self.annset.annotsByID=filtered
        filtered={}
        for item in self.annset.annotsByObj:
            temp=[]
            for ann in self.annset.annotsByObj[item]:
                if not ann.details["EvidenceCode"] in evCodes:
                    temp.append(ann)
            filtered.update({item:temp})
        self.annset.annotsByObj=filtered

    def term2obj(self):
        self.term2obj={}
        for x in self.annset.getAnnotsByTerm():
            if not self.term2obj.has_key(x):
                temp=[]
                for y in self.annset.ontology.closure[x]:
                    try:
                        for z in self.annset.annotsByID[y]:
                            try:
                                temp.append(z.annObj)
                            except KeyError:
                                continue
                    except KeyError:
                        continue
                self.term2obj.update({x:temp})
            else:
                temp=[]
                for y in self.annset.ontology.closure[x]:
                    try:
                        for z in self.annset.annotsByID[y]:
                            try:
                                temp.append(z.annObj)
                            except KeyError:
                                continue
                    except KeyError:
                        continue
                self.term2obj.update({x:temp})
            

    def obj2term(self):
        self.obj2term={}
        for x in self.annset.getAnnotsByObject():
            temp=[]
            for y in self.annset.annotsByObj[x]:
                temp.append(self.annset.ontology.closure[y.ontTerm])
            if not self.obj2term.has_key(x):
                self.obj2term.update({x:temp})
            else:
                self.obj2term[x]=[self.obj2term[x],temp]
        for x in self.obj2term:
            flatten(self.obj2term[x])

    def term2IC(self):
        self.annotationCardinality=len(flatten(self.annset.getAnnotsByObject().values()))
        self.term2IC={}
        for x in self.term2obj:
            try:
                self.term2IC.update({x:math.log(self.annotationCardinality/float(len(self.term2obj[x])))})
            except ZeroDivisionError:
                self.term2IC.update({x:None})
                
    def pair2MICA(self):
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
        return self.maxIC(self.annset.ontology.reverseClosure[termA]&self.annset.ontology.reverseClosure[termB])

    def rowMICA(self,termA,objB):
        #term to obj comparison
        maximum=0
        for y in set.union(*self.obj2term[objB]):
            if self.MICA(termA,y)>maximum:
                maximum=self.MICA(termA,y)
        return maximum

    def objCompare(self,objA,objB):
        #obj to obj comparison
        lst=[]
        for y in set.union(*self.obj2term[objA]):
            lst.append(self.rowMICA(y,objB))
        return sum(lst)/len(lst)

    def resnikResults(self,objA,length):
        #BMA approach; obj to list of objs comparison
        resultsDict={}
        returnDict={}
        count=0
        for x in self.obj2term:
            resultsDict.update({x:self.objCompare(objA,x)})
        for x in sorted(resultsDict):
            if count>=length:
                break
            returnDict.update({x:resultsDict[x]})
            count+=1
        return sorted(returnDict)
        
            
def flatten(lst):
    return sum((flatten(x) if isinstance(x, list) else [x]for x in lst),[])

