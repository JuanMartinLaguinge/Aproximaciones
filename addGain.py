import classEtapa
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

def addGain(stageList,gain):
    # esta funcion le mandas la lista de las etapas, busca la que este seleccionada
    # y le suma a su funcion transferencia un offset de ganancia (en dB)

    veces = 10**(gain/20)

    for k in range(len(stageList)):
        if(stageList[k].sel == True):
            stageList[k].H = signal.TransferFunction(stageList[k].H.num*veces,stageList[k].H.den)

    return stageList