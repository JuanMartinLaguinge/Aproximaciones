import math
import cmath

class P_Z:
    real = 0               #la funcion transerencia
    imag = 0
    Q = 0
    fo = 0             
    sel = 0                 #un booleano que nos dice si la etapa esta seleccionada

    def loadData(self):
        Q = math.sqrt(self.real**2 + self.imag**2)/(2*self.real)
        fo = math.sqrt(self.real**2 + self.imag**2)/(2*math.pi)