'''
Created on Jun 11, 2013

@author: s-galvez
@author: Joel Richardson. Slightly modified (directories). Jun 5 2014
@author: Pat Osterhaus. Edited for command line args.

Example Input with Command Line Arguments:
python main.py -o 2 -e None -f data\MPannot-2013-07-16.txt -d data\Geno_11_OMIM.txt -l 25
python main.py -o 0 -e None -f data\gene_association.mgi -l 25
'''
import sys
import os.path
import subprocess
import optparse

from icLib import AnnotationSet
from icLib import ObjectSimilarity
from icLib import Term
from icLib import DAG
from icLib import Ontology
from icLib import MyClosure
from icLib import ReactionPathway
from icLib import DAGPrinter
from icLib import AnnotatedObject

myDir = os.path.dirname(__file__)

def main():
    options=optionParser()
    ontoChoice=options.ontoChoice
    evidenceCodeStrings=options.evidenceCodeStrings
    evidenceCodeStrings.replace(" ","").replace("None","")
    evidenceCodes=evidenceCodeStrings.split(",")
    fileName=options.fileName
    diseaseFile=options.diseaseFile
    length=options.length
    if ontoChoice == "0":
        ontology = Ontology.load(os.path.join(myDir,"data","gene_ontology.obo"), nodeType = Term.Term, cullObsolete = True)        
        annotationSet = AnnotationSet.AnnotationSet(fileName, ontology, evidenceCodes)
        #pathwayDict = readReactome("NCBI_Reactome_MGI.txt")
    else:
        ontology = Ontology.load(os.path.join(myDir,"data","MPheno_OBO.obo"), nodeType = Term.Term, cullObsolete = True)
        annotationSet = AnnotationSet.MPAnnotationSet(fileName, ontology, diseaseFile, evidenceCodes)        
    c = MyClosure.ForwardClosure(annotationSet, ontology).go(ontology)#Compute descendants.
    c_rev = MyClosure.ReverseClosure(annotationSet).go(ontology, reversed = True)#, allPaths = True) #Compute ancestors.
    countDict = {"C": 0, "F": 0, "P": 0}
    
    more = "y"
    while(more == "y"):
        if ontoChoice == "0":
            #objectID = raw_input("What gene would you like to compare? Enter MGI ID: ")
            object_IDs = ["MGI:94909", "MGI:87961","MGI:88057", "MGI:1859546","MGI:96840"]
            roots = ["F","C","P"]
        else:
            #objectID = raw_input("What genotype would you like to compare? Enter MGI ID: ")
            object_IDs = ["MGI:3526657"]
            roots = ["MP"]
        icChoice = "0"
        if icChoice == "0":
            icType = "annotations"
        else:
            icType = "descendants"
        #length = 25
        
        for root in roots:
            for object_ID in object_IDs:
                comparisonObject = annotationSet.annotatedObjects[object_ID]
                orderings = createSimilarityMatrix(annotationSet,comparisonObject, root, evidenceCodes, icType)
                comparisonData = compareMethodsSameObject(comparisonObject, orderings,length)
                comparisonData2 = compareMethodsSameObject(comparisonObject, orderings,(length*2)//5)
                printToFile(comparisonObject, orderings, length, root, evidenceCodes, icType,annotationSet,ontology, comparisonData, comparisonData2)#, pathwayDict)
        #pr.print_stats()
        #pr.disable()
        return
        if ontoChoice == "0":
            more = raw_input("Obtain metrics for another gene? y to continue. anything else to stop.")
        else:
            more = raw_input("Obtain metrics for another genotype? y to continue. anything else to stop.")
        
        #Code used to query for certain fake genes with chosen annotations:
        '''
        fakeID = "MGI:0000000000"
        #annotationStrings =["", fakeID, "", "", ]
        stompedOverUnpythonicAnnotations = annotationSet.annotations #Sets are annoying. Popping removes that element :( Implemented fake gene creation after 
        if ontoChoice == "0":
            #P-value less than 10^-5 in Vlad:
            annotationDict = {'P': {}, 'C':{}, 'F':{}}
            processEnrichedTerms = ['GO:0043113','GO:0007528','GO:0048741','GO:2000541','GO:0045887',
                                    'GO:2000539','GO:0048747','GO:0050808','GO:0072657','GO:0008582',
                                    'GO:0055002','GO:0055001','GO:0007519','GO:0060538','GO:0051146',
                                    'GO:0007517','GO:0042692','GO:0014706','GO:0016044','GO:0061024',
                                    'GO:0051965','GO:0051962','GO:0044089','GO:0061061','GO:0051963',
                                    'GO:0001934','GO:0042327']
            for term in processEnrichedTerms:
                annotationDict["P"][term] = stompedOverUnpythonicAnnotations[term].pop()
            annotationDict["C"] = {}
            annotationDict["F"] = {} 
            comparisonObject = AnnotatedObject.AnnotatedObject(fakeID, "dummy", "gene_association.mgi",annotationDict["C"], annotationDict["F"], annotationDict["P"])
            
        else:
            #annotationDict = {#"MP:0000001": stompedOverUnpythonicAnnotations["MP:0000001"].pop()#, "MP:0003631": stompedOverUnpythonicAnnotations["MP:0003631"].pop(),"MP:0005385": stompedOverUnpythonicAnnotations["MP:0005385"].pop(),
            #                  #"MP:0001764": stompedOverUnpythonicAnnotations["MP:0001764"].pop(),"MP:0005376": stompedOverUnpythonicAnnotations["MP:0005376"].pop(),"MP:0003632": stompedOverUnpythonicAnnotations["MP:0003632"].pop(),
            #                  "MP:0005387": stompedOverUnpythonicAnnotations["MP:0005387"].pop()}
            annotationDict = {"MP:0006035": stompedOverUnpythonicAnnotations["MP:0006035"].pop()}
            comparisonObject = AnnotatedObject.AnnotatedObject(fakeID, "dummy", "MPanot-2013-07-16.txt",annotationDict)
        for root in roots:
            orderings = createSimilarityMatrix(annotationSet,comparisonObject, root, evidenceCodes, icType)
            comparisonData = compareMethodsSameObject(comparisonObject, orderings,25)
            printToFile(comparisonObject, orderings, length, root, evidenceCodes, icType,annotationSet,ontology, comparisonData, comparisonData)
        return
        '''
        
        
def compareMethodsSameObject(comparisonObject, orderings, length):
    comparisons = {}
    for method1 in comparisonObject.methodStrings:
        comparisonOrdering = orderings[method1]
        for method2 in comparisonObject.methodStrings:
            secondOrdering = orderings[method2]
            if method1 == method2:
                comparisons[(method1,method2)] = 1.0*length/length
            else:
                count = 0
                for objectTuple1 in orderings[method1][0:length]:
                    for objectTuple2 in orderings[method2][0:length]:
                        #print objectTuple1[0], objectTuple2[0]
                        if objectTuple1[0] == objectTuple2[0]:
                            count += 1
                comparisons[(method1, method2)] = 1.0*count/length
                #comparisons[(method2, method1)] = 1.0*count/25 
    return comparisons
def printDiseaseResults(object1, orderings, annotationSet, length):
#Return number of genotypes all annnotated to the same disease
    returnString = object1.object_ID + " " + object1.disease
    for orderingName in orderings.keys():
        i = 0
        count = 0
        while i < length:
            if annotationSet.annotatedObjects[orderings[orderingName][i][0]].disease == object1.disease:
                count += 1
            i += 1
        returnString += "\t" + str(1.0*count/length)
    returnString += "\n"
    return returnString

#REturn distance in ranking between two objects according to two different rankings.
    
#Finds top length genes associated with input gene of interest.
def createSimilarityMatrix(annotationSet, object1, root, evidenceCodes, icType):
#Loops through all annotated objects and computes similarity scores with object1.
    simMeasures = {}
    
    jaccardSimilarity = ObjectSimilarity.JaccardSimilarity()
    simMeasures[object1.methodStrings[0]] = jaccardSimilarity
    jaccardExtSimilarity = ObjectSimilarity.JaccardSimilarityExtended()
    simMeasures[object1.methodStrings[1]] = jaccardExtSimilarity
    gicExtSimilarity = ObjectSimilarity.GICSimilarityExtended(icType)
    simMeasures[object1.methodStrings[2]] = gicExtSimilarity
    wangSimilarity = ObjectSimilarity.WangSimilarity()
    simMeasures[object1.methodStrings[3]] = wangSimilarity
    
    orderings = {}
    for measureName in object1.methodStrings:
        orderings[measureName] = []
    print "orderings declared"
    #count = 0
    #count = 0
    for key in annotationSet.annotatedObjects.keys():
        for methodName in object1.methodStrings:
            similarity = simMeasures[methodName].findSimilarity(object1, annotationSet.annotatedObjects[key], root)
            orderings[methodName].append((key, similarity, annotationSet.annotatedObjects[key].symbol)) #Appending a tuple here: current object's id, similarity value between object1 and current object, and current object's symbol.
        #count += 1
        #if count  == 20:
            #pr.print_stats
        #    return
        #print 1.0*count/len(annotationSet.annotatedObjects.keys())
    print "out of loop"
    for key in orderings:
        orderings[key].sort(key=lambda x: x[1], reverse = True)
    print "Done sorting"
    
    
    return orderings
    
def printToFile(object1, #the annotated object to which all other objects were compared.
                orderings, #A dict mapping methodStrings in the Annotated Object class to ranked lists of similar genes' tuples (their id, similarity, and symbol) according to the measures described by the strings
                length, #the first length genes are output from orderings (where smallest index corresponds to most similar object).
                root, #"F", "P", or "C" corresponding to one of the three ontologies in the GO. MP has root "MP".
                evidenceCodes, #Evidence codes removed during query.
                icType, 
                annotationSet, 
                ontology,
                comparisonData,
                comparisonData2):
    #Creates tab-delimited file for upload to excel or other program.
    modifier = root
    if root == "MP":
        fileName = object1.object_ID.replace("MGI:","") + "_" + modifier + ".txt"
    else:
        fileName = object1.symbol + "_" + modifier + ".txt"
    codeStr = ""
    for code in evidenceCodes: codeStr += code
    if codeStr == "":
        codeStr = "None"
    if root == "MP":
        dir = os.path.join(myDir,"output",object1.object_ID.replace("MGI:","") + "_" + root + "_" + icType + "IC_" + codeStr +"Removed")
    else:
        dir = os.path.join(myDir,"output",object1.symbol + "_" + icType + "IC_" + codeStr + "Removed",  object1.symbol + "_" + root + "_" + icType + "IC_" + codeStr + "Removed")
    if not os.path.exists(dir):
        os.makedirs(dir)
    print dir
    completeName = os.path.join(dir,fileName)
    print fileName
    print completeName
    #completeName = os.path.join(, fileName)
    fp = open(completeName,'w')
    i = 0
    no_measurements = len(orderings)
    removedCodes = ""
    for code in evidenceCodes:
        removedCodes += code + "\t"
    fp.write(object1.object_ID + "\t" + object1.symbol + "\t" + root +"\t" + "Following codes removed: " + removedCodes + "\t\t" + "\n")
    measurementTypeLine = ""
    for key in object1.methodStrings:
        if root == "MP":
            measurementTypeLine += key + "\t\t\t\t\t\t\t\t\t"
        else:
            measurementTypeLine += key + "\t\t\t\t\t\t\t"
    measurementTypeLine += "\n"
    fp.write(measurementTypeLine)
    header = ""
    if root =="P" or root == "F" or root == "C":
        header += no_measurements*"Rank\tSymbol\tMGI ID\tscore\tNumber of Annotations\tOntology\tColon-Addressed Ontology\t" + "\n"
    else:
        header += no_measurements*"Rank\tSymbol\tMGI ID\tscore\tNumber of Annotations\tDisease\tSameDisease\tOntology\tColon-Addressed Ontology\t" + "\n"

        
    fp.write(header)
    
    
    #---------------------
    
    rankDict = {}
    for methodName in object1.methodStrings:
        rankDict[methodName] = 1
    firstTime = True
    '''
    allRanksExceded = False
    while not allRanksExceded: 
        line = ""
        start = True
        for methodName in object1.methodStrings:
            if not firstTime and not orderings[methodName][i][1] == orderings[methodName][i-1][1]:
                rankDict[methodName] += 1
            line += (str(rankDict[methodName]) + "\t" + orderings[methodName][i][2] + "\t" + orderings[methodName][i][0] + "\t" + str(orderings[methodName][i][1]) + "\t")
            
            if i == length and orderings[methodName][i][1] == orderings[methodName][i+1][1] and start:
                i = i - 1
                start = False
        line += "\n"
        fp.write(line)
        firstTime = False
        i = i + 1
        allRanksExceded = True
        for method in rankDict.keys():
            if rankDict[method] < length:
                allRanksExceded = False
                break
    '''
                
    while i < length:
        line = ""
        start = True
        for methodName in object1.methodStrings:
            #print object1.object_ID            
            if not firstTime and not orderings[methodName][i][1] == orderings[methodName][i-1][1]:
                rankDict[methodName] += 1
            if root == "MP":
                ontologyPath = "LEFT(CELL(\"filename\"),LEN(CELL(\"filename\"))-" + str(len(fileName) + 1) + ")" + "&\"" +"\\" + methodName + "\\" + object1.object_ID.replace("MGI:", "") + "_" + orderings[methodName][i][0].replace("MGI:","") + "_" + methodName + "_" + root + ".png\""
                secondOntologyPath = "LEFT(CELL(\"filename\"),LEN(CELL(\"filename\"))-" + str(len(fileName) + 1) + ")" + "&\"" +":" + methodName + ":" + object1.object_ID.replace("MGI:", "") + "_" + orderings[methodName][i][0].replace("MGI:","") + "_" + methodName + "_" + root + ".png\""
            else:
                ontologyPath =  "LEFT(CELL(\"filename\"),LEN(CELL(\"filename\"))-" + str(len(fileName) + 1) + ")" + "&\"" +"\\" + methodName + "\\" + object1.symbol + "_" + orderings[methodName][i][2] + "_" + methodName + "_" + root + ".png\""
                secondOntologyPath =  "LEFT(CELL(\"filename\"),LEN(CELL(\"filename\"))-" + str(len(fileName) + 1) + ")" + "&\"" +":" + methodName + ":" + object1.symbol + "_" + orderings[methodName][i][2] + "_" + methodName + "_" + root + ".png\""
            if root == "MP":
                line += (str(rankDict[methodName]) + "\t" + orderings[methodName][i][2] + "\t" + orderings[methodName][i][0] + "\t" + str(orderings[methodName][i][1]) + "\t" + str(len(annotationSet.annotatedObjects[orderings[methodName][i][0]].annotationDict[root])) + "\t" + annotationSet.annotatedObjects[orderings[methodName][i][0]].disease + "\t" + str(annotationSet.annotatedObjects[orderings[methodName][i][0]].disease == object1.disease) + "\t" + "=HYPERLINK(" + ontologyPath + "," + "\"" + object1.object_ID + " and " + orderings[methodName][i][0] + "\"" + ")" + "\t" + "=HYPERLINK(" + secondOntologyPath + "," + "\"" + object1.object_ID + " and " + orderings[methodName][i][0] + "\"" + ")"  + "\t")

            else:
                line += (str(rankDict[methodName]) + "\t" + orderings[methodName][i][2] + "\t" + orderings[methodName][i][0] + "\t" + str(orderings[methodName][i][1]) + "\t" + str(len(annotationSet.annotatedObjects[orderings[methodName][i][0]].annotationDict[root])) + "\t" + "=HYPERLINK(" + ontologyPath + "," + "\"" + object1.symbol + " and " + orderings[methodName][i][2] + "\"" + ")" + "\t" + "=HYPERLINK(" + secondOntologyPath + "," + "\"" + object1.symbol + " and " + orderings[methodName][i][2] + "\"" + ")"  + "\t")
            #print object1.object_ID
            if i == length and orderings[methodName][i][1] == orderings[methodName][i+1][1] and start:
                i = i - 1
                start = False
        line += "\n"
        fp.write(line)
        firstTime = False
        i = i + 1     
        
        #if i == length:
            #for method in orderings.keys():
                #print method
                #print orderings[method][i][1]
                #print orderings[method][i+1][1]
                #if orderings[method][i+1] != 0.0 and orderings[method][i+1][1] == orderings[method][i][1]:
                #    length += 1
    line = ""    
    line += "\t"
    
    for method in object1.methodStrings:
        line += method + "\t"
    line += "\n"                
    for method1 in object1.methodStrings:
        line += method1 +"\t"
        for method2 in object1.methodStrings:
            try:
                line += str(comparisonData[(method1, method2)]) + "\t"
            except:
                line += "0\t" 
        line += "\n"
    fp.write(line)

    line = ""    
    line += "\t"
    
    for method in object1.methodStrings:
        line += method + "\t"
    line += "\n"                
    for method1 in object1.methodStrings:
        line += method1 +"\t"
        for method2 in object1.methodStrings:
            try:
                line += str(comparisonData2[(method1, method2)]) + "\t"
            except:
                line += "0\t" 
        line += "\n"
    fp.write(line)
    
    fp.close()
    print "Created file called " + fileName
    
    dp = DAGPrinter.DAGPrinter()
    for method in object1.methodStrings:
        i = 0
        dir2 = dir
        path = os.path.join(dir2, method)
        print "path", path
        if not os.path.exists(path):
            os.makedirs(path)
        while i < length:
            textFile = dp.outputGraph(object1, annotationSet.annotatedObjects[orderings[method][i][0]], root, icType, ontology, annotationSet)
            fileName = "testing.dot"
            fp = open(fileName,'w')
            fp.write(textFile)
            fp.close()
            #print textFile
            if root == "MP":
                subprocess.call(['dot', '-Tpng', fileName, '-o', os.path.join(path,object1.object_ID.replace("MGI:", "") + "_" + orderings[method][i][0].replace("MGI:","") + "_" + method + "_" + root + '.png')])
            else:
                subprocess.call(['dot', '-Tpng', fileName, '-o', os.path.join(path,object1.symbol + "_" + orderings[method][i][2] + "_" + method + "_" + root + '.png')])
            i += 1
    
            
        
def readReactome(file): 
#Inputs the contents of NCBI_Reactome_MGI.txt
#Returns dict mapping MGI ID to pathways id's protein is involved in.
    reactions = {}
    fp = open(file,'r')
    lines = fp.readlines()
    i = 0
    for line in lines:
        line_data = line.split("\t")
        try:
            reactions[line_data[1]].append((line_data[2], line_data[3].replace("\n","")))
        except KeyError:
            reactions[line_data[1]] = []
            reactions[line_data[1]].append((line_data[2], line_data[3].replace("\n","")))
    #for reaction in reactions.keys():
    #    print reactions[reaction][0] + ", " + reactions[reaction][1]
    return reactions
    
def testMFBPResults():
    pass

def doInversions(list1, list2):
    pass
    #http://codereview.stackexchange.com/questions/12922/inversion-count-using-merge-sort

def compareDifferentMethodsLists(orderings, length):
#Find fraction of genes that are within the top length genes that two different genes have in common
    for method1 in orderings.keys():
        for method2 in orderings.keys():
            rankedList1 = orderings[method1]
            rankedList2 = orderings[method2]
            count  = 0
            i = 0
            while i < length:
                for geneTuple in rankedList2:
                    if rankedList1[i][2] == geneTuple[2]:
                        count += 1
                i += 1
            print method1, method2, 1.0*count/length
        
def findShallowObjects(ordering, annotationSet, length, root, method):
#Find the number of objects that are annotated only to the namespace in the top N similar objects for each method.
    #shallowObjects = {}
    #for method in orderings.keys():
    shallowObjects = {}
    index = 0
    while index < length:
        if len(annotationSet.annotatedObjects[ordering[index][0]].annotationDict[root]) == 1:
            for key in annotationSet.annotatedObjects[ordering[index][0]].annotationDict[root].keys():
                annotation = annotationSet.annotatedObjects[ordering[index][0]].annotationDict[root][key]
                if AnnotationSet.AnnotationSet.TERMS[annotation.term_ID].namespace == annotation.term_ID:
                    shallowObjects[annotation.term_ID] = annotationSet.annotatedObjects[ordering[index][0]]
        index += 1
    print method, 1.0*len(shallowObjects)/length 
    return shallowObjects
def findPoorlyAnnotatedObjects(ordering, threshold, annotationSet, length, root, method):
#Find the number of objects that are annotated only threshold times or less.
    poorlyAnnotatedObjects = {} #Dict where method name maps to dictionary mapping object ID to poorly annotated object.
    index = 0
    while index < length:
        if len(annotationSet.annotatedObjects[ordering[index][0]].annotationDict[root]) <= threshold:
            poorlyAnnotatedObjects[ordering[index][0]] = annotationSet.annotatedObjects[ordering[index][0]]
            print annotationSet.annotatedObjects[ordering[index][0]].annotationDict[root]
        index += 1
    print method, 1.0*len(poorlyAnnotatedObjects)/length 
    return poorlyAnnotatedObjects

def findAvgMaxResnikMICAs(orderings, length, root):
    avgResOrdering = orderings['resnikAvg']
    maxResOrdering = orderings['resnikMax']
    
    i = 0
    while i < length:
        termList = []
        objectTuple = avgResOrdering[i]
        
        i +=1

def optionParser():
    parser=optparse.OptionParser()
    parser.add_option("-o","--ontology",dest="ontoChoice",default="0",help="Which ontology? 0 for GO, anything else for MP. (default=%default)")
    parser.add_option("-e","--evidence",dest="evidenceCodeStrings",default="None",help="What evidence codes would you like to remove? (Separate evidence codes by commas. Spaces can be used. Specify 'None' to not remove evidence codes. See http://www.geneontology.org/GO.evidence.shtml)(default=%default)")
    parser.add_option("-f","--file",dest="fileName",default="data\gene_association.mgi",help="Which gene or phenotype file would you like to use as input?(default=%default)")
    parser.add_option("-d","--diseasefile",dest="diseaseFile",default="data\Geno_11_OMIM.txt",help="For use with MP terms. Specify which file, containing OMIM data, is desired for input.(default=%default)")
    parser.add_option("-l","--length",type="int",dest="length",default=25,help="Select how many results (matches) are desired. Values will be rounded down to nearest integer of lesser value.(default=%default)")
    (options,args)=parser.parse_args()
    return options

if __name__ == '__main__':
    main()



