import math
from scipy import signal
import sympy

# #Para tener una aproximacion mas exsacta del epsilon
def Chebyshev2Tn(N):
    s=sympy.Symbol('s')
    T0=0
    T1=s
    if N==0:
        return T0
    elif N==1:
        return T1
    else:
        return 2*s*Chebyshev2Tn(N-1)-Chebyshev2Tn(N-2)
#Evaluacion del Tn
def EvalTn(N,Ws,W):
    s=sympy.Symbol('s')
    Tn=Chebyshev2Tn(N)
    Tn=Tn.subs(s,Ws/W)
    return Tn

def Chebyshev2_Corrimiento(N,e,Ws,Wp,Ap,Porcentaje,polos,ceros):
    #Normalizo para Ws
    for i in range(len(polos)):
        polos[i]*=Ws
    for i in range(len(ceros)):
        ceros[i]*=Ws  
    #Luego busco el Wp de este
    num=1
    den=1
    s=sympy.Symbol('s')
    for k in range (0,len(ceros)):
        num = num*(s-ceros[k])  #tenemos el numerador de la funcion transf norm
    for k in range (0,len(polos)):
        den = den*(s-polos[k])  #tenemos el denominador de la funcion transf norm
    H_nor = num/den
    k = H_nor.subs(s,0) #k es la constante que queda mutiplicando al H en formato normalizado
    H_nor = H_nor/k     #al sacarle esa constante hacemos que la funcion no tenga ganancia constante
    #Tn=Chebyshev2Tn(N)
    #Tn=Tn.subs(s,-1j*Ws/s)
    #HCuad=1-(1/(1+(e**2)*(Tn**2)))
    #k=HCuad.subs(s,0)
    #HCuad=HCuad/k
    #Cuando me pide al lado de Ws entonces no necesito hacer este calculo
    if Porcentaje!=100:
        for i in range(10000,10000000000):
            mag=(-20)*(math.log10(abs( H_nor.subs(s,0.0001j*i) ) ) )
            if(mag > Ap):
                w=0.0001*(i-1)
                print(mag)
                print("El W",w)
                break
    else:
        w=0
    #Al realizar varias prubas esta apoximacion funciona para valores de Ws>w
    #if Ws>w:
    deltaW=Ws-w
    ExtraWs=Ws-(Wp+deltaW)
    print(Ws,deltaW)
    NuevoWs=Wp+deltaW+(Porcentaje/100)*ExtraWs
    print(Ws)
    #else:
    #    deltaW=Ws-w
    #    ExtraWs=Ws-(Wp+deltaW)
    #    Ws=Wp+deltaW*(1-Porcentaje/100)
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
    N_Temp=round(N_Order,0)
    if N_Order < N_Temp:
        N = int(N_Temp)
    else:
        N_Temp=N_Order-N_Temp
        N= int(N_Order+1-N_Temp)
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
    #e1=Chebyshev2_Epsilon(Ap)/EvalTn(N,Wp,Ws)
    e=Chebyshev2_Epsilon(As)
    #e=e1+( Porcentaje /100)*(e2-e1)
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
