import os
import ConfigParser
#import optparse

from icLib import Ontology
from icLib import DAG
from icLib import Config_Manager
from icLib import Extended_Closure

def main():
    conman=Config_Manager.Config_Manager()
    rclos=Extended_Closure.ReverseClosure()
    fclos=Extended_Closure.ForwardClosure()
    ontologies=conman.getOntologies()
    annotations=conman.getAnnotations()
    rclosure=rclos.multigo(ontologies[1])
    fclosure=fclos.multigo(ontologies[1])


    #above this comment is mostly algorithmic
    #below this comment is mostly printing to validate variables and output

    print "Data Dir:\t",conman.getDataDir()
    print "Ont Dir:\t",conman.getOntDir()
    print "Ann Dir:\t",conman.getAnnDir(),"\n"
    
    #formatted printing of ontology namespaces and annotation subsets, respectively
    for x in range(0,len(ontologies[1])):
        print ontologies[0][x],":\t",ontologies[1][x].getNamespaces() 
    print "\n"
    for x in range(0,len(annotations[1])):
        print annotations[0][x]," Preview:\t",annotations[1][x][0:2]
        print "\n"
    #annotations[0] holds list of annotation types (e.g., "GO" or "MP")
    #annotations[1] holds list of annotations, split by tabs such that a list is
    #analogous to a row in Excel and each element in the list is from a unique column




    
    #printing 10 terms each from rclosure and fclosure for testing
    print "rclosure subset"
    count=0
    while count<10:
        for x in rclosure:
            if count>10:
                        break
            for y in x:
                if count>10:
                    break
                print "\n**",y,"**"
                for z in x[y]:
                    if count>10:
                        break
                    count+=1
                    print z.id," ",z.name
    print "\nfclosure subset"
    count=0  
    while count<10:
        for x in fclosure:
            if count>10:
                        break
            for y in x:
                if count>10:
                    break
                print "\n**",y,"**"
                for z in x[y]:
                    if count>10:
                        break
                    count+=1
                    print z.id," ",z.name
    
    

def optionParser():
    parser=optparse.OptionParser()
    #parser.add_option("-o","--ontology",dest="ontoChoice",default="0",help="Which ontology? 0 for GO, anything else for MP. (default=%default)")
    #parser.add_option("-e","--evidence",dest="evidenceCodeStrings",default="None",help="What evidence codes would you like to remove? (Separate evidence codes by commas. Spaces can be used. Specify 'None' to not remove evidence codes. See http://www.geneontology.org/GO.evidence.shtml)(default=%default)")
    #parser.add_option("-f","--file",dest="fileName",default="data\gene_association.mgi",help="Which gene or phenotype file would you like to use as input?(default=%default)")
    #parser.add_option("-d","--diseasefile",dest="diseaseFile",default="data\Geno_11_OMIM.txt",help="For use with MP terms. Specify which file, containing OMIM data, is desired for input.(default=%default)")
    #parser.add_option("-l","--length",type="int",dest="length",default=25,help="Select how many results (matches) are desired. Values will be rounded down to nearest integer of lesser value.(default=%default)")

    #above commented options will probably have their place in final iteration

    parser.add_option("-c","--config",dest="configFile",default="C:\Users\s-osterh\Desktop\simmer\config.cfg",help="Specify config file location. (default=%default)")
    (options,args)=parser.parse_args()
    return options

main()
