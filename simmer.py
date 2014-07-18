import os
import ConfigParser
import time

from icLib import Ontology
from icLib import DAG
from icLib import ConfigManager
from icLib import OntologyManager
from icLib import AnnotationManager
from icLib import OntologyAnnotationCompiler
from icLib import CompiledAnnotationSet
from icLib import AnnotatedObject
from icLib import Logger

def main():
    logger=Logger.Logger()
    logger.debug("\tStart!\t\tBeginning Precomputation.")
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    
    logger.debug("\tNow building CompiledAnnotationSet")
    test=CompiledAnnotationSet.CompiledAnnotationSet(annman.annotationSets["geneGO"],["ISS","ISA","ISO","ISM","IGC","IBA","IBD","IKR","IRD","RCA"],ontman)
    
    rBMA=test.resnikBMA(AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:98351"),25)
    print '\nResnikBMA:"MGI:98351"'    
    logger.debug('\nResnikBMA:"MGI:98351"')
    for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True):
        print x,"\t\t",rBMA[x]
        logger.debug("".join(("\t",x.__str__(),"\t\t",str(rBMA[x]))))
        
    jExt=test.jaccardExt(AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:98351"),25)
    print '\nJaccardExt:"MGI:98351"'
    logger.debug('\nJaccardExt:"MGI:98351"')
    for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True):
        print x,"\t\t",jExt[x]
        logger.debug("".join(("\t",x.__str__(),"\t\t",str(jExt[x]))))
    
    gExt=test.gicExt(AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:98351"),25)
    print '\ngicExt:MGI:98351'
    for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True):
        print x,"\t\t",gExt[x]
        logger.debug("".join(("\t",x.__str__(),"\t\t",str(gExt[x]))))
        
def setConfigOptions(op):
    #is this done correctly?
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
if __name__=='__main__':
    main()
