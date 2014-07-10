import AnnotationSet

class AnnotationManager(object):

    def __init__(self,simConPar,ontMan):
        self.simConPar=simConPar
        self.ontMan=ontMan
        self.configDetails={}
        self.annotationNames=[]
        #annotationNames correspond to section names in config file
        self.rawAnns=[]
        #rawAnns are annotaion sets in the most raw form
        #this is a multidimensional list; first layer: annotation set,
        #second layer: line, third layer (not always present): tab/column
        self.annotationSets={}
        for sec in simConPar.sectionsWith("type","annotations"):
            self.configDetails[sec]=simConPar.getConfigObj(sec)
        for detail in self.configDetails:
            with open(self.configDetails[detail]["filename"],'r') as f:
                self.rawAnns.append(f.read().splitlines())
            self.annotationNames.append(detail)
        parse(self.rawAnns,self.annotationNames,self.annotationSets,self.simConPar,self.ontMan)

    def getSet(self,name="None"):
        try:
            return self.annotationSets[name]
        except KeyError:
            try:
                with open(self.simConPar.getConfigObj(self.simConPar.sectionsWith("name",name)[0])["filename"],'r') as f:
                    self.rawAnns.append(f.read().splitlines())
                print self.simConPar.sectionsWith("name",name)
                self.annotationNames.append(self.simConPar.getConfigObj(self.simConPar.sectionsWith("name",name)[0])["name"])
                parse(self.rawAnns,self.annotationNames,self.annotationSets,self.simConPar,self.ontMan)
                return self.annotationSets[name]
            except IndexError:
                return self.annotationNames 

def parse(rawAnnotations,annNames,annSets,simConPar,ontMan):
    formatdict={"gaf-version: 2.0":[6,"GO",{
        "DB":0,
        "annID":1,
        "DBObjectSymbol":2,
        "Qualifier":3,
        "termID":4,
        "DBReference":5,
        "EvidenceCode":6,
        "With (or) From":7,
        "Ascpect":8,
        "DBObjectName":9,
        "DBObjectSynonym":10,
        "DBObjectType":11,
        "Taxon":12,
        "Date":13,
        "AssignedBy":14,
        "AnnotationExtension":15,
        "GeneProductFormID":16
        }],"MP TSV":[1,"MP",{
            "annID":0,
            "Genotype":1,
            "EvidenceCode":2,
            "termID":3,
            "MPTerm":4,
            "Qualifier":5
            }]}

    '''#2014 MP TSV version
    "termID":0,
    "TermName":1,
    "OntologyNamespace":2,
    "annID":3,
    "SubjectName":4,
    "Qualifier":5,
    "EvidenceCode":6,
    "JNumber":7'''
    #add conditionals to check if indices within rawAnnotations have already been
    #parsed into AnnotationSets to avoid unnecessary runtime
    for x in range(0,len(rawAnnotations)):
        annSets[annNames[x]]=AnnotationSet.AnnotationSet(annNames[x],ontMan,simConPar)
        form=simConPar.getConfigObj(annNames[x])["format"]
        for y in range(formatdict[form][0],len(rawAnnotations[x])):
            columns=rawAnnotations[x][y].split("\t")
            details={}
            for z in formatdict[form][2]:
                details[z]=columns[formatdict[form][2][z]]
            if details["Qualifier"]=="None" or details["Qualifier"]=="":
                annSets[annNames[x]].addAnnotation(formatdict[form][1],details)
