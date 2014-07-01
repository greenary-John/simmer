import ConfigParser
import Ontology_Manager
import Annotation_Manager

class Config_Manager(object):

    def __init__(self,cfg):
        self.cp=ConfigParser.SafeConfigParser()
        self.ontman=Ontology_Manager.Ontology_Manager()
        self.annman=Annotation_Manager.Annotation_Manager()
        self.cp.read(cfg)

    def getDataDir(self):
        return self.cp.get('DEFAULT','datadir')
    def getOntDir(self):
        return self.cp.get('DEFAULT','ontdir')
    def getAnnDir(self):
        return self.cp.get('DEFAULT','anndir')
    
    def getOntologies(self):
        ontfiledescripts=[]
        for s in self.cp.sections():
            if "Ontology" in s:
                if "GO" in s:
                    ontfiledescripts.append(["GO",self.cp.get(s,'filename')])
                if "MP" in s:
                    ontfiledescripts.append(["MP",self.cp.get(s,'filename')])
        return self.ontman.ontsload(ontfiledescripts)
    def getAnnotations(self):
        annfiledescripts=[]
        for s in self.cp.sections():
            if "AnnotData" in s:
                 annfiledescripts.append([self.cp.get(s,'ontology'),self.cp.get(s,'filename'),self.cp.get(s,'obtype')])
        return self.annman.annsload(annfiledescripts)
                
                
    
