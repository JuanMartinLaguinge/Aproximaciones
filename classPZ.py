import math
import cmath

class P_Z:
    real = 0      
    imag = 0
    Q = 0
    fo = 0             
    sel = 0                 #un booleano que nos dice si la singularidad esta seleccionada
    mod = 0

    def loadData(self):
        if(self.real == 0 and self.imag == 0):
            Q = 0                   # si la singularidad esta sobre el origen del plano S vamos a decir que si Q es 0 (aunque en realidad no es asi)
        elif(self.real == 0 and self.imag != 0):
            Q = math.inf            # si los complejos conjugados no tiene parte real tienen un Q inifinito
        else:
            self.Q = round(math.sqrt(self.real**2 + self.imag**2)/abs(2*self.real),3)
            self.fo = round(math.sqrt(self.real**2 + self.imag**2)/(2*math.pi),3)
            self.mod = math.sqrt(self.real**2 + self.imag**2)
