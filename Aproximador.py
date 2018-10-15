#Importo las funciones a utilizar
from Normalizador import Normalizacion
from desnormalizacion import desnormalizacion
from Chebyshev import Chebyshev_Aprox
from Chebyshev2 import Chebyshev2_Aprox
from butterworth import butterworth

class AproximadorFiltro:
    #Defino el constructor de la clase en el que creo las variables a usar
    def _init_(self):
        self.Polos=[]
        self.Zeros=[]
    #Le pamos los datos necesarios para la aproximacion
    def Datos(self,Tipo,Ap,As,Wp,Ws,Wp_mas=0,Ws_mas=0,Porcentaje=0,Qmax=0,N=0,Nmin=0,Nmax=0):
        self.Tipo=Tipo
        self.Ws=Ws
        self.Wp=Wp
        self.As=As
        self.Ap=Ap
        self.Wp_mas=Wp_mas
        self.Ws_mas=Ws_mas
        self.Qmax=Qmax
        self.N=N
        self.Nmin=Nmin
        self.Nmax=Nmax
        self.Porcentaje=Porcentaje
    #Se encarga de realizar la aproximacion dado los datos recibidos
    def Aproximacion(self):
        #Primero garantizo el tipo de filtro que quiero
        if self.Wp_mas == 0:
            if self.Wp < self.Ws:
                Filtro="low-pass"
            else:
                Filtro="high-pass"
        else:
            if self.Wp < self.Ws:
                Filtro="bandwidth-pass"
            else:
                Filtro='Reject-band'
        #Una vez que ya tengo el tipo de filtro procedo a normalizarlo
        Wpn,Wsn=Normalizacion(Filtro,self.Ws,self.Wp,self.Wp_mas,self.Ws_mas)
        print("Los valores normalizados son Wpn=",Wpn,"y Wsn=",Wsn,"para un filtro "+Filtro)
        if self.Tipo=="Butterworth":
            print("Butter")
        elif self.Tipo=="Chebyshev I":
            print("Cheby1")
        elif self.Tipo=="Chebyshev II":
            print("Cheby II")
        else:
            print("Bessel")


def main():
    Aprox=AproximadorFiltro()
    Aprox.Datos("Butterworth",2,4,1e03,1.2e03)
    Aprox.Aproximacion()

#Es necesario para poder ejecutar una funcion dentro del archivo
if __name__ == "__main__":
    main()