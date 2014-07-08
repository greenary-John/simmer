import Ontology

class Ontology_Manager(object):

    def __init__(self,conMan):
        self.ontObjs={}
        self.onts={}
        #print conMan.getConfigObj().keys()
        for sec in conMan.sectionsWith("type","ontology"):
            self.ontObjs[sec]=conMan.getConfigObj(sec)
        for obj in self.ontObjs:
            self.onts[obj]=Ontology.load(self.ontObjs[obj]["filename"],False)
