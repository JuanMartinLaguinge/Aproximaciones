from math import *
from sympy import *

def desnormalizacion(tipo,ceros,polos,wp,wp_mas = 0,const = 1):
    s = Symbol('s')
    num = 1
    den = 1
    for k in range (0,len(ceros)):
        num = num*(s-ceros[k])  #tenemos el numerador de la funcion transf norm
    for k in range (0,len(polos)):
        den = den*(s-polos[k])  #tenemos el denominador de la funcion transf norm
    num = expand(num).subs(I,0)
    den = expand(den).subs(I,0)
    H_nor = num/den
    k = H_nor.subs(s,0) #k es la constante que queda mutiplicando al H en formato normalizado
    H_nor = H_nor/k*const     #al sacarle esa constante hacemos que la funcion no tenga ganancia constante
    if(tipo == 'low-pass'):
        H_denor = H_nor.subs(s,s/wp)
    elif(tipo == 'high-pass'):
        H_denor = H_nor.subs(s,wp/s)
    elif(tipo == 'band-pass'):
        wo = sqrt(wp*wp_mas)
        B = (wp_mas - wp)/wo
        print("wo = ",wo,"\nB = ",B)
        H_denor = H_nor.subs(s,1/B * (s/wo + wo/s))
    elif(tipo == 'band-stop'):
        wo = sqrt(wp*wp_mas)
        B = (wp_mas - wp)/wo
        H_denor = H_nor.subs(s,1/(1/B * (s/wo + wo/s)))

    #############ya tenemos la funcion denormalizada##################

    H_denor = simplify(H_denor)
    num,den = fraction(H_denor)
    num = expand(num)
    den = expand(den)
    #print("numerador",num,"   denomunador ",den)
    if(num == num.subs(s,1234567890)):         #si n no tiene s cuando lo mandes al Poli de rompe
        num_coeffs = float(num)                #si se cumple eso en num no hay s
    else:
        num_pol = Poly(num.subs(I,0))
        num_coeffs = num_pol.all_coeffs()
    if(den == den.subs(s,1234567890)):         #le pongo ese numero porque pinto
        den_coeffs = float(den)
    else:
        den_pol = Poly(den.subs(I,0))          #mando la parte imaginaria a 0 porque python tiene problemas
        den_coeffs = den_pol.all_coeffs()       #y como son conjugados los polos la parte imaginaria tiene que ser 0
                                                #cuando se expande la expresion
    return num_coeffs,den_coeffs
