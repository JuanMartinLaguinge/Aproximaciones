from scipy import signal
import math
import cmath

def crearEtapa(polos,ceros)
# a esta funcion le entras con una lista de polos y ceros y te arma la etapa
# que la etapa seria una funcion transferencia
# logicamente a lo sumo le vas a entrar con 2 ceros y 2 polos

if(len(polos) == 1):    # si solo se mando un polo
    if(im(polos) > 0):  # y tiene parte imaginaria mayor a 0, entonces es un par de polo conjugado
        wo = abs(polos)
        zi = math.cos(re(polos)/wo)
        q = 1/(2*zi)
        den = [1/(wo**2), 1/wo * 1/q, 1]
    else:               # si no tiene parte imaginaria es un solo polo simple
        den = [0, 1/polos, 1]
elif(len(polos) == 2):  # de ultima el user mando 2 polos reales y distintos
    den = [1/(polos[0]*polos[1]), 1/polos[0] + 1/polos[1], 1] # y matematicamente los coeficientes serian esos

if(len(ceros) == 1):
    if(im(ceros) > 0):
        wo = abs(ceros)
        zi = math.cos(re(ceros)/wo)
        q = 1/(2*zi)
        num = [1/(wo**2), 1/wo * 1/q, 1]
    else: 
        num = [0, 1/polos, 1]
elif(len(polos) == 2):
    num = [1/(polos[0]*polos[1]), 1/polos[0] + 1/polos[1], 1]

H = signal.TransferFunction(num,den)

return H