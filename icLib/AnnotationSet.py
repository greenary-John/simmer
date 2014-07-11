import Ontology
import AnnotatedObject
import Annotation
import types

#current setup requires ont & con manager to be called before this file to work
#this means that in simmer.py, it is imperative to call ontman before annman

class AnnotationSet:
    def __init__(self,name,ontMan,simConPar):
        self.name=name
        self.annotsByID={}
        self.annotsByObj={}
        self.ontology=ontMan.getOntology(simConPar.getConfigObj(name)["ontology"])
        #ontman required to access list of ontologies in addAnnotation
        
    def addAnnotation(self,details):
        #details parameter will be a dictionary of additional values
        #these values may include evCode, J reference, etc.
        #structure: {"evCode":blah,"JRef":bloop,"InfoVar":beep,...}
        annObj=AnnotatedObject.AnnotatedObject.getAnnotatedObj(details["annID"])
        ontTerm=self.ontology.getTerm(details["termID"])
        self.annotsByID[ontTerm]=Annotation.Annotation(self.ontology,details)
        self.annotsByObj[annObj]=Annotation.Annotation(self.ontology,details)

    def getAnnotsByObject(self,obj=None):
        if obj==None:
            return self.annotsByObj
        if type(obj)==types.StringType:
            try:
                return self.annotsByObj[AnnotatedObject.AnnotatedObject.getAnnotatedObj(obj)]
            except KeyError:
                print "No annotations for requested object."
                return None
        else:
            try:
                return self.annotsByObj[obj]
            except KeyError:
                print "No annotations for requested object."
                return None

    def getAnnotsByTerm(self,term=None):
        if term==None:
            return self.annotsByID
        if type(term)==types.StringType:
            try:
                return self.annotsByID[self.ontology.getTerm(term)]
            except KeyError:
                print "No annotations for requested object."
                return None 
        else:
            try:
                return self.annotsByID[term]
            except KeyError:
                print "No annotations for requested object."
                return None
        
