from flask import Flask
from flask import request
import os
import optparse
import ConfigParser
import json
import time

from icLib import Ontology
from icLib import DAG
from icLib import ConfigManager
from icLib import OntologyManager
from icLib import AnnotationManager
from icLib import CompiledAnnotationSet
from icLib import AnnotatedObject
from icLib import Logger
from icLib import Labeler
from icLib import SimmerEngine

app= Flask(__name__, static_url_path="")

#example input URL:
#http://localhost:5000/simmer?ecode=ND&annSet=geneGO&method=jaccardExt&qtype=object&qid=MGI:87961&length=25&nspace=biological_process
#http://localhost:5000/simmer?ecode=ND&annSet=genotypeMP&method=jaccardExt&qtype=object&qid=MGI:3526657&length=25&nspace=MPheno.ontology

@app.route('/simmer')
def simmer_engine():
    annSetChoice = request.values.get('annSet').split(",")[0]    
    searchType  = request.values.get('qtype')
    searchInput  = request.values.getlist('qid')
    if request.values.get('nspace')!=None:
        namespaceChoice = request.values.get('nspace')
    elif len(request.values.get('annSet').split(","))>=2:
        namespaceChoice=request.values.get('annSet').split(",")[1] 
    if namespaceChoice=="MPheno.ontology":
        evCodesChoice=""
    else:
        evCodesChoice = request.values.get('ecode')
    method = request.values.get('method')
    length = int(float(request.values.get('length')))#rounds down any floats entered to nearest int
    #return json.dumps([annSetChoice,str(evCodesChoice),searchType,searchInput,namespaceChoice,method,length])
    return SimmerEngine.requestSubmissionPC(annSetChoice,evCodesChoice,searchType,",".join([x for x in searchInput]),namespaceChoice,method,length,logger,labeler,ontman,annman,"html")

def setConfigOptions(op):
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")


if __name__=='__main__':
    print "Pre-Computation I..." 
    start=time.time()
    logger=Logger.Logger()
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    labeler=Labeler.Labeler(simmercon)
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    print time.time()-start
    CompiledAnnotationSet.CompiledAnnotationSet.getCAS(annman.annotationSets["geneGO"],"ND",ontman)
    CompiledAnnotationSet.CompiledAnnotationSet.getCAS(annman.annotationSets["geneGO"],"ND,ISS,ISA,ISO,ISM,IGC,IBA,IBD,IKR,IRD,RCA",ontman)
    CompiledAnnotationSet.CompiledAnnotationSet.getCAS(annman.annotationSets["genotypeMP"],"",ontman)
    app.run(debug=True,use_reloader=False)
