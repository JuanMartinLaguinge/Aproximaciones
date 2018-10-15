import math

def Normalizacion(Tipo,Ws_menos,Wp_menos,Ws_mas=0,Wp_mas=0):
    Nor={ 'low-pass': (Ws_menos/Wp_menos), 
    'high-pass': (Wp_menos/Ws_menos), 
    'bandwidth-pass': ( (Ws_mas-Ws_menos) / (Wp_mas-Wp_menos) ),
    'Rechaza-banda': ( (Wp_mas-Wp_menos) / (Ws_mas-Ws_menos) )}
    if( Ws_menos*Ws_mas != Wp_mas*Wp_menos ):
        if Tipo=='Pasa-banda':
            Ws=Wp_mas*Wp_menos/Ws_mas
            if Ws_menos<Ws:
                Ws_menos=Ws
                Nor[Tipo]=( (Ws_mas-Ws_menos) / (Wp_mas-Wp_menos) )
            Ws=Wp_mas*Wp_menos/Ws_menos
            if Ws_mas>Ws:
                Ws_mas=Ws
                Nor[Tipo]=( (Ws_mas-Ws_menos) / (Wp_mas-Wp_menos) )
            else:
                print("Error:No se puedo realizar la simetria del Pasa-banda")
        else:
            Wp=Ws_mas*Ws_menos/Wp_mas
            if Wp_menos<Wp:
                Wp_menos=Wp
                Nor[Tipo]=( (Ws_mas-Ws_menos) / (Wp_mas-Wp_menos) )
            Wp=Ws_mas*Ws_menos/Wp_menos
            if Wp_mas>Wp:
                Wp_mas=Wp
                Nor[Tipo]=( (Ws_mas-Ws_menos) / (Wp_mas-Wp_menos) )
            else:
                print("Error:No se puedo realizar la simetria del Rechaza-banda")
    Ws_Nor=Nor[Tipo]
    Wp_Nor=1
    return Wp_Nor,Ws_Nor