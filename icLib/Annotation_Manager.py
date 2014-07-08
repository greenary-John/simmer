import Annotated_Set

class Annotation_Manager(object):

    #__init__ below will probably be replaced by __init__ in progress below it
    def __init__(self,conMan,ontMan):
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
        #ontMan will be utilized in the implementation suggested by Joel (annSet and annObj approach)


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
            rawAnns.append(open(self.configDetails[obj]["filename"],'r').read().splitlines())
            annotationNames.append(detail)
        #note that this next loop is preferable because above loop iterates through
        #a dictionary while loop below iterates through a multi-dimensional list and needs indices

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
        



    def annsload(self,filedescripts):
        #fildescripts formatted as: [type_of_ann,filename_of_ann]
        anns=[]
        types=[]
        for filedescript in filedescripts:
            #store information, each line as an element, in anns
            anns.append(open(filedescript[1],'r').read().splitlines())
            types.append(filedescript[0])
        for x in range (0,len(anns)):
            for y in range (0,len(anns[x])):
                if "\t" in anns[x][y]:
                    #reformat anns such that each element is a list separated by tabs
                    anns[x][y]=anns[x][y].split("\t")
            #relevant range for GO and MP split annotations, respectively, are [6:] and [1:]
            #code below removes headers for generic GO and MP annotation files
            if types[x]=="GO":
                anns[x]=anns[x][6:]
            if types[x]=="MP":
                anns[x]=anns[x][1:]
        return [types,anns]
        
            
