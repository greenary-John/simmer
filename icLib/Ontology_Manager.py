import Ontology

class Ontology_Manager(object):

    def __init__(self):
        pass

    def ontload(self,filedescript):
        return Ontology.load(filedescript[1])

    def ontsload(self,filedescripts):
        onts=[]
        for filename in filedescripts:
            onts.append(Ontology.load(filename[1]))
        return onts
    
