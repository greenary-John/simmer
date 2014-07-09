import Ontology
import Annotated_Object
#two imports below possibly unneccesary?
import Ontology_Manager
import Config_Manager

#current setup requires ont & con manager to be called before this file to work
#this means that in simmer.py, it is imperative to call ontman before annman

class AnnotatedSet:
    def __init__(self,name,ontMan,simConPar):
        self.name=name
        self.annotations={"ID":{},"Obj":{}}
        self.ontman=ontMan
        self.scp=simConPar
        #ontman required to access list of ontologies in addAnnotation
        #scp required to check format of annotations
        
    def addAnnotation(self,annID,ontID,termID,details):
        #details parameter will be a dictionary of additional values
        #these values may include evCode, J reference, etc.
        #structure: {"evCode":blah,"JRef":bloop,"InfoVar":beep,...}
        self.ontology=self.ontman.onts[ontID]
        annObj=Annotated_Object.AnnotatedObject.getAnnotatedObj(annID)
        ontTerm=self.ontology.getTerm(termID)
        self.annotations["ID"][ontTerm]=[annObj,details]
        self.annotations["Obj"][annObj]=[ontTerm,details]

    def getAnnotsByObject(self,obj=None):
        #print self.annotations["Obj"].keys()
        if obj==None:
            return self.annotations["Obj"]
        try:
            return self.annotations["Obj"][obj]
        except KeyError:
            try:
                return self.annotations["Obj"][Annotated_Object.AnnotatedObject.getAnnotatedObj(obj)]
            except KeyError:
                print "No annotations for requested object."
                return None
    def getAnnotsByTerm(self,term=None):
        if term==None:
            return self.annotations["ID"]
        try:
            return self.annotations["ID"][term]
        except KeyError:
            for ont in self.ontman.onts:
                try:
                    return  self.annotations["ID"][self.ontman.onts[ont].getTerm(term)]
                except KeyError:
                    continue
            print "No annotations for requested object."
            return None
        
