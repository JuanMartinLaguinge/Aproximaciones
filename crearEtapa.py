from scipy import signal
import classPZ
import math
import cmath
import classEtapa

def crearEtapa(polos,ceros):
# a esta funcion le entras con una lista de polos y ceros y te arma la etapa
# que la etapa seria una funcion transferencia
# logicamente a lo sumo le vas a entrar con 2 ceros y 2 polos

    stage = classEtapa.Etapa()
    if(len(polos) == 1):    # si solo se mando un polo
        if(polos[0].imag > 0):  # y tiene parte imaginaria mayor a 0, entonces es un par de polo conjugado
            wo = polos[0].mod
            #print("wo : ",wo)
            zi = abs(polos[0].real)/wo
            #print("zi : ",zi)
            q = 1/(2*zi)
            #print("q : ",q)
            den = [1/(wo**2), 1/wo * 1/q, 1]
        else:               # si no tiene parte imaginaria es un solo polo simple
            den = [0, 1/abs(polos[0].real), 1]
    elif(len(polos) == 2):  # de ultima el user mando 2 polos reales y distintos
        den = [1/(polos[0].real*polos[1].real), 1/polos[0].real + 1/polos[1].real, 1] # y matematicamente los coeficientes serian esos
    elif(len(polos) == 0):
        den = 1

    if(len(ceros) == 1):
        if(ceros[0].imag > 0):
            wo = ceros[0].mod
            zi = abs(ceros[0].real)/wo
            q = 1/(2*zi)
            num = [1/(wo**2), 1/wo * 1/q, 1]
        else: 
            num = [0, 1/abs(ceros[0].real), 1]
    elif(len(ceros) == 2):
        if(ceros[0].Q == 0 and ceros[1].Q == 0):                # Q = 0 es nuestra manera se saber que la singularidad esta sobre origen del plano S
            num = [1,0,0]
        elif(ceros[0].Q == 0 and ceros[1].Q != 0):             
            num = [1,ceros[1],0]
        elif(ceros[0].Q != 0 and ceros[1].Q == 0):             
            num = [1,ceros[0],0]
        else:
            num = [1/(ceros[0].real*ceros[1].real), 1/ceros[0].real + 1/ceros[1].real, 1]
    elif(len(ceros) == 0):
        num = 1

    #print("numerador: ",num,"\ndenominador: ",den,"\n\n")
    H = signal.TransferFunction(num,den)

    stage.H = H
    stage.loadData()

    return stage
