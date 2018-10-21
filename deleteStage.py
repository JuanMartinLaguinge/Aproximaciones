import classEtapa

def deleteStage(stageList):
    # a esta funcion le mandas la lista de etapas y agarra la sleccionada y la borra
    for k in range(len(stageList)):
        if(stageList[k].sel == True):
            a = k
    
    stageList.pop(a)
    return stageList