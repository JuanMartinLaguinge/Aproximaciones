import classEtapa

def shiftStage(stageList,direc):
    # esta funcion le pasas como parametros de entrada la lista de las etapas y
    # la direccion en la que queres shiftear
    # un elemento de la lista de etapas de estar seleccionado

    oldOrder = []
    newOrder = []
    for k in range(len(stageList)):
        oldOrder.append(k)                     #orden original de las etapas

    for k in range(len(stageList)):
        if(stageList[k].sel == True):        #agarramos la etapa que esta seleccionada

            if(direc == 'left'):             #queremos shiftear el elemento a la izquierda  
                if(k > 0):       
                    for q in range(k - 1):
                        newOrder.append(q)
                    newOrder.append(k)
                    newOrder.append(k-1)
                    for q in range(k+1 , len(stageList)):
                        newOrder.append(q)
                else:
                    newOrder = oldOrder

            if(direc == 'right'):
                if(k < (len(stageList)-1)):
                    for q in range(k):
                        newOrder.append(q)
                    newOrder.append(k+1)
                    newOrder.append(k)
                    for q in range(k+2 , len(stageList)):
                        newOrder.append(q)
                else:
                    newOrder = oldOrder

    stageList = [stageList[i] for i in newOrder]

    return stageList