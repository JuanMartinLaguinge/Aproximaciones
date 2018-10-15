def butterworth(Ap,wp,Aa,wa,wp_mas=0,wa_mas=0):
    #las variables wp_mas y ws_mas son para hacer bandas
    wan = normalizacion(wp,wa,wp_mas,wa_mas) #ya tenemos el wan, todo normalizado
    E = sqrt(10**(Ap/10) - 1)
    #print("E = ",E,"\n")
    n = math.log10(sqrt(10**(Aa/10 - 1)) / E) / math.log10(wan)
    n = int(n) + 1
    #print("n = ",n,"\n")
    radio = math.pow(E,-1/n)
    #print("radio = ",radio,"\n")
    ang = math.pi/n
    ceros = []
    polos = []

    phase_ini = math.pi/2 + ang/2

    for k in range (0,n):
        a = cmath.rect(radio, phase_ini + k*ang)
        polos.append(round(re(a),6) + I*round(im(a),6))
        print("polo = ",polos[k],"\n")

    return ceros,polos