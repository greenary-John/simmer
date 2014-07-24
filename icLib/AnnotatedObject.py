''' AnnotatedObject
The AnnotatedObject class contains a dictionary mapping identifiers
to defined objects. These objects are also created within the class
and simply contain the ID (e.g., 'MGI:1918911') of the object (gene
or mouse model) component of an annotation.

Author: Patrick Osterhaus   s-osterh
'''
class AnnotatedObject:
    knownObjs={}
    @classmethod
    def getAnnotatedObj(cls,iden):
        if iden in cls.knownObjs:
            return cls.knownObjs[iden]
        else:
            newObj=AnnotatedObject(iden)
            return newObj
    def __init__(self,iden):
        self.id=iden
        self.knownObjs[iden]=self
    def __str__(self):
        return self.id
    def getID(self):
        return self.id
        
