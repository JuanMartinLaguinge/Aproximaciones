import math

#Funcion que se enarga de encontrar el orden correcto de la aproximación
def Chebyshev_Order(As,Ap,Ws,Wp):
    N_Up=math.acosh(math.sqrt((10**(As/10)-1)/(10**(Ap/10)-1)))
    N_Down=math.acosh(Ws/Wp)
    N_Order=N_Up/N_Down
    '''Con esto ya calculamos el valor del orden de la aproximacion 
    pero todavia tenemos que elegir el valor entero mayor o 
    igual al que ya tenemos'''
    N=math.ceil(N_Order)
    return N
#Se encarga de devolver los polos 
def Chebyshev_Polos(N,e):
    Polos = []
    Re_cte=math.sinh((1/N)*math.asinh(1/e))
    Im_cte=math.cosh((1/N)*math.asinh(1/e))
    for i in range(N):
        Polos_Re= round( Re_cte*math.sin( ( math.pi*(2*(i+1) -1) ) / ( 2*N ) ) ,6)
        Polos_Im= round( Im_cte*math.cos( ( math.pi*(2*(i+1) -1) ) / ( 2*N ) ) ,6)
        Polos.append(Polos_Re+1j*Polos_Im)
    return Polos

#Se encontrar el epsilon
def Chebyshev_Epsilon(Ap):
    Epsilon=math.sqrt(10**(Ap/10)-1)
    return Epsilon
#Obtenemos la aproximacion normalizada
def Chebyshev_Aprox(As,Ap,Ws,Wp,N=0,Nmin=0,Nmax=0,Porcentaje=0):
    if N ==0 :
        N=Chebyshev_Order(As,Ap,Ws,Wp)
        if Nmin !=0 and Nmax !=0:
            if Nmin > N:
                N=Nmin
            elif N > Nmax:
                N=Nmax 
    if(Porcentaje == 0):
        e=Chebyshev_Epsilon(Ap)
    else:
        e1=Chebyshev_Epsilon(Ap)
        e2=Chebyshev_Epsilon(As)/(math.cosh(N*math.acosh(Ws)))
        e=e1+(Porcentaje/100)*(e2-e1)
    #print("Epsilos=",e)
    P=Chebyshev_Polos(N,e)
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
    K=1/math.sqrt(1+ (e**2) * ( (math.cos( N* math.acos(0) ))**2 ) )
    return N,P,K
