'''File, written by Pat Osterhaus, contains significant portions (most) of
code written by Daniel Galvez'''

import Ontology
import sets

class OntTerm(Ontology.OboTerm):

    def __init__(self,id,name,ont):
        #for now, id is included. it is hoped that since id and name are linked
        #this could take simply name yet call OboTerm with id and name due to the linkage
       super(OntTerm,self).__init__(id, name, ont)

       '''
       self.ancestors=sets.Set()
       self.descendants=sets.Set()
       self.descendantsIC=0
       self.annotationsIC=None
       self.annotation_count=0
       self.annotatedObjects={}
       self.wang_s={}
       self.wang_sv=0
       self.ancestorGraph=""
       '''


    '''
    def getIC(self,typ):
        if typ=="annotations":
            return self.annotationsIC
        else:
            return self.descendantsIC
    def __str__(self):
        return self.id
    '''
