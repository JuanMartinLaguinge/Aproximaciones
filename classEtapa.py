from scipy import signal
import math
import cmath

class Etapa:
    H               #la funcion transerencia
    Q
    fo
    sel             #un booleano que nos dice si la etapa esta seleccionada

    def loadData(self):
        if(len(self.H.poles) == 2):
            Q = abs(self.H.poles[0])/(2*self.H.poles[0].real())
            fo = abs(self.H.poles[0])/(2*math.pi)