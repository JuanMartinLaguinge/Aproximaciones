from math import *
from sympy import *
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

def bodeSym(sym):
    # esta funcion recibe una ecuacion simbolica y te saca el bode
    sym = simplify(sym)
    num, den = fraction(sym)
    num = expand(num)
    den = expand(den)
    if(num == num.subs(s,1234567890)):        
        num_coeffs = float(num)                
    else:
        num_pol = Poly(num)
        num_coeffs = num_pol.all_coeffs()
    if(den == den.subs(s,1234567890)):         
        den_coeffs = float(den)
    else:
        den_pol = Poly(den)          
        den_coeffs = den_pol.all_coeffs()       

    n = np.array(num_coeffs).astype(np.float64)
    d = np.array(den_coeffs).astype(np.float64)

    H = signal.TransferFunction(n,d)

    w,mag,pha = signal.bode(H)
    return w, mag