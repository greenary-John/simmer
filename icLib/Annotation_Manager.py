import Annotated_Set

class Annotation_Manager(object):

    '''
    #__init__ below will probably be replaced by __init__ in progress below it
    def __init__(self,conMan):
        self.annObjs={}
        typesTemp=[]
        annsTemp=[]
        self.anns={}
        for sec in conMan.sectionsWith("type","annotations"):
            self.annObjs[sec]=conMan.getConfigObj(sec)
        for obj in self.annObjs:
            annsTemp.append(open(self.annObjs[obj]["filename"],'r').read().splitlines())
            typesTemp.append(obj)
        for x in range(0,len(annsTemp)):
            for y in range (0,len(annsTemp[x])):
                if "\t" in annsTemp[x][y]:
                    #reformaat anns such that each element is a list separated by tabs
                    annsTemp[x][y]=annsTemp[x][y].split("\t")
            if typesTemp[x]=="geneGO":
                self.anns[typesTemp[x]]=annsTemp[x][6:]
            if typesTemp[x]=="geneMP":
                self.anns[typesTemp[x]]=annsTemp[x][1:]
    '''


    
    
    def __init__(self,simConPar,ontMan):
        self.configDetails={}
        annotationNames=[]
        #annotationNames correspond to section names in config file
        rawAnns=[]
        #rawAnns are annotaion sets in the most raw form
        #this is a multidimensional list; first layer: annotation set,
        #second layer: line, third layer (not always present): tab/column
        self.annotationSets={}
        for sec in simConPar.sectionsWith("type","annotations"):
            self.configDetails[sec]=simConPar.getConfigObj(sec)
        for detail in self.configDetails:
            rawAnns.append(open(self.configDetails[detail]["filename"],'r').read().splitlines())
            annotationNames.append(detail)
        #note that this next loop is preferable because above loop iterates through
        #a dictionary while loop below iterates through a multi-dimensional list and needs indices

        parse(rawAnns,annotationNames,self.annotationSets,simConPar,ontMan)
    

    '''
        #old
        #create AnnotatedSet objects for each annotaion set
    `   #replace below statements with tentative "parse" function on board
        for x in range(0,len(rawAnns)):
            self.annotationSets[annotationNames[x]]=AnnotatedSet(annotationNames[x],ontMan)
            
            
        
        #iterate through each annotation set
        for x in range (0,len(rawAnns)):
            #create AnnotatedSet object for each annotation set
            self.annotationSets[annotationNames[x]]=AnnotatedSet(annotationNames[x],ontMan)
            #iterate through each line
            for y in range (0,len(rawAnns[x])):
                #must perform check in case of headers and inconsistent format
                if "\t" in rawAnns[x][y]:
                    #reformat rawAnns such that each element of depth 2 is a list separated by tabs
                    rawAnns[x][y]=rawAnns[x][y].split("\t")

        #now, how do I parse header information to find correct inputs for annID, ontID
        #termID, and details parameters of AnnotatedSet.addAnnotation method?
    '''
def parse(rawAnnotations,annNames,annSets,simConPar,ontMan):
        for x in range(0,len(rawAnnotations)):
            annSets[annNames[x]]=Annotated_Set.AnnotatedSet(annNames[x],ontMan,simConPar)
            form=simConPar.getConfigObj(annNames[x])["format"]
            if form=="MP TSV":
                for y in range(1,len(rawAnnotations[x])):
                    add_MP_TSV_Annotation(annSets[annNames[x]],rawAnnotations[x][y])
            if form=="gaf-version: 2.0":
                for y in range(6,len(rawAnnotations[x])):
                    add_gaf_Annotation(annSets[annNames[x]],rawAnnotations[x][y])

def add_MP_TSV_Annotation(annSet,annLine):
    try:
        columns=annLine.split("\t")
        annID=columns[0]
        #2014 annID is columns[3]
        ontID="MP"
        termID=columns[3]
        #2014 termID is columns[0]
        details={
             '''"TermName":columns[1],
             "OntologyNamespace":columns[2],
             "SubjectName":columns[4],
             "Qualifier":columns[5],
             "EvidenceCode":columns[6],
             "JNumber":columns[7]'''
             #above is for 2014 version
             #below is for 2013 version
             "Genotype":columns[1],
             "Evidence":columns[2],
             "MPTerm":columns[4],
             "Qualifier":columns[5]
                 }
        if details["Qualifier"]!="normal":
            annSet.addAnnotation(annID,ontID,termID,details)
    except Exception as e:
        print type(e)
        print "\nError near:\t",annID
        #pass
    
    
def add_gaf_Annotation(annSet,annLine):
    try:
        columns=annLine.split("\t")
        annID=columns[1]
        ontID="GO"
        termID=columns[4]
        details={"DB":columns[0],
             "DBObjectSymbol":columns[2],
             "Qualifier":columns[3],
             "DBReference":columns[5],
             "EvidenceCode":columns[6],
             "With (or) From":columns[7],
             "Aspect":columns[8],
             "DBObjectName":columns[9],
             "DBObjectSynonym":columns[10],
             "DBObjectType":columns[11],
             "Taxon":columns[12],
             "Date":columns[13],
             "AssignedBy":columns[14],
             "AnnotationExtension":columns[15],
             "GeneProductFormID":columns[16]}
        if details["Qualifier"]=="None" or details["Qualifier"]=="":
            annSet.addAnnotation(annID,ontID,termID,details)
    except:
        print "Error on:\t",annID

    
