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
        for evCode in evCodes:
            try:
                self.annset.annotations["ID"]={key:value for key,value in self.annset.annotations["ID"].items() if value[1]["EvidenceCode"]!=evCode}
                self.annset.annotations["Obj"]={key:value for key,value in self.annset.annotations["Obj"].items() if value[1]["EvidenceCode"]!=evCode}
            except KeyError:
                self.annset.annotations["ID"]={key:value for key,value in self.annset.annotations["ID"].items() if value[1]["Evidence"]!=evCode}
                self.annset.annotations["Obj"]={key:value for key,value in self.annset.annotations["Obj"].items() if value[1]["Evidence"]!=evCode}

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
