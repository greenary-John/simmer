import Ontology

class Ontology_Manager(object):

    def __init__(self):
        pass

    def ontload(self,filedescript):
        return [filedescript[0],Ontology.load(filedescript[1])]

    def ontsload(self,filedescripts):
        onts=[]
        types=[]
        for filename in filedescripts:
            onts.append(Ontology.load(filename[1]))
            types.append(filename[0])
        return [types,onts]
    
