import Ontology

class Ontology_Manager(object):

    def __init__(self):
        pass

    def ontsload(self,filedescripts):
        #filedescripts formatted as: [type_of_ont,filename_of_ont]
        onts=[]
        types=[]
        for filename in filedescripts:
            onts.append(Ontology.load(filename[1],True))
            types.append(filename[0])
        return [types,onts]
    
