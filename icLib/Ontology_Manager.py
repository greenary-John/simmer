import Ontology

class Ontology_Manager(object):

    def __init__(self,conMan):
        self.ontObjs={}
        self.onts={}
        for sec in conMan.sectionsWith("type","ontology"):
            self.ontObjs[sec]=conMan.getConfigObj(sec)[sec]
        for obj in self.ontObjs:
            self.onts[obj]=Ontology.load(self.ontObjs[obj]["filename"],True)

    def ontsload(self,filedescripts):
        #filedescripts formatted as: [type_of_ont,filename_of_ont]
        onts=[]
        types=[]
        for filename in filedescripts:
            onts.append(Ontology.load(filename[1],True))
            types.append(filename[0])
        return [types,onts]
    
