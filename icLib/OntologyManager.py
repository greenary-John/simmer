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
        try:
            return self.onts[name]
        except KeyError:
            names=[]
            for namespace in self.onts:
                names.append(namespace)
            return names
