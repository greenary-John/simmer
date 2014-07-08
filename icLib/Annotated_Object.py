class AnnotatedObject:
    knownObjs={}
    @classmethod
    def getAnnotatedObj(cls,iden):
        try:
            return knownObjs[iden]
        except KeyError:
            print "No object found; creating one."
            newObj=AnnotatedObject(iden)
            return newObj
    def __init__(self,iden):
        self.id=iden
        knownObjs[iden]=self
    def getID(self):
        return self.id
        
