class AnnotatedObject:
    global knownObjs
    knownObjs={}
    @classmethod
    def getAnnotatedObj(cls,iden):
        try:
            return knownObjs[iden]
        except KeyError:
            #print "No object found; creating one."
            newObj=AnnotatedObject(iden)
            return newObj
    def __init__(self,iden):
        self.id=iden
        knownObjs[iden]=self
    def __str__(self):
        return self.id
    def getID(self):
        return self.id
        
