def AnnotationSetEvidenceFilter(AnnSet,evCodes):
    #input of annotation set and desired evidence codes to REMOVE
    annotationsByID=AnnSet.annotations["ID"]
    annotationsByObj=AnnSet.annotations["Obj"]
    for evCode in evCodes:
        try:
            annotationsByID={key:value for key,value in annotationsByID.items() if value[1]["EvidenceCode"]!=evCode}
            annotationsByObj={key:value for key,value in annotationsByObj.items() if value[1]["EvidenceCode"]!=evCode}
        except KeyError:
            annotationsByID={key:value for key,value in annotationsByID.items() if value[1]["Evidence"]!=evCode}
            annotationsByObj={key:value for key,value in annotationsByObj.items() if value[1]["Evidence"]!=evCode}
    AnnSet.annotations={"ID":annotationsByID,"Obj":annotationsByObj}
