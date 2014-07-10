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
        lst=["ID","Obj"]
        for typ in lst:
            filtered={}
            for ann in self.annset.annotations[typ]:
                if not self.annset.annotations[typ][ann][1]["EvidenceCode"] in evCodes:
                    filtered.update({ann:self.annset.annotations[typ][ann]})
            self.annset.annotations[typ]=filtered

    def term2obj(self):
        self.term2obj={}
        for x in self.annset.annotations["ID"]:
            if not self.term2obj.has_key(x):
                for y in self.annset.ontology.closure[x]:
                    try:
                        self.term2obj.update({x:self.annset.annotations["ID"][y][0]})
                    except KeyError:
                        continue
            else:
                for y in self.annset.ontolgoy.closure[x]:
                    try:
                        self.term2obj[x]=[self.term2obj[x],self.annset.annotations["ID"][y][0]]
                    except KeyError:
                        continue

    def obj2term(self):
        self.obj2term={}
        for x in self.annset.annotations["Obj"]:
            if not self.obj2term.has_key(x):
                self.obj2term.update({x:self.annset.ontology.closure[self.annset.annotations["Obj"][x][0]]})
            else:
                self.obj2term[x]=[self.obj2term[x],self.annset.ontology.closure[self.annset.annotations["Obj"][x][0]]]
            for y in self.annset.annotations["Obj"][x]:
                y=y.__str__()

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
