import classEtapa
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

def acumulative(stageList):
    # esta funcion recive la lista de etapas y devuelve la magnitud acumulada junto con el w
    if(len(stageList)):
        w,mag,pha = signal.bode(stageList[0].H)
        mag = np.array(mag)
        w = np.array(w)

        for k in range(1,len(stageList)):               #no agarro el primero porque ya lo tome
            wo,mago,phao = signal.bode(stageList[k].H)
            mago = np.array(mago)
            mag = mag + mago        #voy sumando las magnitudes

    return w, mag