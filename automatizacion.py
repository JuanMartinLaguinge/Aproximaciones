import crearEtapa
import classEtapa
import classPZ
import singularidades as sin
import math
import cmath
from scipy import signal

def automatizacion(ceros,polos):
    # a esta funcion le entras con una lista de nuestras clases de polos y ceros
    # y te devuelve una lista de etapas para minimizar, ponele, el RD
    clearSel(ceros)
    clearSel(polos)
    stageList = []
    stageClass = classEtapa.Etapa()
    
    while (not allSelected(ceros) and not allSelected(polos)):
        Zlist = []
        Plist = []
        aux = stageClass.__class__
        stage = aux()
        

        if(not allSelected(polos)):
            Qo = math.inf                          #inicializo con un valor de Q
            for k in range (len(polos)):
                if(polos[k].sel == False):          #si el polo todavia no fue seleccionado
                    if(polos[k].Q < Qo):            #quiero el polo que tenga el menor Q
                        mipolo = k
                        Qo = polos[k].Q
            
            polos[mipolo].sel = True                #tengo el polo de menor Q de los disponibles
            Plist.append(polos[mipolo])

        if(not allSelected(ceros) and len(ceros) > 0):
            Qo = 0                                #inicializo con un valor de Q
            for k in range (len(ceros)):
                if(ceros[k].sel == False):          #si el cero todavia no fue seleccionado
                    if(ceros[k].Q >= Qo):            #quiero el cero que tenga el mayor Q
                        micero = k
                        Qo = ceros[k].Q

            ceros[micero].sel = True
            Zlist.append(ceros[micero])

        if(polos[mipolo].imag == 0 and not allSelected(polos)):            #agarre uno simple, voy a agarrar otro para hacerlo de orden 2
            Qo = math.inf                          
            for k in range (len(polos)):
                if(polos[k].sel == False and polos[k].imag == 0):
                    if(polos[k].Q < Qo):           
                        mipolo = k
                        Qo = polos[k].Q
                    polos[mipolo].sel = True     
                    Plist.append(polos[mipolo])

        if(not allSelected(ceros) and len(ceros) > 0):      # no junto todo dentro de un solo if porque 
            if(ceros[micero].imag == 0):                    # 'micero' puede no estar definido
                Qo = 0
                for k in range (len(ceros)):
                    if(ceros[k].sel == False and ceros[k].imag == 0):          
                        if(ceros[k].Q >= Qo):            
                            micero = k
                            Qo = ceros[k].Q

                ceros[micero].sel = True
                Zlist.append(ceros[micero])

        stage = crearEtapa.crearEtapa(Plist,Zlist)
        stage.loadData()
        stageList.append(stage)
    return stageList

    

def allSelected(arreglo):
    if(len(arreglo) == 0):              #si la lista de ceros o polos no tiene nada devuelvo 0
        ret = False
    else:
        ret = True
        for k in range(len(arreglo)):
            if(arreglo[k].sel == 0):
                ret = False
    return ret

def clearSel(arreglo):
    for k in range(len(arreglo)):
        arreglo[k].sel = 0
