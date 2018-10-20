import sympy

#Se encarga de realizar el polinomio de Bessel de manera recursiva y solo es necesario darle el orden
def PoliBessel (N):
    s=sympy.Symbol('s')
    B1=s+1
    B2=s**2+3*s+3
    if N == 1:
        return B1
    elif N == 2:
        return B2
    else:
        Num=2
        while(Num != N):
            Num+=1
            B=(2*Num-1)*B2+(s**2)*B1
            B2=B
            B1=B1
#De esta manera devolvemos la expresion resuelta simbolicamente
            return sympy.expand(B)
    

def main():
    H=PoliBessel(3)
    print(H)

if __name__ == "__main__":
    main()