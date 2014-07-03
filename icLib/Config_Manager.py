import ConfigParser
#import Ontology_Manager
#import Annotation_Manager
import optparse

class optionParser(object):
    def __init__(self):
        parser=optparse.OptionParser()
        parser.add_option("-c","--config",dest="configFile",default="C:\Users\s-osterh\Desktop\simmer\config.cfg",help="Specify config file location. (default=%default)")
        parser.add_option("-D","--Define",action="append",dest="defintions",default=None,help="Define new sections and variables for config file. (default=%default)")
        #parser.add_option("-o","--ontology",dest="ontoChoice",default="0",help="Which ontology? 0 for GO, anything else for MP. (default=%default)")
        #parser.add_option("-e","--evidence",dest="evidenceCodeStrings",default="None",help="What evidence codes would you like to remove? (Separate evidence codes by commas. Spaces can be used. Specify 'None' to not remove evidence codes. See http://www.geneontology.org/GO.evidence.shtml)(default=%default)")
        #parser.add_option("-f","--file",dest="fileName",default="data\gene_association.mgi",help="Which gene or phenotype file would you like to use as input?(default=%default)")
        #parser.add_option("-d","--diseasefile",dest="diseaseFile",default="data\Geno_11_OMIM.txt",help="For use with MP terms. Specify which file, containing OMIM data, is desired for input.(default=%default)")
        #parser.add_option("-l","--length",type="int",dest="length",default=25,help="Select how many results (matches) are desired. Values will be rounded down to nearest integer of lesser value.(default=%default)")
        #above commented options will probably have their place in final iteration
        (options,args)=parser.parse_args()
        self.opts=options
        self.ars=args

class Config_Manager(object):
    def __init__(self):
        self.cp=simmerConfigParser()
        self.op=optionParser()
        print "\n**",self.op.opts.defintions,"**\n"
        '''
        open(self.op.opts.configFile,'r+')
        defs=[]
        for de in self.op.opts.defintions:
            temp=de.split(".")
            for te in temp:
                defs.append(te.split("=")
        '''
        self.cp.read(self.op.opts.configFile)
    #methods called with simmerConfigParser class    

    def sectionsWith(self,name,value=None):
        return self.cp.sectionsWith(name,value)
    def getConfigObj(self,section=None):
        return self.cp.getConfigObj(section)
    def getDataDir(self):
        return self.cp.get('DEFAULT','datadir')
    def getOntDir(self):
        return self.cp.get('DEFAULT','ontdir')
    def getAnnDir(self):
        return self.cp.get('DEFAULT','anndir')

class simmerConfigParser(ConfigParser.SafeConfigParser):
    def sectionsWith(self,name,value=None):
        rlist=[]
        for s in self.sections():
            for (var,val) in self.items(s):
                if var==name and value==None or val==value:
                    rlist.append(s)
        return rlist
    def getConfigObj(self,section=None):
        sectionInfo={}
        for s in self.sections():
            sectInfo={}
            for (var,val) in self.items(s):
                if (var,val) not in self.items("DEFAULT"):
                    sectInfo.update({var:val})
            if section==s:
                return {s:sectInfo}
            sectionInfo.update({s:sectInfo})
        return sectionInfo

    #get methods for values contained in the DEFAULT section; maybe not vital
    def getDataDir(self):
        return self.get('DEFAULT','datadir')
    def getOntDir(self):
        return self.get('DEFAULT','ontdir')
    def getAnnDir(self):
        return self.get('DEFAULT','anndir')

    '''
    #getOntologies and getAnnotations will need to be moved to the respective manager modules
    def getOntologies(self):
        ontfiledescripts=[]
        #parses information held in sections, including header details
        for s in self.sections():
            if "Ontology" in s:
                if "GO" in s:
                    ontfiledescripts.append(["GO",self.get(s,'filename')])
                if "MP" in s:
                    ontfiledescripts.append(["MP",self.get(s,'filename')])
        #loads and returns ontologies associated with config information
        return self.ontman.ontsload(ontfiledescripts)
    
    def getAnnotations(self):
        annfiledescripts=[]
        #parses information held in AnnotData sections
        for s in self.cp.sections():
            if "AnnotData" in s:
                 annfiledescripts.append([self.get(s,'ontology'),self.get(s,'filename'),self.get(s,'obtype')])
        #loads and returns annotations associated with config information
        return self.annman.annsload(annfiledescripts)
    '''
def __test__():
    simmercon=Config_Manager()
    print "Data Dir:\t",simmercon.getDataDir()
    print "Ont Dir:\t",simmercon.getOntDir()
    print "Ann Dir:\t",simmercon.getAnnDir()
    print "\nSections with 'type' of 'ontology'\n",simmercon.sectionsWith("type","ontology")
    print "\ngetConfigObj(\"GO\")\n",simmercon.getConfigObj("GO")
    print "\ngetConfigObj()\n",simmercon.getConfigObj()
    
if __name__=="__main__":
    __test__()
