import math
import cmath

class P_Z:
    real = 0               #la funcion transerencia
    imag = 0
    Q = 0
    fo = 0             
    sel = 0                 #un booleano que nos dice si la etapa esta seleccionada
    mod = 0

    def loadData(self):
        if(self.real == 0 and self.imag == 0):
            Q = 0
        else:
            self.Q = round(math.sqrt(self.real**2 + self.imag**2)/abs(2*self.real),3)
            self.fo = round(math.sqrt(self.real**2 + self.imag**2)/(2*math.pi),3)
            self.mod = math.sqrt(self.real**2 + self.imag**2)
