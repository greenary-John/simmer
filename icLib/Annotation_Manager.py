

class Annotation_Manager(object):

    def __init__(self):
        pass

    def annload(self,filedescript):
        return [filedescript[0],open(filedescript[1],'r').read().split()]

    def annsload(self,filedescripts):
        anns=[]
        types=[]
        for filedescript in filedescripts:
            anns.append(open(filedescript[1],'r').read().split())
            types.append(filedescript[0])
        return [types,anns]
        
            
