'''Ontology Manager
The OntologyManager class creates an object that utilizes a ConfigManager
object to load ontologies. Additionally this class pre-computes forward
and reverse closures and stores this infomation, along with ontologies,
within the object.

Author: Patrick Osterhaus   s-osterh
'''
import Ontology
import DAG

class OntologyManager(object):

    def __init__(self,conMan):
        self.ontDetails={}
        self.onts={}
        for sec in conMan.sectionsWith("type","ontology"):
            self.ontDetails[sec]=conMan.getConfigObj(sec)
        for det in self.ontDetails:
            self.onts[det]=Ontology.load(self.ontDetails[det]["filename"],False)
        for ont in self.onts:
            self.onts[ont].closure=DAG.Closure().go(self.onts[ont])
            self.onts[ont].reverseClosure=DAG.Closure().go(self.onts[ont],None,True)

    def getOntology(self,name=None):
        if name in self.onts:
            return self.onts[name]
        else:
            names=[]
            for namespace in self.onts:
                names.append(namespace)
            return names
