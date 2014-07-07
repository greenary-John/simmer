

class Annotation_Manager(object):

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
        
            
