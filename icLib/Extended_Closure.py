import DAG
import Ontology

class ReverseClosure(DAG.Traversal):
    #note this does not work for has_part relations
    #conjecture: this only works for is_a and part_of relations
    def __init__(self,nodeSelector=lambda n:True):
        self.closure = {}
	self.nodeSelector = nodeSelector
    def beforeNode(self,dag,node,path):
	self.closure[node] = set([node])
    def afterEdge(self,dag,p,c,d,path):
        for term in self.closure[p]:
            self.closure[c]|=set([term])
    def getResults(self):
        return self.closure
    def go_(self,ont):
        return self.go(ont,None,True)
    def multigo(self,onts):
        ret=[]
        for x in onts:
            ret.append(self.go_(x))
        return ret

    
class ForwardClosure(DAG.Traversal):
    def __init__(self,nodeSelector=lambda n:True):
        self.closure = {}
	self.nodeSelector = nodeSelector
    def beforeNode(self,dag,node,path):
        s = set()
	if self.nodeSelector(node):
	    s.add(node)
	self.closure[node] = s
    def afterEdge(self,dag,p,c,d,path):
        if self.reversed:
	    self.closure[c] |= self.closure[p]
	else:
	    self.closure[p] |= self.closure[c]
    def getResults(self):
        return self.closure
    def multigo(self,onts):
        ret=[]
        for x in onts:
            ret.append(self.go(x))
        return ret
