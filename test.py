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

@app.route('/')
def hello_world():

    return SimmerEngine.requestSubmissionPC("geneGO","ND","object","MGI:87961","biological_process","resnikBMA",25,labeler,logger,ontman,annman,"True")

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
    app.run(debug=True)
