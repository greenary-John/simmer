def AnnotationSetEvidenceFilter(AnnSet,evCodes):
    #input of annotation set and desired evidence codes to REMOVE
    for evCode in evCodes:
        try:
            AnnSet.annotations["ID"]={key:value for key,value in AnnSet.annotations["ID"].items() if value[1]["EvidenceCode"]!=evCode}
            AnnSet.annotations["Obj"]={key:value for key,value in AnnSet.annotations["Obj"].items() if value[1]["EvidenceCode"]!=evCode}
        except KeyError:
            AnnSet.annotations["ID"]={key:value for key,value in AnnSet.annotations["ID"].items() if value[1]["Evidence"]!=evCode}
            AnnSet.annotations["Obj"]={key:value for key,value in AnnSet.annotations["Obj"].items() if value[1]["Evidence"]!=evCode}
