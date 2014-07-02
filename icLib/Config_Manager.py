import ConfigParser
import Ontology_Manager
import Annotation_Manager
import optparse

class Config_Manager(object):

    #initializes Config_Manager class
    def __init__(self):
        self.cp=ConfigParser.SafeConfigParser()
        self.op=optionParser()
        self.ontman=Ontology_Manager.Ontology_Manager()
        self.annman=Annotation_Manager.Annotation_Manager()
        #this should handle only config files and command line options
        #inheritance backwards; ann and ont managers should call con man
        self.cp.read(self.op.opts.configFile)

    #get methods for values contained in the DEFAULT section; maybe not vital
    def getDataDir(self):
        return self.cp.get('DEFAULT','datadir')
    def getOntDir(self):
        return self.cp.get('DEFAULT','ontdir')
    def getAnnDir(self):
        return self.cp.get('DEFAULT','anndir')
    
    def getOntologies(self):
        ontfiledescripts=[]
        #parses information held in sections, including header details
        for s in self.cp.sections():
            if "Ontology" in s:
                if "GO" in s:
                    ontfiledescripts.append(["GO",self.cp.get(s,'filename')])
                if "MP" in s:
                    ontfiledescripts.append(["MP",self.cp.get(s,'filename')])
        #loads and returns ontologies associated with config information
        return self.ontman.ontsload(ontfiledescripts)
    
    def getAnnotations(self):
        annfiledescripts=[]
        #parses information held in AnnotData sections
        for s in self.cp.sections():
            if "AnnotData" in s:
                 annfiledescripts.append([self.cp.get(s,'ontology'),self.cp.get(s,'filename'),self.cp.get(s,'obtype')])
        #loads and returns annotations associated with config information
        return self.annman.annsload(annfiledescripts)

class optionParser(object):
    def __init__(self):
        parser=optparse.OptionParser()
        parser.add_option("-c","--config",dest="configFile",default="C:\Users\s-osterh\Desktop\simmer\config.cfg",help="Specify config file location. (default=%default)")
        #parser.add_option("-o","--ontology",dest="ontoChoice",default="0",help="Which ontology? 0 for GO, anything else for MP. (default=%default)")
        #parser.add_option("-e","--evidence",dest="evidenceCodeStrings",default="None",help="What evidence codes would you like to remove? (Separate evidence codes by commas. Spaces can be used. Specify 'None' to not remove evidence codes. See http://www.geneontology.org/GO.evidence.shtml)(default=%default)")
        #parser.add_option("-f","--file",dest="fileName",default="data\gene_association.mgi",help="Which gene or phenotype file would you like to use as input?(default=%default)")
        #parser.add_option("-d","--diseasefile",dest="diseaseFile",default="data\Geno_11_OMIM.txt",help="For use with MP terms. Specify which file, containing OMIM data, is desired for input.(default=%default)")
        #parser.add_option("-l","--length",type="int",dest="length",default=25,help="Select how many results (matches) are desired. Values will be rounded down to nearest integer of lesser value.(default=%default)")
        #above commented options will probably have their place in final iteration
        (options,args)=parser.parse_args()
        self.opts=options
        self.ars=args
    
                
    
