import os
import ConfigParser

from icLib import Ontology
from icLib import DAG
from icLib import Config_Manager
from icLib import Ontology_Manager
from icLib import Extended_Closure
from icLib import Annotation_Manager

def main():
    cm=Config_Manager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    ontman=Ontology_Manager.Ontology_Manager(simmercon)
    annman=Annotation_Manager.Annotation_Manager(simmercon,ontman)
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
    print "\nannman.annotationSets[\"geneGO\"].getAnnotsByTerm(\"GO:0031403\")\n",annman.annotationSets["geneGO"].getAnnotsByTerm("GO:0031403")
    print "\nannman.annotationSets[\"geneGO\"].getAnnotsByObject(\"MGI:1918911\")\n",annman.annotationSets["geneGO"].getAnnotsByObject("MGI:1918911")
    #print "\nannman.annotationSets[\"geneGO\"].getAnnotsByTerm()",annman.annotationSets["geneGO"].getAnnotsByTerm()    
    #print "\nannman.annotationSets[\"geneGO\"].getAnnotsByObject()",annman.annotationSets["geneGO"].getAnnotsByObject() 
    #formatted printing of ontology namespaces and annotation subsets, respectively
    
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

def setConfigOptions(op):
    #is this done correctly?
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
if __name__=='__main__':
    main()
