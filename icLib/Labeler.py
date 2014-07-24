
import json
import urllib

class Labeler:
    def __init__(self, cp):
        self.cp = cp
	self.lcache = {}

    def resetCache(self):
        self.lcache = {}

    def get(self, typ, oid):
	k = typ+' '+oid
	lbl = self.lcache.get(k,None)
	if lbl:
	    return lbl
	try:
	    sec = 'query.'+typ
	    if not self.cp.has_section(sec):
		return oid
	    mmurl = self.cp.get(sec,'url')
	    mmq  = self.cp.get(sec, 'query', False, {'id':oid})
	    url = mmurl + urllib.quote(mmq)
	    fd = urllib.urlopen(url)
	    r=fd.read()
	    fd.close()
	    r = json.loads(r)["results"]
	    if len(r) == 0:
		lbl = oid
	    if self.cp.has_option(sec,'format'):
		lbl = self.cp.get(sec,'format',False,r[0])
	    else:
		lbl = r[0]
	except:
	    lbl = oid;
	self.lcache[k] = lbl
	return lbl

if __name__ == "__main__":
    # self test
    import sys
    import ConfigParser
    cp = ConfigParser.ConfigParser()
    cp.read(sys.argv[1])
    l = Labeler(cp)
    print l.get('gene','MGI:96677')
    print l.get('genotype','MGI:3613478')
