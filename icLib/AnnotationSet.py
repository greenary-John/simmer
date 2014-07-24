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
        self.annots=[]
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
        if isinstance(details,Annotation.Annotation):
            a=details
        else:
            a=Annotation.Annotation(self.ontology,details)
        for x in self.ontology.reverseClosure[a.ontTerm]:
            self.annotsByID.setdefault(x,set([])).add(a)
        self.annotsByObj.setdefault(a.annObj,set([])).add(a)
        self.annots.append(a)

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
            obj=AnnotatedObject.AnnotatedObject.getAnnotatedObj(obj)
        if obj==None:
            self.logger.info("".join(("\nNo annotations for requested object:",str(obj))))
        return self.annotsByObj.get(obj,[])

    def getAnnotsByTerm(self,term=None):
        if term==None:
            return self.annotsByID
        if type(term)==types.StringType:
            term=self.ontology.getTerm(term)
        return self.annotsByID.get(term,[])
        #ret=self.annotsByID.get(term,[])
        #if ret==[]:
            #self.logger.info("".join(("\nNo annotations for requested term:",str(term))))
        #return ret

        #above four lines commented out to avoid logging unfound terms
        #logging slows down process considerably. replace return statement
        #with commented lines to log unfound terms

    def evidenceFilter(self,evCodes):
        annset=AnnotationSet(self.name,self.ontMan,self.simConPar)
        for a in self.annots:
            if not a.evCode in evCodes:
                annset.addAnnotation(a)
        return annset
        
