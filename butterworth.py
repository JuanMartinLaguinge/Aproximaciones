import math
import cmath
from sympy import *

def butterworth(Ap,As,Wpn,Wsn,N=0,Nmin=0,Nmax=0,rango=0):
    #las variables wp_mas y ws_mas son para hacer bandas
    #N es para que el usuario configure un orden fijo
    #si Nmax no es sero se toma al N como orden minimo y Nmax como orden maximo
    E = sqrt(10**(Ap/10) - 1)
    n = math.log10(sqrt(10**(As/10) - 1) / E) / math.log10(Wsn)

    if(N == 0):              #no hay orden fijo
        if(Nmax == 0):      #no hay rango de orden
            if(n == int(n)):
                n = int(n)
            else:
                n = int(n) + 1
        else:
            if(n < Nmin):
                n = Nmin
            elif(n > Nmax):
                n = Nmax
            if(n == int(n)):
                n = int(n)
            else:
                n = int(n) + 1
    else:
        n = N

    if(rango != 0):      #el usuario quiere un rango de aproximacion de 1 a 100
        Ep = sqrt(10**(As/10) - 1)/(Wsn**n)
        E = E + (rango/100)*(Ep - E)

    radio = math.pow(E,-1/n)
    ang = math.pi/n
    ceros = []
    polos = []

    phase_ini = math.pi/2 + ang/2

    for k in range (0,n):
        a = cmath.rect(radio, phase_ini + k*ang)
        polos.append(round(re(a),6) + I*round(im(a),6))

    return n,ceros,polos
