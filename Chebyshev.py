import math

#Funcion que se enarga de encontrar el orden correcto de la aproximación
def Chebyshev_Order(As,Ap,Ws,Wp):
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
#Se encarga de devolver los polos 
def Chebyshev_Polos(N,e):
    Polos = []
    Re_cte=-math.sinh((1/N)*math.asinh(1/e))
    Im_cte=math.cosh((1/N)*math.asinh(1/e))
    for i in range(N):
        Polos_Re=Re_cte*math.sin( ( math.pi*(2*(i+1) -1) ) / ( 2*N ) ) 
        Polos_Im= Im_cte*math.cos( ( math.pi*(2*(i+1) -1) ) / ( 2*N ) )
        Polos.append(Polos_Re+1j*Polos_Im)
    return Polos

#Se encontrar el epsilon
def Chebyshev_Epsilon(Ap):
    Epsilon=math.sqrt(10**(Ap/10)-1)
    return Epsilon
#Obtenemos la aproximacion normalizada
def Chebyshev_Aprox(As,Ap,Ws,Wp,N=0,Nmin=0,Nmax=0):
    if N ==0 :
        N=Chebyshev_Order(As,Ap,Ws,Wp)
        if Nmin !=0 & Nmax !=0:
            if Nmin > N:
                N=Nmin
            elif N > Nmax:
                N=Nmax 
    e=Chebyshev_Epsilon(Ap)
    print("Epsilos=",e)
    P=Chebyshev_Polos(N,e)
    """ Ahora vamos a calcular la constante que se le multiplica 
    a la funcion tranferencia cuando la obtenemos por polos"""
    K=(-1)**N
    for i in range(N):
        #Si es mas chico que 1*10**(-10) entonces es aproximadamente 0
        if(P[i].imag < 1e-10 and P[i].imag>0) or (P[i].imag > -1e-10 and P[i].imag<0):
            P[i]-=P[i].imag*1j
        K*=P[i]
    K*=1/math.sqrt(1+ (e**2) * ( (math.cos( N* math.acos(0) ))**2 ) )
    K=K.real
    return N,P,K
