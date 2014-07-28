'''simmer
This is the hardcoded command line driver implementation of the gene and
mouse strain search engine. Queries can be made through hardcoding them as
input.

Author: Patrick Osterhaus   s-osterh
'''
import os
import optparse
import ConfigParser

from icLib import Ontology
from icLib import DAG
from icLib import ConfigManager
from icLib import OntologyManager
from icLib import AnnotationManager
from icLib import CompiledAnnotationSet
from icLib import AnnotatedObject
from icLib import Logger
from icLib import Labeler
from icLib import SimmerEngine

def main():
    global simmercon
    print "Pre-Computation I..."
    logger=Logger.Logger()
    logger.debug("\tStart!\t\tBeginning Precomputation I.")
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    labeler=Labeler.Labeler(simmercon)
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    if simmercon.get("CmdLineOpts","annSetChoice")=="geneGO":
        labelType="gene"
    if simmercon.get("CmdLineOpts","annSetChoice")=="genotypeMP":
        labelType="genotype"
        
    annSetChoice=simmercon.get("CmdLineOpts","annSetChoice")
    evCodesChoice=simmercon.get("CmdLineOpts","evCodesChoice")
    searchType=simmercon.get("CmdLineOpts","searchType")
    searchInput=simmercon.get("CmdLineOpts","searchInput")
    namespaceChoice=simmercon.get("CmdLineOpts","namespaceChoice")
    methodChoice=simmercon.get("CmdLineOpts","methodChoice")
    length=int(simmercon.get("CmdLineOpts","length"))

    results=SimmerEngine.requestSubmissionPC(annSetChoice,evCodesChoice,searchType,searchInput,namespaceChoice,methodChoice,length,logger,labeler,ontman,annman)
    
    print "\n",str(length),"results for:",namespaceChoice,":",methodChoice,":",searchInput
    logger.debug("".join(("\n",str(length),"results for:",namespaceChoice,":",methodChoice,":",searchInput)))
    for x in sorted(results,key=lambda entry:results[entry],reverse=True):
        print labeler.get(labelType,x.id),"\t\t",results[x]
        logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(results[x]))))
    print "\n"," ".join([x.id for x in sorted(results,key=lambda entry:results[entry],reverse=True)])

 
def setConfigOptions(op):
    op.add_option("-a","--annSet",metavar="STRING",dest="annSetChoice",default="geneGO",type="string",help="Desired annSet from the config file. Use section header name. (default=%default)")
    op.add_option("-e", "--evCodes",metavar="STRING",dest="evCodesChoice",default="ND",type="string",help="Desired excluded evidence codes (comma/space delimited list) (default=%default)")
    op.add_option("-s","--searchType",metavar="STRING",dest="searchType",default="object",type="string",help="Specify object or list for object or term-set search, respectively. (default=%default)")
    op.add_option("-q","--query",metavar="STRING",dest="searchInput",default="MGI:87961",type="string",help="Desired query. (e.g., 'MGI:87961' or 'GO:0008150,GO:0008219') (default=%default)")
    op.add_option("-n","--namespace",metavar="STRING",dest="namespaceChoice",default="biological_process",type="string",help="Specify namespace desired for use within search engine. (default=%default)")
    op.add_option("-m","--method",metavar="STRING",dest="methodChoice",default="resnikBMA",type="string",help="Specif which sem sim method is desired for use (i.e., resnikBMA, jaccardExt, or gicExt). (default=%default)")
    op.add_option("-l","--length",metavar="INT",dest="length",default="25",type="string",help="Specify the desired length of returned set of results. (default=%default)")
    
if __name__=='__main__':
    main()
