'''REPL
This is the Read-Eval-Print-Loop implementation of the gene and mouse model
search engine. Queries are made within the command prompt.

Author: Patrick Osterhaus   s-osterh
'''
import sys
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

#NOTE: The loops contained within main may be better wrapped in a function
#and handled that way. My only concern with that is I don't know how to
#exit the program while not in the main method.

def main():
    menu=['''
What would you like to do? (Enter "h" for help)
''','''
Which would you like to search with?
"1"             =   search by object
"2"             =   search by set of terms
"restart"       =   start over (new CompiledAnnotationSet)
"quit"          =   quit the loop
''','''
Please name the object you'd like to search by.
Ex:     "MGI:87961"
Ex:     "MGI:3526657"
''','''
Please type the list of terms, separated by spaces or commas, you'd like to search by.
Ex:     "GO:0008219,GO:0008150"
''','''
Please specify which namespace you'd like to compare the query in:
"1"            =   "biological_process"
"2"            =   "molecular_function"
"3"            =   "cellular_component"
''','''
"e q"           =   display current evidenceCode exclusion list
"a q"           =   display available annotation sets
"o q"           =   display available ontologies
"c"             =   interrogate config file

"a s"           =   select from available annotation sets
"e c"           =   clear evidence code exclusion list
"e a"           =   specify evidence codes to add to exclusion list

"s"             =   use the search program
"quit"          =   quit the loop
''','''
Please specify which semantic similarity measure you'd like to use.
"1"             =   Resnik Best Match Average
"2"             =   Jaccard Extended
"3"             =   GIC Extended
''']
    logger=Logger.Logger()
    print "Precomputing..."
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    labeler=Labeler.Labeler(simmercon)
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    while True:
        user_choice=raw_input(menu[0])
        while user_choice!="s":
            if user_choice=="quit":
                user_choice=raw_input('Are you sure? (Type "quit" to quit; otherwise use another command.)\n')
                if user_choice=="quit":
                    quit()
            print "\n",choiceProcessing(menu[5],user_choice,ontman,annman,cm),"\n"
            user_choice=raw_input(menu[0])
        print "Building CompiledAnnotationSet (paying overhead)."
        cas=CompiledAnnotationSet.CompiledAnnotationSet.getCAS(annman.annotationSets[choices[0]],list(choices[1]),ontman)
        while True:
            user_choice=raw_input(menu[1]).replace("1","object").replace("2","list")
            if user_choice=="quit":
                user_choice=raw_input('Are you sure? (Type "quit" to quit; otherwise type anything else.)\n')
                if user_choice=="quit":
                    quit()
                else:
                    continue
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
                if choices[0]=="genotypeMP":
                    user_choice3="MPheno.ontology"
                    labelType="genotype"
                else:
                    user_choice3=raw_input(menu[4]).replace("1","biological_process").replace("2","molecular_function").replace("3","cellular_component")
                    labelType="gene"
                    if user_choice3 not in ["cellular_component","biological_process","molecular_function"]:
                        print "\nCannot interpret input. Please try again."
                        continue
                while True:
                    user_choice4=raw_input(menu[6])
                    if user_choice4 not in ["1","2","3"]:
                        print "\nCannot interpret input. Please try again."
                        continue
                    
                    if user_choice4=="1":
                        rBMA=cas.resnikBMA(user_choice,user_choice2,user_choice3,25)
                        if isinstance(user_choice2,list):
                            print "\n",user_choice3,":Top 25 Resnik BMA results for",[x.__str__() for x in user_choice2].__str__()
                            logger.debug("".join((user_choice3,"Top 25 Resnik BMA results for ",[x.__str__() for x in user_choice2].__str__())))
                        else:
                            print "\n",user_choice3,":Top 25 Resnik BMA results for",labeler.get(labelType,user_choice2.id)
                            logger.debug("".join((user_choice3,"Top 25 Resnik BMA results for ",labeler.get(labelType,user_choice2.id))))
                        for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True):
                            print labeler.get(labelType,x.id),"\t\t",rBMA[x]
                            logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(rBMA[x]))))
                        print "\n"," ".join([x.id for x in sorted(rBMA,key=lambda entry:rBMA[entry],reverse=True)])
                        

                    if user_choice4=="2":
                        jExt=cas.jaccardExt(user_choice,user_choice2,user_choice3,25)
                        if isinstance(user_choice2,list):
                            print "\n",user_choice3,":Top 25 Jaccard Extended results for",[x.__str__() for x in user_choice2].__str__()
                            logger.debug("".join((user_choice3,"Top 25 Jaccard Extended results for ",[x.__str__() for x in user_choice2].__str__())))
                        else:
                            print "\n",user_choice3,":Top 25 Jaccard Extended results for",labeler.get(labelType,user_choice2.id)
                            logger.debug("".join((user_choice3,"Top 25 Jaccard Extended results for ",labeler.get(labelType,user_choice2.id))))
                        for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True):
                            print labeler.get(labelType,x.id),"\t\t",jExt[x]
                            logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(jExt[x]))))
                        print "\n"," ".join([x.id for x in sorted(jExt,key=lambda entry:jExt[entry],reverse=True)])

                    if user_choice4=="3":
                        gExt=cas.gicExt(user_choice,user_choice2,user_choice3,25)
                        if isinstance(user_choice2,list):
                            print "\n",user_choice3,":Top 25 GIC Extended results for",[x.__str__() for x in user_choice2].__str__()
                            logger.debug("".join((user_choice3,"Top 25 GIC Extended results for ",[x.__str__() for x in user_choice2].__str__())))
                        else:
                            print "\n",user_choice3,":Top 25 GIC Extended results for",labeler.get(labelType,user_choice2.id)
                            logger.debug("".join((user_choice3,"Top 25 GIC Extended results for ",labeler.get(labelType,user_choice2.id))))
                        for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True):
                            print labeler.get(labelType,x.id),"\t\t",gExt[x]
                            logger.debug("".join(("\t",labeler.get(labelType,x.id),"\t\t",str(gExt[x]))))
                        print "\n"," ".join([x.id for x in sorted(gExt,key=lambda entry:gExt[entry],reverse=True)])
                            
                    if raw_input('\nWould you like to search again with a new semantic similarity measure?\n"y"\t\t=\tSearch again\nanything else\t=\tDo not search again\n')=="y":
                        continue
                    break
                break
    
def setConfigOptions(op):
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
def choiceProcessing(menu,choice,ontman,annman,conman):
    if choice=="h":
        return menu
    elif choice=="e q":
        return choices[1]
    elif choice=="a q":
        return annman.getSet()
    elif choice=="o q":
        return ontman.getOntology()
    elif choice=="c":
        return configDetails(conman)
    elif choice=="a s":
        print annman.getSet()
        choices[0]=raw_input("Which annotationSet do you want to use?\n")
        return choices[0]
    elif choice=="e c":
        choices[1]=set([])
        return choices[1]
    elif choice=="e a":
        choices[1]|=set(raw_input("Which evidence codes would you like to append to the exclusion list?\n(Please enter as comma or space delimited list.)\n").replace(" ",",").split(","))
        return choices[1]
    elif choice=="s":
        pass
    else:
        return "Choice not understood; please try again."
        
def configDetails(conman):
    print conman.cp.sections(),"\n"
    choiceOptionInquiry=raw_input("\nWhich section would you like? (Hit enter for all.)\n")
    return conman.cp.getConfigObj(choiceOptionInquiry)

if __name__=='__main__':
    choices=["geneGO",set(["ND"])]
    main()


