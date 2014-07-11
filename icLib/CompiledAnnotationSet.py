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
        print "annCard calculated!"
        self.term2IC={}
        for x in self.term2obj:
            try:
                self.term2IC.update({x:-1.0*math.log(float(len(self.term2obj[x]))/self.annotationCardinality)})
            except ValueError:
                self.term2IC.update({x:None})

def flatten(lst):
	return sum((flatten(x) if isinstance(x, list) else [x]for x in lst),[])
