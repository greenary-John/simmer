import os
import ConfigParser

from icLib import Ontology
from icLib import DAG
from icLib import ConfigManager
from icLib import OntologyManager
from icLib import AnnotationManager
from icLib import OntologyAnnotationCompiler
from icLib import CompiledAnnotationSet
from icLib import AnnotatedObject

def main():
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    #ontologies=simmercon.getOntologies()
    #annotations=simmercon.getAnnotations()
    #rclosure=Extended_Closure.ReverseClosure().multigo(ontologies[1])
    #fclosure=Extended_Closure.ForwardClosure().multigo(ontologies[1])


    #above this comment is mostly algorithmic
    #below this comment is mostly printing to validate variables and output
    #print conman.sectionInfo,"\n\n"
    print "\nSections with 'type' of 'ontology'\n",simmercon.sectionsWith("type","ontology")
    print "\ngetConfigObj(\"GO\")\n",simmercon.getConfigObj("GO")
    print "\ngetConfigObj()\n",simmercon.getConfigObj()
    print "\nontman.onts\n",ontman.onts
    print "\nannman.annotationSets[\"geneGO\"]\n",annman.annotationSets["geneGO"]
    print "\nannman.annotationSets[\"geneGO\"].getAnnotsByTerm(\"GO:0007612\")\n",annman.annotationSets["geneGO"].getAnnotsByTerm("GO:0007612")
    print "\nannman.annotationSets[\"geneGO\"].getAnnotsByObject(\"MGI:1918911\")\n",annman.annotationSets["geneGO"].getAnnotsByObject("MGI:1918911"),"\n"
    #print "\nannman.annotationSets[\"geneGO\"].getAnnotsByTerm()",annman.annotationSets["geneGO"].getAnnotsByTerm()    
    #print "\nannman.annotationSets[\"geneGO\"].getAnnotsByObject()",annman.annotationSets["geneGO"].getAnnotsByObject() 
    #print "Cardinality before filtering:\t",len(flatten(annman.annotationSets["geneGO"].getAnnotsByObject().values())),"annotations"
    test=CompiledAnnotationSet.CompiledAnnotationSet(annman.annotationSets["geneGO"],["ISS","ISA","ISO","ISM","IGC","IBA","IBD","IKR","IRD","RCA"],ontman)
    #print "Cardinality after filtering:\t",len(flatten(test.annset.getAnnotsByObject().values())),"annotations"
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
    print "\nlen(test.term2IC)\n",len(test.term2IC)
    print "\n",len(test.term2obj),"term2obj entries"
    print "\ntest.annotationCardinality\n",test.annotationCardinality
    print "\ntest.pair2MICA[(test.ontology.getTerm(\"GO:0007612\"),test.ontology.getTerm(\"GO:0007611\"))]\n",test.pair2MICA[(test.ontology.getTerm("GO:0007612"),test.ontology.getTerm("GO:0007611"))]
    
    
    '''
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
    '''
def flatten(lst):
	return sum((flatten(x) if isinstance(x, list) else [x]for x in lst),[])
    
def setConfigOptions(op):
    #is this done correctly?
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
if __name__=='__main__':
    main()
