import sympy

#Se encarga de realizar el polinomio de Bessel de manera recursiva y solo es necesario darle el orden
def PoliBessel (N):
    s=sympy.Symbol('s')
    B1=s+1
    B2=(s**2)+(3*s)+3
    if N==1:
        B= B1
    elif N==2:
        B= B2
    else:
        B=sympy.expand ( (2*N-1)*PoliBessel(N-1)+(s**2)*PoliBessel(N-2))
    return B

#Se encarga de realizar la normalizacion para bessel
def NormaBessel(Retardo,Wrg):
    #Normalizo la frecuencia de paso
    Wrgn=Retardo*Wrg
    return Wrgn

'''Se encarga de devolver los coeficientes de la funcion tranferencia de Bessel
Recibe el Retardo de grupo querido, la freceuncai a la cual el retardo de grupo
debe superar una cierta tolerancia y la tolerancia en porcentaje'''
def AproxBessel(Retardo,Wrg,Tol):
    s=sympy.Symbol('s')
    Wn=NormaBessel(Retardo,Wrg)
    #Trato de obtener la funcion de bessel que cumpla con lo pedido
    N=1
    print("Frecuencia de paso normalizada es ",Wn)
    while N < 15:
        Polinomio = PoliBessel(N)
        Tranferencia = Polinomio.subs(s,0)/Polinomio.subs(s,1j*Wn)
        Temp= ( ( Wn**(2*N) ) * (abs(Tranferencia)**2) )/ (Polinomio.subs(s,0)**2)
        if (Temp<Tol):
            print(Temp)
            break
        else:
            N+=1
    return N,Polinomio    
import math

def main():
    print(AproxBessel(10e-03,600,0.20))

if __name__ == "__main__":
    main()