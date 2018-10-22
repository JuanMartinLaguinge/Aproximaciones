import math
from scipy import signal

'''Quiero recibir los Numeradores y Denominadores de la funcion transferencia y
 espero resibir la tension de saturacion(Vmax) y la de ruido (Vmin) en Volts'''
def RangoDinamico(Num,Den,Vmax=0,Vmin=0):
    if Vmax==0:
        Vmax=10
    if Vmin==0:
        Vmin=10e-03
    RangoDin=20*math.log10(Vmax/Vmin)
    Transferencia = signal.lti(Num,Den)
    W,Magnitud,Fase =signal.bode(Transferencia)
    #Me desago de las variable que no uso
    W=0
    Fase=0
    #Al cambiarlas de tipo de variable elimino el espacio de memoria mal gastado
    MaxMagnitud=0
    MinMagnitud=math.inf
    Maxaux=max(Magnitud)
    Minaux=min(Magnitud)
    if Maxaux > MaxMagnitud:
        MaxMagnitud=Maxaux
    if Minaux < MinMagnitud:
        MinMagnitud=Minaux
    PerdidaRangoDin=20*math.log10(MaxMagnitud/MinMagnitud)
    RangoDin-=PerdidaRangoDin
    return RangoDin

def main():
    #RangoDinamico([])
#Es necesario para poder ejecutar una funcion dentro del archivo
if __name__ == "__main__":
    main()