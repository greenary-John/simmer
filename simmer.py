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
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    logger=Logger.Logger()
    logger.debug("\tNow building CompiledAnnotationSet")
    test=CompiledAnnotationSet.CompiledAnnotationSet(annman.annotationSets["geneGO"],["ISS","ISA","ISO","ISM","IGC","IBA","IBD","IKR","IRD","RCA"],ontman)
    #ontologies=simmercon.getOntologies()
    #annotations=simmercon.getAnnotations()
    #rclosure=Extended_Closure.ReverseClosure().multigo(ontologies[1])
    #fclosure=Extended_Closure.ForwardClosure().multigo(ontologies[1])


    #above this comment is mostly algorithmic
    #below this comment is mostly printing to validate variables and output
    #print conman.sectionInfo,"\n\n"
    '''print "\nSections with 'type' of 'ontology'\n",simmercon.sectionsWith("type","ontology")
    print "\ngetConfigObj(\"GO\")\n",simmercon.getConfigObj("GO")
    print "\ngetConfigObj()\n",simmercon.getConfigObj()
    print "\nontman.onts\n",ontman.onts
    print "\nannman.annotationSets[\"geneGO\"]\n",annman.annotationSets["geneGO"]
    print "\nannman.annotationSets[\"geneGO\"].getAnnotsByTerm(\"GO:0007612\")\n",annman.annotationSets["geneGO"].getAnnotsByTerm("GO:0007612")
    print "\nannman.annotationSets[\"geneGO\"].getAnnotsByObject(\"MGI:1918911\")\n",annman.annotationSets["geneGO"].getAnnotsByObject("MGI:1918911"),"\n"
    #print "\ntype(annman.annotationSets[\"geneGO\"].getAnnotsByObject().keys()[0])\n",type(annman.annotationSets["geneGO"].getAnnotsByObject().keys()[0])
    #print "\nannman.annotationSets[\"geneGO\"].getAnnotsByTerm()",annman.annotationSets["geneGO"].getAnnotsByTerm()    
    #print "\nannman.annotationSets[\"geneGO\"].getAnnotsByObject()",annman.annotationSets["geneGO"].getAnnotsByObject() 
    #print "Cardinality before filtering:\t",len(test.annset.getAnnotatedObjects()),"annotations"    
    #print "Cardinality after filtering:\t",len(test.annset.getAnnotatedObjects()),"annotations"
    #print "\ntest.getAnnotatedObjects()\n",test.annset.getAnnotatedObjects()
    print "\nClosure sample:\n",test.annset.ontology.closure[test.annset.getAnnotsByObject("MGI:98351")[0].ontTerm],"\n"
    print "There should be",len(annman.annotationSets["geneGO"].getAnnotsByObject()),"obj2term entries."
    print "There should be",len(annman.annotationSets["geneGO"].getAnnotsByTerm()),"term2obj entries."
    print len(test.obj2term),"obj2term entries"
    print len(test.term2obj),"term2obj entries"
    print "\ntest.annset.getAnnotsByTerm(\"GO:0007612\")\n",test.annset.getAnnotsByTerm("GO:0007612")
    #print "\ntest.obj2term[Annotated_Object.AnnotatedObject.getAnnotatedObj(\"MGI:1918911\")]\n",test.obj2term[Annotated_Object.AnnotatedObject.getAnnotatedObj("MGI:1918911")]
    #statement above printing many instances of OboTerm; why isn't __str__ formatting them?
    print "\nannman.getSet(\"geneGO\")\n",annman.getSet("geneGO")
    print "\nontman.getOntology()\n",ontman.getOntology()
    #print "\ntest.term2IC\n",test.term2IC
    print "\nmax(test.term2IC.values())\n",max(test.term2IC.values())
    print "\nlen(test.term2IC)\n",len(test.term2IC)'''
    logger.debug("\tNow starting resnikBMA\n")
    #print "\ntest.annotationCardinality\n",test.annotationCardinality
    #print "\ntest.rowMICA(AnnotatedObject.AnnotatedObject.getAnnotatedObj(\"MGI:98351\"),test.annset.getAnnotsByTerm(\"GO:0007612\"))\n",test.rowMICA(AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:98351"),test.annset.getAnnotsByTerm("GO:0007612"))
    #print "\ntest.objCompare(AnnotatedObject.AnnotatedObject.getAnnotatedObj(\"MGI:98351\"),AnnotatedObject.AnnotatedObject.getAnnotatedObj(\"MGI:3619222\"))\n",test.objCompare(AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:98351"),AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:3619222"))
    results=test.resnikResults(AnnotatedObject.AnnotatedObject.getAnnotatedObj("MGI:98351"),25)
    print "\ntest.resnikResults(AnnotatedObject.AnnotatedObject.getAnnotatedObj(\"MGI:98351\"),25)"    
    logger.debug("\ntest.resnikResults(AnnotatedObject.AnnotatedObject.getAnnotatedObj(\"MGI:98351\"),25)")
    #print sorted(results,key=lambda entry:results[entry],reverse=True)
    for x in sorted(results,key=lambda entry:results[entry],reverse=True):
        print x,"\t\t",results[x]
        logger.debug("".join(("\t",x,"\t\t",results[x])))
    #print "\ntest.pair2MICA[(test.annset.ontology.getTerm(\"GO:0007612\"),test.annset.ontology.getTerm(\"GO:0007611\"))]\n",test.pair2MICA[(test.annset.ontology.getTerm("GO:0007612"),test.annset.ontology.getTerm("GO:0007611"))]
   
def setConfigOptions(op):
    #is this done correctly?
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
if __name__=='__main__':
    main()
