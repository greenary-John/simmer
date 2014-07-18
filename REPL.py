import sys
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
    menu='''
What would you like to do?
"evCodesQ"      =   display current evidenceCode exclusion list
"annotationQ"   =   display available annotation sets
"ontologyQ"     =   display available ontologies
"configDetails" =   interrogate config file

"annotationSel" =   select from available annotation sets
"evCodesClear"  =   clear evidence code exclusion list
"evCodes"       =   specify evidence codes to add to exclusion list

"search"        =   use the search program
"quit"          =   quit the loop
  
'''
    print "Precomputing..."
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    user_choice=raw_input(menu)
    while user_choice!="search":
        if user_choice=="quit":
            quit()
        print "\n",choiceProcessing(user_choice,ontman,annman,cm),"\n"
        user_choice=raw_input(menu)
    cas=CompiledAnnotationSet.CompiledAnnotationSet(annman.annotationSets[choices[0]],choices[1],ontman)
    print "\nlen(cas.term2IC)\n",len(cas.term2IC)
    
def setConfigOptions(op):
    #is this done correctly?
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
def choiceProcessing(choice,ontman,annman,conman):
    if choice=="evCodesQ":
        return choices[1]
    elif choice=="annotationQ":
        return annman.getSet()
    elif choice=="ontologyQ":
        return ontman.getOntology()
    elif choice=="configDetails":
        return configDetails(conman)
    elif choice=="annotationSel":
        print annman.getSet()
        choices[0]=raw_input("Which annotationSet do you want to use?\n")
        return choices[0]
    elif choice=="evCodesClear":
        choices[1]=[]
        return choices[1]
    elif choice=="evCodes":
        choices[1].append(raw_input("Which evidence code would you like to append to the exclusion list?"))
        return choices[1]
    elif choice=="search":
        pass
    else:
        print "Choice not understood; please try again."
        

def configDetails(conman):
    print conman.cp.sections(),"\n"
    choiceOptionInquiry=raw_input("\nWhich section would you like?\n")
    return conman.cp.getConfigObj(choiceOptionInquiry)

def Termination(Exception):
    def __init(self):
        pass

if __name__=='__main__':
    choices=["geneGO",["ISS","ISA","ISO","ISM","IGC","IBA","IBD","IKR","IRD","RCA"]]
    main()


