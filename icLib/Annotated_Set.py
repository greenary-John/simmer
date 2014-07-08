import Ontology
import Annotated_Object
import Ontology_Manager

#current setup requires ontology manager to be called before this file to work
#this means that in simmer.py, it is imperative to call ontman before annman

class AnnotatedSet:
    def __init__(self,name,ontMan):
        self.name=name
        self.annotations={"ID":{},"Obj":{}}
        self.ontman=ontMan
        #ontologyManager required to access list of ontologies in addAnnotation
        
    def addAnnotation(self,annID,ontID,termID,details):
        #details parameter will be a dictionary of additional values
        #these values may include evCode, J reference, etc.
        #structure: {"evCode":blah,"JRef":bloop,"InfoVar":beep,...}
        annObj=AnnotatedObject.getAnnotatedObj(annID)
        ontTerm=self.ontman.onts[ontID].getTerm(termID)
        self.annotations["ID"][ontTerm]=[annObj,details]
        self.annotations["Obj"][annObj]=[ontTerm,details]

    def getAnnotsByObject(self,obj):
        try:
            return self.annotations["Obj"][obj]
        except KeyError:
            try:
                return self.annotations["Obj"][AnnotatedObject.getAnnotatedObj(obj)]
            except KeyError:
                print "No annotations for requested object."
                return None
    def getAnnotsByTerm(self,term):
        try:
            return self.annotations["ID"][term]
        except KeyError:
            for ont in self.ontman.onts:
                try:
                    return  self.annotations["ID"][ont.getTerm(term)]
                except KeyError:
                    continue
            print "No annotations for requested object."
            return None
