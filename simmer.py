import os
import ConfigParser
#import optparse

from icLib import Ontology
from icLib import DAG
from icLib import Config_Manager
from icLib import Extended_Closure

def main():
    conman=Config_Manager.Config_Manager()
    #rclos=Extended_Closure.ReverseClosure()
    #fclos=Extended_Closure.ForwardClosure()
    ontologies=conman.getOntologies()
    annotations=conman.getAnnotations()
    rclosure=Extended_Closure.ReverseClosure().multigo(ontologies[1])
    fclosure=Extended_Closure.ForwardClosure().multigo(ontologies[1])


    #above this comment is mostly algorithmic
    #below this comment is mostly printing to validate variables and output

    print "Data Dir:\t",conman.getDataDir()
    print "Ont Dir:\t",conman.getOntDir()
    print "Ann Dir:\t",conman.getAnnDir(),"\n"
    
    #formatted printing of ontology namespaces and annotation subsets, respectively
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

main()
