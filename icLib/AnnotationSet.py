import Ontology
import AnnotatedObject
import types

#current setup requires ont & con manager to be called before this file to work
#this means that in simmer.py, it is imperative to call ontman before annman

class AnnotationSet:
    def __init__(self,name,ontMan,simConPar):
        self.name=name
        self.annotations={"ID":{},"Obj":{}}
        self.ontman=ontMan
        self.scp=simConPar
        #ontman required to access list of ontologies in addAnnotation
        #scp required to check format of annotations
        
    def addAnnotation(self,ontID,details):
        #details parameter will be a dictionary of additional values
        #these values may include evCode, J reference, etc.
        #structure: {"evCode":blah,"JRef":bloop,"InfoVar":beep,...}
        self.ontology=self.ontman.onts[ontID]
        annObj=AnnotatedObject.AnnotatedObject.getAnnotatedObj(details["annID"])
        ontTerm=self.ontology.getTerm(details["termID"])
        self.annotations["ID"][ontTerm]=[annObj,details]
        self.annotations["Obj"][annObj]=[ontTerm,details]

    def getAnnotsByObject(self,obj=None):
        if obj==None:
            return self.annotations["Obj"]
        if type(obj)==types.StringType:
            try:
                return self.annotations["Obj"][AnnotatedObject.AnnotatedObject.getAnnotatedObj(obj)]
            except KeyError:
                print "No annotations for requested object."
                return None
        else:
            try:
                return self.annotations["Obj"][obj]
            except KeyError:
                print "No annotations for requested object."
                return None

    def getAnnotsByTerm(self,term=None):
        if term==None:
            return self.annotations["ID"]
        if type(term)==types.StringType:
            try:
                for ont in self.ontman.onts:
                    try:
                        return self.annotations["ID"][self.ontman.onts[ont].getTerm(term)]
                    except KeyError:
                        continue
                return self.annotations["ID"][None]
            except KeyError:
                print "No annotations for requested object."
                return None 
        else:
            try:
                return self.annotations["ID"][term]
            except KeyError:
                print "No annotations for requested object."
                return None
        
