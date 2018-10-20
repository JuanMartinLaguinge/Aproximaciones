#Importo las funciones a utilizar
from Normalizador import Normalizacion
from desnormalizacion import desnormalizacion
from Chebyshev import Chebyshev_Aprox
from Chebyshev2 import Chebyshev2_Aprox
from butterworth import butterworth
import scipy
import numpy

class AproximadorFiltro:
    #Defino el constructor de la clase en el que creo las variables a usar
    #def _init_(self):

    #Le damos los datos necesarios para la aproximacion
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
        self.Const=1
    #Se encarga de realizar la aproximacion dado los datos recibidos
    def Aproximacion(self):
        #Variables a utilizar
        Polos=[]
        Ceros=[]
        OK=False
        self.Const=1
        #Primero garantizo el tipo de filtro que quiero
        if self.Wp_mas == 0:
            if self.Wp < self.Ws:
                Filtro="low-pass"
            else:
                Filtro="high-pass"
        else:
            if self.Wp < self.Ws:
                Filtro="band-pass"
            else:
                Filtro='band-stop'
        #Una vez que ya tengo el tipo de filtro procedo a normalizarlo
        Wpn,Wsn=Normalizacion(Filtro,self.Ws,self.Wp,self.Wp_mas,self.Ws_mas)
        #print("Los valores normalizados son Wpn=",Wpn,"y Wsn=",Wsn,"para un filtro "+Filtro)
        while OK == False:
            if self.Tipo=="Butterworth":
                Ceros,Polos=butterworth(self.Ap,self.As,Wpn,Wsn,self.N,self.Nmin,self.Nmax,self.Porcentaje)
                self.Const=1
            elif self.Tipo=="Chebyshev I":
                self.N,Polos,self.Const=Chebyshev_Aprox(self.As,self.Ap,Wsn,Wpn,self.N,self.Nmin,self.Nmax,self.Porcentaje)
            elif self.Tipo=="Chebyshev II":
                self.N,Polos,Ceros,self.Const=Chebyshev2_Aprox(self.As,self.Ap,Wsn,Wpn,self.N,self.Nmin,self.Nmax,self.Porcentaje)
            else:
                print("Bessel")
            '''#Chequeo
            for i in range(len(Polos)):
                print("Polo",i,"=",Polos[i])
            for i in range(len(Ceros)):
                print("Cero",i,"=",Ceros[i])
            print("La constante es",self.Const)'''
            #Ya tenemos la aproximacion normalizada solo falta desnormalizarla
            Num,Den=desnormalizacion(Filtro,Ceros,Polos,self.Wp,self.Wp_mas)
            if type(Num) != float:
                for i in range(len(Num)):
                    Num[i]=Num[i]*self.Const
            else:
                Num*=self.Const
            #Al final chequeamos que cumpla con la condicion del Qmax dado de haber dado uno
            #Para eso primero eliminamos los elementos anteriores de las listas
            if type(Ceros) == list :
                Ceros.clear()
            if type(Polos) == list :
                Polos.clear()
            Ceros= scipy.roots(Num)
            Polos= scipy.roots(Den)
            #Ahora calculo el Q para ver que cumpla con la condicion del Qmax
            if self.Qmax != 0:
                for i in range(len(Polos)):
                    Q_Polos= abs( Polos[i] ) / (2*(Polos[i].real) )
                    #Chequeo            
                    print("QPolo",i,"=",Q_Polos)
                    #Chequeo
                    if Q_Polos > self.Qmax :
                        if self.N > 1:
                            self.N=self.N-1
                        #Cheque que no se pueda hacer lo imposible que es realizar una aproximacion de orden menor a 1
                        else:
                            OK= True
                            print("No se puedo realizar una aproximacion con el Q pedido")
                        break
                    '''Chequeo si hay algun cero, dado que si no hay entonces ya no hay más Q que calcular'''
                    if ( len(Ceros) == 0 ) and ( (i+1) == len(Polos)) :
                        OK= True
                for i in range(len(Ceros)):
                    Q_Ceros= abs( Ceros[i] ) / (2*(Ceros[i].real) )
                    """ #Chequeo            
                    print("QCero",i,"=",Q_Ceros)
                    #Chequeo """
                    if Q_Ceros > self.Qmax:
                        if self.N > 1:
                            self.N-=1
                        #Cheque que no se pueda hacer lo imposible que es realizar una aproximacion de orden menor a 1
                        else:
                            OK=True
                            print("No se puedo realizar una aproximacion con el Q pedido")
                    if  (i+1) == len(Polos) :
                        OK= True               
            else:
                OK=True
            #Reseteo la constante para el proximo calculo
            if OK != True:
                self.Const=1
        '''Devolvemos el valor de forma tal que el primer numero del arreglo de los 
        cocientes es el que tiene el mayor orden y van decreciendo a medida que uno lee 
        del primer elemento al ultimo'''
        #Chequeo
        print("Los numeradoes son",Num*self.Const)
        print("Los denominadores son",Den)
        for i in range(len(Polos)):                
            print("Polo",i,"=",Polos[i])
        for i in range(len(Ceros)):
            print("Cero",i,"=",Ceros[i])
            print("La constante es",self.Const)
        print("El orden es de",self.N)
        #Chequeo
        
        #return Num,Den


def main():
    Aprox=AproximadorFiltro()
    Aprox.Datos("Chebyshev I",2,4,1e03,1.2e03,0,0,0,1.8,0,0,0)
    Aprox.Aproximacion()
#Es necesario para poder ejecutar una funcion dentro del archivo
if __name__ == "__main__":
    main()