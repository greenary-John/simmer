

class Annotation_Manager(object):

    def __init__(self):
        pass

    def annload(self,filedescript):
        return [filedescript[0],open(filedescript[1],'r').read().split()]

    def annsload(self,filedescripts):
        anns=[]
        types=[]
        for filedescript in filedescripts:
            anns.append(open(filedescript[1],'r').read().splitlines())
            types.append(filedescript[0])
        for x in range (0,len(anns)):
            for y in range (0,len(anns[x])):
                if "\t" in anns[x][y]:
                    anns[x][y]=anns[x][y].split("\t")
            #relevant range for GO and MP split annotations, respectively, are [6:] and [1:]
            if types[x]=="GO":
                anns[x]=anns[x][6:]
            if types[x]=="MP":
                anns[x]=anns[x][1:]
        return [types,anns]
        
            
