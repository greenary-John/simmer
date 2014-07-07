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
    ontman=Ontology_Manager.Ontology_Manager(simmercon)
    annman=Annotation_Manager.Annotation_Manager(simmercon)
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
    print "\nannman.anns[\"geneMP\"][0]\n",annman.anns["geneMP"][0]
    
    #formatted printing of ontology namespaces and annotation subsets, respectively
    '''
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
    '''

def setConfigOptions(op):
    #is this done correctly?
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
if __name__=='__main__':
    main()
