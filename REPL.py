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
"1"             =   search by object
"2"             =   search by set of terms
"restart"       =   start over (new CompiledAnnotationSet)
"quit"          =   quit the loop
''','''
Please name the object you'd like to search by.
Ex:     "MGI:98351"
Ex:     "MGI:3526657"
''','''
Please type the list of terms, separated by spaces or commas, you'd like to search by.
Ex:     "GO:0008219,GO:0008150"
''','''
Please specify which namespace you'd like to compare the query in:
"1"            =   "biological_process"
"2"            =   "molecular_function"
"3"            =   "cellular_component"
''']
    logger=Logger.Logger()
    print "Precomputing..."
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    while True:
        user_choice=raw_input(menu[0])
        while user_choice!="search":
            if user_choice=="quit":
                quit()
            print "\n",choiceProcessing(user_choice,ontman,annman,cm),"\n"
            user_choice=raw_input(menu[0])
        print "Building CompiledAnnotationSet (paying overhead)."
        cas=CompiledAnnotationSet.CompiledAnnotationSet(annman.annotationSets[choices[0]],choices[1],ontman)
        while True:
            user_choice=raw_input(menu[1]).replace("1","object").replace("2","list")
            if user_choice=="quit":
                quit()
            elif user_choice=="restart":
                break
            elif user_choice=="object":
                user_choice2=AnnotatedObject.AnnotatedObject.getAnnotatedObj(raw_input(menu[2]))
            elif user_choice=="list":
                user_choice2=[]
                for x in raw_input(menu[3]).replace(" ",",").split(","):
                    user_choice2.append(cas.annset.ontology.getTerm(x))
            else:
                print "\nCannot interpret input. Please try again."
                continue
            while True:
                if choices[0]=="geneMP":
                    user_choice3="MPheno.ontology"
                else:
                    user_choice3=raw_input(menu[4]).replace("1","biological_process").replace("2","molecular_function").replace("3","cellular_component")
                    if user_choice3 not in ["cellular_component","biological_process","molecular_function"]:
                        print "\nCannot interpret input. Please try again."
                        continue
                rBMA=cas.resnikBMA(user_choice,user_choice2,user_choice3,25)
                if isinstance(user_choice2,list):
                    print "\n",user_choice3,":Top 25 Resnik BMA results for",[x.__str__() for x in user_choice2].__str__()
                    logger.debug("".join((user_choice3,"Top 25 Resnik BMA results for ",[x.__str__() for x in user_choice2].__str__())))
                else:
                    print "\n",user_choice3,":Top 25 Resnik BMA results for",user_choice2.__str__()
                    logger.debug("".join((user_choice3,"Top 25 Resnik BMA results for ",user_choice2.__str__())))
                for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True):
                    print x,"\t\t",rBMA[x]
                    logger.debug("".join(("\t",x.__str__(),"\t\t",str(rBMA[x]))))
            
                jExt=cas.jaccardExt(user_choice,user_choice2,user_choice3,25)
                if isinstance(user_choice2,list):
                    print "\n",user_choice3,":Top 25 Jaccard Extended results for",[x.__str__() for x in user_choice2].__str__()
                    logger.debug("".join((user_choice3,"Top 25 Jaccard Extended results for ",[x.__str__() for x in user_choice2].__str__())))
                else:
                    print "\n",user_choice3,":Top 25 Jaccard Extended results for",user_choice2.__str__()
                    logger.debug("".join((user_choice3,"Top 25 Jaccard Extended results for ",user_choice2.__str__())))
                for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True):
                    print x,"\t\t",jExt[x]
                    logger.debug("".join(("\t",x.__str__(),"\t\t",str(jExt[x]))))
    
                gExt=cas.gicExt(user_choice,user_choice2,user_choice3,25)
                if isinstance(user_choice2,list):
                    print "\n",user_choice3,":Top 25 GIC Extended results for",[x.__str__() for x in user_choice2].__str__()
                    logger.debug("".join((user_choice3,"Top 25 GIC Extended results for ",[x.__str__() for x in user_choice2].__str__())))
                else:
                    print "\n",user_choice3,":Top 25 GIC Extended results for",user_choice2.__str__()
                    logger.debug("".join((user_choice3,"Top 25 GIC Extended results for ",user_choice2.__str__())))
                for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True):
                    print x,"\t\t",gExt[x]
                    logger.debug("".join(("\t",x.__str__(),"\t\t",str(gExt[x]))))

                break
    
def setConfigOptions(op):
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
        choices[1]=set([])
        return choices[1]
    elif choice=="evCodes":
        choices[1]|=set(raw_input("Which evidence codes would you like to append to the exclusion list?\n(Please enter as comma or space delimited list.)\n").replace(" ",",").split(","))
        return choices[1]
    elif choice=="search":
        pass
    else:
        return "Choice not understood; please try again."
        
def configDetails(conman):
    print conman.cp.sections(),"\n"
    choiceOptionInquiry=raw_input("\nWhich section would you like?\n")
    return conman.cp.getConfigObj(choiceOptionInquiry)

if __name__=='__main__':
    choices=["geneGO",set(["ISS","ISA","ISO","ISM","IGC","IBA","IBD","IKR","IRD","RCA"])]
    main()


