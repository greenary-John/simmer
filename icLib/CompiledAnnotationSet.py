import math

class CompiledAnnotationSet:

    def __init__(self,AnnSet,evCodes,ontman):
        self.ontman=ontman
        self.annset=AnnSet
        self.evCodes=evCodes if isinstance(evCodes,list) else [evCodes]
        self.AnnotationSetEvidenceFilter(self.evCodes)
        self.term2obj()
        self.obj2term()
        #self.term2IC()

    def AnnotationSetEvidenceFilter(self,evCodes):
        #input of annotation set and desired evidence codes to REMOVE
        filtered={}
        for ann in self.annset.annotsByID:
            #print self.annset.annotsByID[ann].details["EvidenceCode"]
            #print evCodes
            if not self.annset.annotsByID[ann].details["EvidenceCode"] in evCodes:
                filtered.update({ann:self.annset.annotsByID[ann]})
        self.annset.annotsByID=filtered
        filtered={}
        for ann in self.annset.annotsByObj:
            #print self.annset.annotsByObj[ann].details["EvidenceCode"]
            #print evCodes
            if not self.annset.annotsByObj[ann].details["EvidenceCode"] in evCodes:
                filtered.update({ann:self.annset.annotsByObj[ann]})
        self.annset.annotsByObj=filtered

    def term2obj(self):
        self.term2obj={}
        for x in self.annset.annotsByID:
            if not self.term2obj.has_key(x):
                for y in self.annset.ontology.closure[x]:
                    try:
                        self.term2obj.update({x:self.annset.annotsByID[y].annObj})
                    except KeyError:
                        continue
            else:
                for y in self.annset.ontolgoy.closure[x]:
                    try:
                        self.term2obj[x]=[self.term2obj[x],self.annset.annotsByID[y].annObj]
                    except KeyError:
                        continue

    def obj2term(self):
        self.obj2term={}
        for x in self.annset.annotsByObj:
            if not self.obj2term.has_key(x):
                self.obj2term.update({x:self.annset.ontology.closure[self.annset.annotsByObj[x].ontTerm]})
            else:
                self.obj2term[x]=[self.obj2term[x],self.annset.ontology.closure[self.annset.annotsByObj[x].ontTerm]]

    def term2IC(self):
        self.term2IC={}
        sum=0
        counts={}
        print type(self.term2obj)
        for x in self.term2obj:
            print self.term2obj[x]
            counts.update({x:len(self.term2obj[x])})
            sum+=len(self.term2obj[x])
        for x in self.term2obj:
            self.term2IC.update({x:math.log(float(counts[x])/sum)})

def flatten(lst):
	return sum((flatten(x) if isinstance(x, list) else [x]for x in lst))
