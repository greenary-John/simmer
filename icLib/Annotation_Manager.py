

class Annotation_Manager(object):

    def __init__(self):
        pass

    def annload(self,filedescript):
        return open(filedescript[1],'r').read().split()

    def annsload(self,filedescripts):
        anns=[]
        for filedescript in filedescripts:
            anns.append(open(filedescript[1],'r').read().split())
        return anns
        
            
