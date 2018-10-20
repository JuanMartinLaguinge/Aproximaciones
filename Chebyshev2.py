import math
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
def Chebyshev2_CerosYPolos(N,e):
    Re_cte=-math.sinh((1/N)*math.asinh(1/e))
    Im_cte=math.cosh((1/N)*math.asinh(1/e))
    Polos = []
    for i in range(N):
        Polos_ReTemp= Re_cte*math.sin( ( math.pi*(2*(i+1) -1) ) / ( 2*N ) ) 
        Polos_ImTemp= Im_cte*math.cos( ( math.pi*(2*(i+1) -1) ) / ( 2*N ) ) 
        Polos_Re = Polos_ReTemp/(Polos_ReTemp**2 + Polos_ImTemp**2)
        Polos_Im = -Polos_ImTemp/(Polos_ReTemp**2 + Polos_ImTemp**2)
        Polos.append(Polos_Re+1j*Polos_Im)
    #Ahora calculo los ceros y estos solo poseen parte imaginaria
    Zeros = []
    if N % 2 == 0:
        RangoZ=N//2
    else:
        RangoZ=N//2+N%2
    for i in range(RangoZ):
        Zeros.append( 1j/math.cos( (math.pi)*(2*i+1) / (2*N) ) )
    return Polos,Zeros

def Chebyshev2_Aprox(As,Ap,Ws,Wp,N=0,Nmin=0,Nmax=0,Porcentaje=0):
    if N ==0 :
        N=Chebyshev2_Order(As,Ap,Ws,Wp)
        if Nmin !=0 & Nmax !=0:
            if Nmin > N:
                N=Nmin
            elif N > Nmax:
                N=Nmax 
    if(Porcentaje == 0):
        e=Chebyshev2_Epsilon(Ap)*(1/math.cos(N*math.acos(1/Wp)))
    else:
        e1=Chebyshev2_Epsilon(Ap)*(1/math.cos(N*math.acos(1/Wp)))
        e2=Chebyshev2_Epsilon(As)
        e=e1+(Porcentaje/100)*(e2-e1)
    #print("Epsilos=",e)
    P,Zeros=Chebyshev2_CerosYPolos(N,e)
    """ Ahora vamos a calcular la constante que se le multiplica 
    a la funcion tranferencia cuando la obtenemos por polos"""
    for i in range(N):
        #Si es mas chico que 1*10**(-10) entonces es aproximadamente 0
        if(P[i].imag < 1e-10 and P[i].imag>0) or (P[i].imag > -1e-10 and P[i].imag<0):
            P[i]-=P[i].imag*1j
     #La desnormalizacion asegura que la funcion tranferencia no vaya a dar
    # un valor deferente de 1 en s=0 pero eso no alcanza para cheby dado que
    # tambien necesito que sea igual a la normalizado con lo cual calculo el
    #valor de donde empezaria en cheby y se lo multiplico al valor que hace que
    #cuando lo calcules por polos esta funcion no se vaya del 1
    K=math.sqrt( (e**2) * ( (math.cos( N* math.acos(0) ))**2 ) )/math.sqrt(1+ (e**2) * ( (math.cos( N* math.acos(0) ))**2 ) )
    return N,P,Zeros,K
