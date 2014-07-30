'''REPL
This is the Read-Eval-Print-Loop implementation of the gene and mouse model
search engine. Queries are made within the command prompt.

Author: Patrick Osterhaus   s-osterh
'''
import sys
import os
import ConfigParser
import time

from icLib import Ontology
from icLib import DAG
from icLib import ConfigManager
from icLib import OntologyManager
from icLib import AnnotationManager
from icLib import CompiledAnnotationSet
from icLib import AnnotatedObject
from icLib import Logger
from icLib import Labeler
from icLib import SimmerEngine

#NOTE: The loops contained within main may be better wrapped in a function
#and handled that way. My only concern with that is I don't know how to
#exit the program while not in the main method.
def main2():
    annSetChoice=raw_input("Which annSet would you like?\n> ")
    evCodesChoice=raw_input("Which evCodes should be removed?\n>    ").replace(" ,",",").replace(" ",",")
    searchType=raw_input("Search by object or list?\n>  ")
    searchInput=raw_input("Search what?\n>  ")
    namespaceChoice=raw_input("Which namespace should be used?\n>   ")
    methodChoice=raw_input("Which method should be used?\n> ")
    length=int(raw_input("How many results should be returned?\n>   "))
    results=SimmerEngine.requestSubmissionRaw(annSetChoice,evCodesChoice,searchType,searchInput,namespaceChoice,methodChoice,length)
    if searchType=="list":
        print "\n",namespaceChoice,": Top",length," ",methodChoice," results for",[x.__str__() for x in searchInput].__str__()
    else:
        print "\n",namespaceChoice,": Top",length," ",methodChoice," results for",searchInput
    for x in sorted(results,key=lambda entry:results[entry],reverse=True):
        print x,"\t\t",results[x]

def main():
    menu=['''
What would you like to do? (Enter "h" for help)
>\t''','''
Which would you like to search with?
"1"\t\t\t\t=\tsearch by object
"2"\t\t\t\t=\tsearch by set of terms
"restart"\t\t\t=\tstart over (new CompiledAnnotationSet)
"quit"\t\t\t\t=\tquit the loop
>\t''','''
Please name the object you'd like to search by.
Ex:\t\t"MGI:87961"
Ex:\t\t"MGI:3526657"
>\t''','''
Please type the list of terms, separated by spaces or commas, you'd like to search by.
Ex:\t\t"GO:0008219,GO:0008150"
>\t''','''
Please specify which namespace you'd like to compare the query in:
"1"\t\t\t\t=\t"biological_process"
"2"\t\t\t\t=\t"molecular_function"
"3"\t\t\t\t=\t"cellular_component"
>\t''','''
"e q"\t\t\t=\tdisplay current evidenceCode exclusion list
"a q"\t\t\t=\tdisplay available annotation sets
"o q"\t\t\t=\tdisplay available ontologies
"c"\t\t\t=\tinterrogate config file

"a s"\t\t\t=\tselect from available annotation sets
"e a"\t\t\t=\tspecify evidence codes to exclude

"s"\t\t\t=\tuse the search program
"quit"\t\t\t=\tquit the loop
>\t''','''
Please specify which semantic similarity measure you'd like to use.
"1"\t\t\t\t=\tResnik Best Match Average
"2"\t\t\t\t=\tJaccard Extended
"3"\t\t\t\t=\tGIC Extended
>\t''']
    start=time.time()
    print "Pre-Computation I..."
    logger=Logger.Logger()
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    labeler=Labeler.Labeler(simmercon)
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    print time.time()-start
    while True:
        user_choice=raw_input(menu[0])
        while user_choice!="s":
            if user_choice=="quit":
                user_choice=raw_input('Are you sure? (Type "quit" to quit; otherwise use another command.)\n>\t')
                if user_choice=="quit":
                    quit()
            print "\n",choiceProcessing(menu[5],user_choice,cm),"\n"
            user_choice=raw_input(menu[0])
        while True:            
            user_choice=raw_input(menu[1]).replace("1","object").replace("2","list")
            if user_choice=="quit":
                user_choice=raw_input('Are you sure? (Type "quit" to quit; otherwise type anything else.)\n>\t')
                if user_choice=="quit":
                    quit()
                else:
                    continue
            elif user_choice=="restart":
                break
            elif user_choice=="object":
                user_choice2=raw_input(menu[2])
            elif user_choice=="list":
                user_choice2=raw_input(menu[3])
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
                    user_choice4=raw_input(menu[6]).replace("1","resnikBMA").replace("2","jaccardExt").replace("3","gicExt")
                    if user_choice4 not in ["resnikBMA","jaccardExt","gicExt"]:
                        print "\nCannot interpret input. Please try again."
                        continue
                    user_choice5=int(raw_input("How many results should be returned?\n>\t"))
                    results=SimmerEngine.requestSubmissionPC(choices[0],choices[1],user_choice,user_choice2,user_choice3,user_choice4,user_choice5,logger,labeler,ontman,annman)
                    #if isinstance(user_choice2,list):
                        #print "\n",user_choice3,":Top",str(user_choice5),user_choice4,"results for",[x.__str__() for x in user_choice2].__str__()
                        #logger.debug("".join((user_choice3,":Top",str(user_choice5),user_choice4,"results for ",[x.__str__() for x in user_choice2].__str__())))
                    #else:
                        #print "\n",user_choice3,":Top",str(user_choice5),user_choice4,"results for",labeler.get(labelType,user_choice2)
                        #logger.debug("".join((user_choice3,":Top",str(user_choice5),user_choice4,"results for ",labeler.get(labelType,user_choice2))))
                    #for x in results:
                        #print labeler.get(labelType,x[0].id),"\t\t",x[1]
                        #logger.debug("".join((" ",labeler.get(labelType,x[0].id),"\t\t",str(x[1]))))
                    #print "\n"," ".join([x[0].id for x in results])
                    print results
                    logger.debug(results)
                            
                    if raw_input('\nWould you like to search again with a new semantic similarity measure?\n"y"\t\t=\tSearch again\nanything else\t=\tDo not search again\n>\t')=="y":
                        continue
                    break
                break
    
def setConfigOptions(op):
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
    
def choiceProcessing(menu,choice,conman):
    if choice=="h":
        return menu
    elif choice=="e q":
        return [x for x in choices[1].split(",")]
    elif choice=="a q":
        return conman.cp.sectionsWith("type","annotations")
    elif choice=="o q":
        return conman.cp.sectionsWith("type","ontology")
    elif choice=="c":
        return configDetails(conman)
    elif choice=="a s":
        print conman.cp.sectionsWith("type","annotations")
        choices[0]=raw_input("Which annotationSet do you want to use?\n>\t")
        return choices[0]
    elif choice=="e a":
        choices[1]=raw_input("Which evidence codes would you like to exclude?\n(Please enter as comma or space delimited list.)\n>\t").replace(" ,",",").replace(" ",",")
        return choices[1]
    elif choice=="s":
        pass
    else:
        return "Choice not understood; please try again."
        
def configDetails(conman):
    print conman.cp.sections(),"\n"
    choiceOptionInquiry=raw_input("\nWhich section would you like? (Hit enter for all.)\n>\t")
    return conman.cp.getConfigObj(choiceOptionInquiry)

if __name__=='__main__':
    choices=["geneGO","ND"]
    main()
