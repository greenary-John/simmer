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

app= Flask(__name__)

#example input URL:
#http://127.0.0.1:5000/?ecode=ND&annSet=geneGO&method=resnikBMA&qtype=object&qid=MGI:87961&length=25&nspace=biological_process

@app.route('/')
def hello_world():
    annSetChoice = request.values.get('annSet')
    evCodesChoice = request.values.getlist('ecode')
    searchType  = request.values.get('qtype')
    searchInput  = request.values.getlist('qid')
    namespaceChoice = request.values.get('nspace')
    method = request.values.get('method')
    length = int(float(request.values.get('length')))#rounds down any floats entered to nearest int
    #return json.dumps([annSetChoice,str(evCodesChoice),searchType,searchInput,namespaceChoice,method,length])
    return SimmerEngine.requestSubmissionPC(annSetChoice,",".join([x for x in evCodesChoice]),searchType,",".join([x for x in searchInput]),namespaceChoice,method,length,labeler,logger,ontman,annman,"True")

def setConfigOptions(op):
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")


if __name__=='__main__':
    start=time.time()
    print "Pre-Computation I..."
    logger=Logger.Logger()
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    labeler=Labeler.Labeler(simmercon)
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    simmercon,cm=None,None
    print time.time()-start
    app.run(debug=True,use_reloader=False)
