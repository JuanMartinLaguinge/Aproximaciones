#Importo las funciones a utilizar
from Normalizador import Normalizacion
from desnormalizacion import desnormalizacion
from Chebycheff import Chebyshev_Aprox
from Chebycheff2 import Chebyshev2_Aprox
from butterworth import butterworth

def main():
    #print("Favor de mandar los valores en el siguiente orden:")
    #print("As,Ap,Ws,Wp")bajos
    Wpn,Wan=Normalizacion('Pasa-banda',2e03,1e03,1)
    print("Normalizate, El valor de Wpn es",Wpn,"y el de Wan es",Wan)
   
#Es necesario para poder ejecutar una funcion dentro del archivo
if __name__ == "__main__":
    main()