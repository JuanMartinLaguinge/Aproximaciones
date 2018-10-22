#Importo las funciones a utilizar
from Normalizador import Normalizacion
from desnormalizacion import desnormalizacion
from Chebyshev import Chebyshev_Aprox
from Chebyshev2 import Chebyshev2_Aprox
from butterworth import butterworth
from Bessel import AproxBessel
import scipy
import numpy

class AproximadorFiltro:
    #Defino un constructor que me ayude con chequeos
    def __init__(self):
        self.Retardo=0
        self.Ws=1
        self.Wp=1.2
        self.Ws_mas=0
        self.Wp_mas=0
        self.Wrg=0
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
        #Cada vez que me dan los datos para filtros normales seteo el retraso en 0
        self.Retardo=0
        self.Const=1
    #Datos para una funcion que use retardo de grupo
    def DatosRetard(self,Tipo,Retardo,Wrg,Tol,Qmax=0,N=0,Nmin=0,Nmax=15):
        self.Tipo=Tipo
        self.Retardo=Retardo
        self.Wrg=Wrg
        self.Tol=Tol
        self.Qmax=Qmax
        self.N=N
        self.Nmin=Nmin
        self.Nmax=Nmax
    #Se encarga de realizar la aproximacion dado los datos recibidos
    def Aproximacion(self):
        #Variables a utilizar
        Polos=[]
        Ceros=[]
        OK=False
        self.Const=1
        #Primero garantizo el tipo de filtro que quiero
        if self.Retardo != 0:
            Filtro="retard"
        elif self.Wp_mas == 0:
            if self.Wp < self.Ws:
                Filtro="low-pass"
            else:
                Filtro="high-pass"
        else:
            if self.Wp_mas < self.Ws_mas:
                Filtro="band-pass"
            else:
                Filtro='band-stop'
        #Una vez que ya tengo el tipo de filtro procedo a normalizarlo
        if self.Retardo != 0:
            Wrgn=Normalizacion(Filtro,self.Ws,self.Wp,self.Ws_mas,self.Wp_mas,self.Retardo,self.Wrg)
        else:
            Wpn,Wsn=Normalizacion(Filtro,self.Ws,self.Wp,self.Ws_mas,self.Wp_mas,self.Retardo,self.Wrg)
        #print("Los valores normalizados son Wpn=",Wpn,"y Wsn=",Wsn,"para un filtro "+Filtro)
        while OK == False:
            if self.Tipo=="butterworth":
                Ceros,Polos=butterworth(self.Ap,self.As,Wpn,Wsn,self.N,self.Nmin,self.Nmax,self.Porcentaje)
                self.Const=1
            elif self.Tipo=="chebyshev I":
                self.N,Polos,self.Const=Chebyshev_Aprox(self.As,self.Ap,Wsn,Wpn,self.N,self.Nmin,self.Nmax,self.Porcentaje)
            elif self.Tipo=="chebyshev II":
                self.N,Polos,Ceros,self.Const=Chebyshev2_Aprox(self.As,self.Ap,Wsn,Wpn,self.N,self.Nmin,self.Nmax,self.Porcentaje)
            elif self.Tipo=="bessel":
                if self.Nmax==0:
                    #Es un limite que le ponemos por predeterminado
                    self.Nmax=15
                self.N,Polos,self.Const=AproxBessel(self.Retardo,Wrgn,self.Tol,self.N,self.Nmin,self.Nmax)
            '''#Chequeo
            for i in range(len(Polos)):
                print("Polo",i,"=",Polos[i])
            for i in range(len(Ceros)):
                print("Cero",i,"=",Ceros[i])
            print("La constante es",self.Const)'''
            #Ya tenemos la aproximacion normalizada solo falta desnormalizarla
            Num,Den=desnormalizacion(Filtro,Ceros,Polos,self.Wp,self.Wp_mas,self.Const,self.Retardo)
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
        # print("Los numeradores son",Num)
        # print("Los denominadores son",Den)
        # for i in range(len(Polos)):                
        #     print("Polo",i,"=",Polos[i])
        # for i in range(len(Ceros)):
        #     print("Cero",i,"=",Ceros[i])
        #     print("La constante es",self.Const)
        # print("El orden es de",self.N)
        #Chequeo
        #Devolvemos los polos en frecuencia para las Aproximaciones de plantilla y en radianes/segundo para bessel
        return Num,Den
