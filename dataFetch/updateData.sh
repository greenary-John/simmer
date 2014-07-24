#!/bin/bash

# quick script to use curl to refresh OBO files and GO GAF file
#  and get MPannotations from MouseMine

baseDataDir=../Data

ontDir=${baseDataDir}/ontologies
annDir=${baseDataDir}/annotations

# backup existing ontDir and annDir into an archive directory
curTime=`date +"%Y-%m-%d:%H:%M"`
archiveDir=$baseDataDir/archive.$curTime
mkdir $archiveDir
cp -pR $ontDir $annDir $archiveDir

MGIftpSite="ftp://ftp.informatics.jax.org"
GOoboFile="http://www.geneontology.org/ontology/obo_format_1_0/gene_ontology.1_0.obo"
curl $MGIftpSite/pub/reports/MPheno_OBO.ontology >$ontDir/MPheno_OBO.obo
curl $MGIftpSite/pub/reports/gene_association.mgi >$annDir/gene_association.mgi
curl $GOoboFile > $ontDir/gene_ontology.obo

python getMPannotations.py > $annDir/MPannot.txt
