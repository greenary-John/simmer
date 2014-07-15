import math

class CompiledAnnotationSet:

    def __init__(self,AnnSet,evCodes,ontman):
        self.ontman=ontman
        self.annset=AnnSet
        self.evCodes=evCodes if isinstance(evCodes,list) else [evCodes]
        self.AnnotationSetEvidenceFilter(self.evCodes)
        self.Compute_term2obj()
        self.Compute_obj2term()
        self.Compute_term2IC()
        self.count=0
        #print "\nlen(term2IC)\n",len(self.term2IC)
        #self.Compute_pair2MICA()

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

    def Compute_term2obj(self):
        self.term2obj={}
        for x in self.annset.getAnnotsByTerm():
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
        for x in self.annset.getAnnotsByObject():
            temp=set([])
            for y in self.annset.annotsByObj[x]:
                temp.union(self.annset.ontology.reverseClosure[y.ontTerm])
            self.obj2term.setdefault(x,set([])).union(temp)

    def Compute_term2IC(self):
        self.annotationCardinality=len(flatten(self.annset.getAnnotsByObject().values()))
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
            for y in set.union(*self.obj2term[objB]):
                if self.MICA(termA,y)>maximum:
                    maximum=self.MICA(termA,y)
                    count+=1
        return maximum

    def objCompare(self,objA,objB):
        #obj to obj comparison
        lst=[]
        count=0
        if len(self.obj2term[objA])>0:
            for y in set.union(*self.obj2term[objA]):
                lst.append(self.rowMICA(y,objB))
                count+=1
        return sum(lst)/len(lst)

    def resnikResults(self,objA,length):
        #BMA approach; obj to list of objs comparison
        resultsDict={}
        returnDict={}
        count2=0
        count=0
        for x in self.obj2term:
            resultsDict.update({x:self.objCompare(objA,x)})
            count+=1
        for x in sorted(resultsDict):
            if count2>=length:
                break
            returnDict.update({x:resultsDict[x]})
            count2+=1
        return returnDict

def flatten(lst):
	return sum((flatten(x) if isinstance(x, list) else [x]for x in lst),[])
