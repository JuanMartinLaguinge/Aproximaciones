import classEtapa
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from sympy import *
import bodeSym as bS


def acumulative(stageList):
    # esta funcion recive la lista de etapas y devuelve la magnitud acumulada junto con el w
    if(len(stageList)):
        num = 1
        den = 1
        for k in range(len(stageList)):
            num = num*poly(stageList[k].H.num)
            den = den*poly(stageList[k].H.den)
        num = expand(num)
        den = expand(den)

        w, mag = bS.bodeSym(num/den)

    return w , mag



def poly(array):
    n = 0
    s = Symbol('s')
    for k in range(len(array)):
        n = n + array[k]*s**(len(array)-1-k)

    return n
