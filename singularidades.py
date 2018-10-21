import classPZ
import math
import cmath


def singularidades(vec):
    # esta funcion le entras con lista de polos o ceros (locos de signal) y te devuelve una lista de la clase que hicimos
    PZ_list=[]
    for k in range (len(vec)):
        if(vec[k].imag >= 0 ):    #solo vamos a agarrar las singularidades con parte imaginaria mayor o igual a 0
            PZ = classPZ.P_Z()
            PZ.real = vec[k].real
            PZ.imag = vec[k].imag
            PZ.sel = 0
            PZ.loadData()
            PZ_list.append(PZ)

    return PZ_list
