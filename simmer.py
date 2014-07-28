'''simmer
This is the hardcoded command line driver implementation of the gene and
mouse strain search engine. Queries can be made through hardcoding them as
input.

Author: Patrick Osterhaus   s-osterh
'''
import os
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
    print "Pre-Computation I..."
    logger=Logger.Logger()
    logger.debug("\tStart!\t\tBeginning Precomputation I.")
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    labeler=Labeler.Labeler(simmercon)
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)

    labelType="gene"
    rBMA=SimmerEngine.requestSubmissionPC("geneGO","ND","object","MGI:87961","biological_process","resnikBMA",25,logger,labeler,ontman,annman)
    print '\nBP:ResnikBMA:MGI:87961'    
    logger.debug('\nBP:ResnikBMA:MGI:87961')
    for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True):
        print labeler.get(labelType,x.id),"\t\t",rBMA[x]
        logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(rBMA[x]))))
    print "\n"," ".join([x.id for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True)])

    jExt=rBMA=SimmerEngine.requestSubmissionPC("geneGO","ND","object","MGI:87961","biological_process","jaccardExt",25,logger,labeler,ontman,annman)
    print '\nBP:JaccardExt:MGI:87961'
    logger.debug('\nBP:JaccardExt:MGI:87961')
    for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True):
        print labeler.get(labelType,x.id),"\t\t",jExt[x]
        logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(jExt[x]))))
    print "\n"," ".join([x.id for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True)])
    
    gExt=rBMA=SimmerEngine.requestSubmissionPC("geneGO","ND","object","MGI:87961","biological_process","gicExt",25,logger,labeler,ontman,annman)
    print '\nBP:gicExt:MGI:87961'
    logger.debug('\nBP:gicExt:MGI:87961)')
    for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True):
        print labeler.get(labelType,x.id),"\t\t",gExt[x]
        logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(gExt[x]))))
    print "\n"," ".join([x.id for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True)])
    
def setConfigOptions(op):
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
if __name__=='__main__':
    main()
