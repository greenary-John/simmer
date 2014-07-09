def AnnotationSetEvidenceFilter(AnnSet,evCodes):
    #input of annotation set and desired evidence codes to REMOVE
    annotationsByID=AnnSet.annotations["ID"]
    annotationsByObj=AnnSet.annotations["Obj"]
    for evCode in evCodes:
        try:
            annotationsbyID={key:value for key,value in annnotationsByID.items() if value[1]["EvidenceCode"]!=evCode}
            annotationsbyObj={key:value for key,value in annnotationsByObj.items() if value[1]["EvidenceCode"]!=evCode}
        except KeyError:
            annotationsbyID={key:value for key,value in annnotationsByID.items() if value[1]["Evidence"]!=evCode}
            annotationsbyObj={key:value for key,value in annnotationsByObj.items() if value[1]["Evidence"]!=evCode}
    AnnSet.annotations={"ID":annotationsByID,"Obj":annotationsByObj}
