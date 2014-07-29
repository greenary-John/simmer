'''simmerEngine
This is the search engine to which the three different implementations feed
requests. This is the consolidated search engine and will hold the bulk, if not
all, computation instead of the three drivers.

Author: Patrick Osterhaus   s-osterh
'''
import sys
import os
import ConfigParser
import json

from icLib import Ontology
from icLib import DAG
from icLib import ConfigManager
from icLib import OntologyManager
from icLib import AnnotationManager
from icLib import CompiledAnnotationSet
from icLib import AnnotatedObject
from icLib import Logger
from icLib import Labeler

#NOTE:It is much better in REPL to use requestSubmissionPC so that each query
#does not require a new Pre-Computation I step
def requestSubmissionPC(annSetChoice,evCodesChoice,searchType,searchInput,namespaceChoice,methodChoice,length,logger,labeler,ontman,annman,jason="False"):
    #annSetChoice   =   string specifying desired AnnSet (e.g., 'geneGO' or 'genotypeMP')
    #evCodesChoice  =   string specifying desired evCodes to remove (e.g., 'ND,ISO,ISS')
    if searchType not in ["object","list"]:
        print "Problem with parameter 3."
    if methodChoice not in ["resnikBMA","jaccardExt","gicExt"]:
        print "Problem with parameter 6."
    if not isinstance(length,int):
        print "Problem with parameter 7."
    if annSetChoice not in annman.annotationSets:
        print "Problem with parameter 1."
    annset=annman.annotationSets[annSetChoice]
    evCodes=list(set(evCodesChoice.split(",")))
    cas=CompiledAnnotationSet.CompiledAnnotationSet.getCAS(annset,evCodes,ontman)
    if searchType=="object":
        query=AnnotatedObject.AnnotatedObject.getAnnotatedObj(searchInput)
    if searchType=="list":
        query=[cas.annset.ontology.getTerm(x)for x in searchInput.replace(" ,",",").replace(" ",",").split(",")]
    if methodChoice=="resnikBMA":
        ret=cas.resnikBMA(searchType,query,namespaceChoice,length)
    if methodChoice=="jaccardExt":
        ret=cas.jaccardExt(searchType,query,namespaceChoice,length)
    if methodChoice=="gicExt":
        ret=cas.gicExt(searchType,query,namespaceChoice,length)
    if jason!="False":
        retH=[{x.id:ret[x]} for x in ret]
        retI=dict(sum([x.items()for x in retH],[]))
        retJ={"params":{"annSetChoice":annSetChoice,
                        "evCodesChoice":evCodesChoice,
                        "searchType":searchType,
                        "searchInput":searchInput,
                        "namespaceChoice":namespaceChoice,
                        "methodChoice":methodChoice,
                        "length":length},
              "results":retI}
        return json.dumps(retJ)
    else:return ret

def requestSubmissionRaw(annSetChoice,evCodesChoice,searchType,searchInput,namespaceChoice,methodChoice,length,jason=False):
    #annSetChoice   =   string specifying desired AnnSet (e.g., 'geneGO' or 'genotypeMP')
    #evCodesChoice  =   string specifying desired evCodes to remove (e.g., 'ND,ISO,ISS')
    if searchType not in ["object","list"]:
        print "Problem with parameter 3."
    if methodChoice not in ["resnikBMA","jaccardExt","gicExt"]:
        print "Problem with parameter 6."
    if not isinstance(length,int):
        print "Problem with parameter 7."
    print "Pre-Computation I..."
    logger=Logger.Logger()
    cm=ConfigManager.ConfigManager(setConfigOptions)
    simmercon=cm.readConfig()
    #readConfig() returns a SimmerConfigParser so simmercon is a SimmerConfigParser
    labeler=Labeler.Labeler(simmercon)
    ontman=OntologyManager.OntologyManager(simmercon)
    annman=AnnotationManager.AnnotationManager(simmercon,ontman)
    if annSetChoice not in annman.annotationSets:
        print "Problem with parameter 1."

    annset=annman.annotationSets[annSetChoice]
    evCodes=list(set(evCodesChoice.split(",")))
    cas=CompiledAnnotationSet.CompiledAnnotationSet.getCAS(annset,evCodes,ontman)
    if searchType=="object":
        query=AnnotatedObject.AnnotatedObject.getAnnotatedObj(searchInput)
    if searchType=="list":
        query=[cas.annset.ontology.getTerm(x)for x in searchInput.replace(" ,",",").replace(" ",",").split(",")]
    if methodChoice=="resnikBMA":
        ret=cas.resnikBMA(searchType,query,namespaceChoice,length)
    if methodChoice=="jaccardExt":
        ret=cas.jaccardExt(searchType,query,namespaceChoice,length)
    if methodChoice=="gicExt":
        ret=cas.gicExt(searchType,query,namespaceChoice,length)
    if jason!="False":
        retH=[{x.id:ret[x]} for x in ret]
        retI=dict(sum([x.items()for x in retH],[]))
        retJ={"params":{"annSetChoice":annSetChoice,
                        "evCodesChoice":evCodesChoice,
                        "searchType":searchType,
                        "searchInput":searchInput,
                        "namespaceChoice":namespaceChoice,
                        "methodChoice":methodChoice,
                        "length":length},
              "results":retI}
        return json.dumps(retJ)
    else:return ret

def setConfigOptions(op):
    op.add_option("-l", "--length", metavar="NUM", dest="n", type="int", help="A number.")
