import types

import Ontology
import AnnotatedObject
import Annotation
import Logger

#current setup requires ont & con manager to be called before this file to work
#this means that in simmer.py, it is imperative to call ontman before annman

class AnnotationSet:
    def __init__(self,name,ontMan,simConPar):
        self.name=name
        self.annots=set([])
        self.annotsByID={}
        self.annotsByObj={}
        self.ontology=ontMan.getOntology(simConPar.getConfigObj(name)["ontology"])
        self.ontMan=ontMan
        self.simConPar=simConPar
        self.logger=Logger.Logger()
        #ontman required to access list of ontologies in addAnnotation
        
    def addAnnotation(self,details):
        #details parameter will be a dictionary of additional values
        #these values may include evCode, J reference, etc.
        #structure: {"evCode":blah,"JRef":bloop,"InfoVar":beep,...}
        annObj=AnnotatedObject.AnnotatedObject.getAnnotatedObj(details["annID"])
        a=Annotation.Annotation(self.ontology,details)
        ontTerm=self.ontology.getTerm(details["termID"])
        for x in self.ontology.reverseClosure[ontTerm]:
            self.annotsByID.setdefault(x,set([])).add(a)
        self.annotsByObj.setdefault(annObj,set([])).add(a)
        self.annots.add(a)

    def getAnnots(self):
        return self.annots

    def getAnnotatedObjects(self):
        return self.annotsByObj.keys()

    def getAnnotatedTerms(self):
        return self.annotsByID.keys()

    def getAnnotsByObject(self,obj=None):
        if obj==None:
            return self.annotsByObj
        if type(obj)==types.StringType:
            try:
                return self.annotsByObj[AnnotatedObject.AnnotatedObject.getAnnotatedObj(obj)]
            except KeyError:
                self.logger.info("".join(("\nNo annotations for requested object:",str(obj))))
                return None
        else:
            try:
                return self.annotsByObj[obj]
            except KeyError:
                self.logger.info("".join(("\nNo annotations for requested object:",str(obj))))
                return None

    def getAnnotsByTerm(self,term=None):
        if term==None:
            return self.annotsByID
        if type(term)==types.StringType:
            try:
                return self.annotsByID[self.ontology.getTerm(term)]
            except KeyError:
                self.logger.info("".join(("\nNo annotations for requested term:",str(term))))
                return None 
        else:
            try:
                return self.annotsByID[term]
            except KeyError:
                self.logger.info("".join(("\nNo annotations for requested term:",str(term))))
                return None

    def evidenceFilter(self,evCodes):
        annset=AnnotationSet(self.name,self.ontMan,self.simConPar)
        filtered={}
        for item in self.annotsByID:
            temp=[]
            for ann in self.annotsByID[item]:
                if not ann.details["EvidenceCode"] in evCodes:
                    temp.append(ann)
            filtered.update({item:temp})
        annset.annotsByID=filtered
        
        filtered={}
        for item in self.annotsByObj:
            temp=[]
            for ann in self.annotsByObj[item]:
                if not ann.details["EvidenceCode"] in evCodes:
                    temp.append(ann)
            filtered.update({item:temp})
        annset.annotsByObj=filtered
        
        return annset
        
