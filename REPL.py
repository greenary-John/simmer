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
from icLib import Logger

#NOTE: The loops contained within main may be better wrapped in a function
#and handled that way. My only concern with that is I don't know how to
#exit the program while not in the main method.

def main():
    menu=['''
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
  
''','''
Which would you like to search with?
"0"             =   search by object
"1"             =   search by set of terms
"quit"          =   quit the loop
''','''
Please name the object you'd like to search by.
Ex:     "MGI:98351"
''']
    logger=Logger.Logger()
    print "Precomputing..."
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    user_choice=raw_input(menu[0])
    while user_choice!="search":
        if user_choice=="quit":
            quit()
        print "\n",choiceProcessing(0,user_choice,ontman,annman,cm),"\n"
        user_choice=raw_input(menu[0])
    print "Building CompiledAnnotationSet (paying overhead)."
    cas=CompiledAnnotationSet.CompiledAnnotationSet(annman.annotationSets[choices[0]],choices[1],ontman)
    while True:
        user_choice=raw_input(menu[1])
        if user_choice=="quit":
            quit()
        user_choice=choiceProcessing(1,user_choice,ontman,annman,cm)
        if user_choice==0:
            user_choice=raw_input(menu[2])
        if user_choice==1:
            continue #for now, continue. update whenever term set search is supported
        
        rBMA=cas.resnikBMA(AnnotatedObject.AnnotatedObject.getAnnotatedObj(user_choice),25)
        print "Top 25 Resnik BMA results for",user_choice    
        for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True):
            print x,"\t\t",rBMA[x]
            logger.debug("".join(("\t",x.__str__(),"\t\t",str(rBMA[x]))))
        
        jExt=cas.jaccardExt(AnnotatedObject.AnnotatedObject.getAnnotatedObj(user_choice),25)
        print "\nTop 25 Jaccard Extended results for",user_choice    
        for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True):
            print x,"\t\t",jExt[x]
            logger.debug("".join(("\t",x.__str__(),"\t\t",str(jExt[x]))))

        gExt=cas.gicExt(AnnotatedObject.AnnotatedObject.getAnnotatedObj(user_choice),25)
        print "\nTop 25 GIC Extended results for",user_choice    
        for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True):
            print x,"\t\t",gExt[x]
            logger.debug("".join(("\t",x.__str__(),"\t\t",str(gExt[x]))))
    
def setConfigOptions(op):
    #is this done correctly?
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
def choiceProcessing(run,choice,ontman,annman,conman):
    if choice=="evCodesQ"and run==0:
        return choices[1]
    elif choice=="annotationQ"and run==0:
        return annman.getSet()
    elif choice=="ontologyQ"and run==0:
        return ontman.getOntology()
    elif choice=="configDetails"and run==0:
        return configDetails(conman)
    elif choice=="annotationSel"and run==0:
        print annman.getSet()
        choices[0]=raw_input("Which annotationSet do you want to use?\n")
        return choices[0]
    elif choice=="evCodesClear"and run==0:
        choices[1]=set([])
        return choices[1]
    elif choice=="evCodes"and run==0:
        choices[1].add(raw_input("Which evidence code would you like to append to the exclusion list?"))
        return choices[1]
    elif choice=="search"and run==0:
        pass
    elif choice=="0"and run==1:
        return 0
    elif choice=="1"and run==1:
        print "\nTerm set search not yet supported. Please search by object."
        return 1
    else:
        return "Choice not understood; please try again."
        
def configDetails(conman):
    print conman.cp.sections(),"\n"
    choiceOptionInquiry=raw_input("\nWhich section would you like?\n")
    return conman.cp.getConfigObj(choiceOptionInquiry)

if __name__=='__main__':
    choices=["geneGO",set(["ISS","ISA","ISO","ISM","IGC","IBA","IBD","IKR","IRD","RCA"])]
    main()


