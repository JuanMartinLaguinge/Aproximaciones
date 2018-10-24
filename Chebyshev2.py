import math
from scipy import signal
import sympy
from bodeSym import bodeSym

def Chebyshev2_Corrimiento(N,e,Ws,Wp,Ap,Porcentaje,polos,ceros):
    #Normalizo para Ws
    for i in range(len(polos)):
        polos[i]*=Ws
    for i in range(len(ceros)):
        ceros[i]*=Ws  
    #Luego busco el Wp de este
    W=[]
    num=1
    den=1
    s=sympy.Symbol('s')
    for k in range (0,len(ceros)):
        num = num*(s-ceros[k])  
    for k in range (0,len(polos)):
        den = den*(s-polos[k]) 
    H_nor = num/den
    #k es la constante que queda mutiplicando al H en formato normalizado
    k = H_nor.subs(s,0) 
    #al sacarle esa constante hacemos que la funcion no tenga ganancia constante
    H_nor = H_nor/k
    print(polos)
    #Creo el intervalo de W donde quiero que evalue
    for i in range(1, 1000000 ):
        W.append(0.01*Ws*i)   
    W,Mag=bodeSym(H_nor,W)
    #Cuando me pide al lado de Ws entonces no necesito hacer este calculo
    if Porcentaje!=100:
        for i in range(len(Mag)):
            Mag[i]=-Mag[i]
            if(Mag[i] > Ap):
                w=W[i-1]
                break
    else:
        w=0
    #Tengo que usar el Ws para el Wp que quiero para que luego no este pegado al As
    deltaW=Ws-w
    ExtraWs=Ws-(Wp+deltaW)
    NuevoWs=Wp+deltaW+ExtraWs*(Porcentaje/100)
    for i in range(len(polos)):
        polos[i]*=NuevoWs/Ws
    for i in range(len(ceros)):
        ceros[i]*=NuevoWs/Ws    
    return ceros,polos

#Funcion que se enarga de encontrar el orden correcto de la aproximación
def Chebyshev2_Order(As,Ap,Ws,Wp):
    N_Up=math.acosh(math.sqrt((10**(As/10)-1)/(10**(Ap/10)-1)))
    N_Down=math.acosh(Ws/Wp)
    N_Order=N_Up/N_Down
    '''Con esto ya calculamos el valor del orden de la aproximacion 
    pero todavia tenemos que elegir el valor entero mayor o 
    igual al que ya tenemos'''
    N=math.ceil(N_Order)
    return N

#Se encontrar el epsilon
def Chebyshev2_Epsilon(As):
    Epsilon=1/math.sqrt(10**(As/10)-1)
    return Epsilon

#Se encarga de devolver los polos
def Chebyshev2_CerosYPolos(N,e,Ws):
    Re_cte=-math.sinh((1/N)*math.asinh(1/e))
    Im_cte=math.cosh((1/N)*math.asinh(1/e))
    Polos = []
    for i in range(N):
        Polos_ReTemp= Re_cte*math.sin( ( math.pi*(2*(i+1) -1) ) / ( 2*N ) ) 
        Polos_ImTemp= Im_cte*math.cos( ( math.pi*(2*(i+1) -1) ) / ( 2*N ) ) 
        Polos_Re = Polos_ReTemp/(Polos_ReTemp**2 + Polos_ImTemp**2)
        Polos_Im = -Polos_ImTemp/(Polos_ReTemp**2 + Polos_ImTemp**2)
        Polos.append(Ws*(round(Polos_Re,6) + 1j*round(Polos_Im,6) ) )
    #Ahora calculo los ceros y estos solo poseen parte imaginaria
    Zeros = []
    if N % 2 == 0:
        RangoZ=N//2
    else:
        RangoZ=N//2+N%2
    for i in range(RangoZ):
        Zeros.append( Ws*1j*round (1/math.cos( (math.pi)*(2*i+1) / (2*N) ),6 ) )
        #Falta el Cero congujado
        if (Zeros != 0):
            Zeros.append(Zeros[i].conjugate())
    return Polos,Zeros

def Chebyshev2_Aprox(As,Ap,Ws,Wp,N=0,Nmin=0,Nmax=0,Porcentaje=0):
    if N ==0 :
        N=Chebyshev2_Order(As,Ap,Ws,Wp)
        if Nmin !=0 and Nmax !=0:
            if Nmin > N:
                N=Nmin
            elif N > Nmax:
                N=Nmax 
    e=Chebyshev2_Epsilon(As)
    P,Zeros=Chebyshev2_CerosYPolos(N,e,1)
    """ Ahora vamos a calcular la constante que se le multiplica 
    a la funcion tranferencia cuando la obtenemos por polos"""
    for i in range(N):
        #Si es mas chico que 1*10**(-10) entonces es aproximadamente 0
        if(P[i].imag < 1e-10 and P[i].imag>0) or (P[i].imag > -1e-10 and P[i].imag<0):
            P[i]-=P[i].imag*1j
    for i in range(len(Zeros)):
        if (Zeros[i].real< 1e-10 and Zeros[i].real>0) or (Zeros[i].real> -1e-10 and Zeros[i].real<0):
            Zeros[i]=Zeros[i].imag*1j
    #Me falta realizar el Porcentaje
    Zeros,P=Chebyshev2_Corrimiento(N,e,Ws,Wp,Ap,Porcentaje,P,Zeros)
    return N,P,Zeros
