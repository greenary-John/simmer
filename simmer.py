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

def main():
    logger=Logger.Logger()
    logger.debug("\tStart!\t\tBeginning Precomputation.")
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    labeler=Labeler.Labeler(simmercon)
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    
    logger.debug("\tNow building CompiledAnnotationSet")
    '''
    test=CompiledAnnotationSet.CompiledAnnotationSet(annman.annotationSets["geneMP"],[],ontman)

    rBMA=test.resnikBMA("object",AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:3526657"),"MPheno.ontology",25)
    print '\nMP:ResnikBMA:MGI:3526657'    
    logger.debug('\nMP:ResnikBMA:MGI:3526657')
    for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True):
        print x,"\t\t",rBMA[x]
        logger.debug("".join(("\t",x.__str__(),"\t\t",str(rBMA[x]))))

    jExt=test.jaccardExt("object",AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:3526657"),"MPheno.ontology",25)
    print '\nMP:JaccardExt:MGI:3526657'
    logger.debug('\nMP:JaccardExt:MGI:3526657')
    for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True):
        print x,"\t\t",jExt[x]
        logger.debug("".join(("\t",x.__str__(),"\t\t",str(jExt[x]))))
    
    gExt=test.gicExt("object",AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:3526657"),"MPheno.ontology",25)
    print '\nMP:gicExt:MGI:3526657'
    logger.debug('\nMP:gicExt:MGI:3526657)')
    for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True):
        print x,"\t\t",gExt[x]
        logger.debug("".join(("\t",x.__str__(),"\t\t",str(gExt[x]))))
    '''
    
    test=CompiledAnnotationSet.CompiledAnnotationSet(annman.annotationSets["geneGO"],["ISS","ISA","ISO","ISM","IGC","IBA","IBD","IKR","IRD","RCA"],ontman)
    labelType="gene"
    rBMA=test.resnikBMA("object",AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:87961"),"biological_process",25)
    print '\nBP:ResnikBMA:MGI:87961'    
    logger.debug('\nBP:ResnikBMA:MGI:87961')
    for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True):
        print labeler.get(labelType,x.id),"\t\t",rBMA[x]
        logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(rBMA[x]))))
    print [x.id for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True)]

    jExt=test.jaccardExt("object",AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:87961"),"biological_process",25)
    print '\nBP:JaccardExt:MGI:87961'
    logger.debug('\nBP:JaccardExt:MGI:87961')
    for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True):
        print labeler.get(labelType,x.id),"\t\t",jExt[x]
        logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(jExt[x]))))
    print [x.id for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True)]
    
    gExt=test.gicExt("object",AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:87961"),"biological_process",25)
    print '\nBP:gicExt:MGI:87961'
    logger.debug('\nBP:gicExt:MGI:87961)')
    for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True):
        print labeler.get(labelType,x.id),"\t\t",gExt[x]
        logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(gExt[x]))))
    print [x.id for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True)]
    
def setConfigOptions(op):
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
if __name__=='__main__':
    main()
