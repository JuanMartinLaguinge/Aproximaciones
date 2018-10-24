#TP4 Teoria de Cirucitos.

#La GUI de este programa funciona a través de pasos. Es decir, a medida que el usuario va haciendo los pasos que se
#le indica, el siguiente paso aparece.

import math
import matplotlib
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk as toolbar
from matplotlib.figure import Figure
import matplotlib.patches as patches #para plotear la plantilla en el plot.
from scipy import signal
from singularidades import singularidades as sing
from Aproximador import AproximadorFiltro
from crearEtapa import crearEtapa
from classEtapa import Etapa
from automatizacion import automatizacion as auto
from acumulative import acumulative as acum_bode

class Gui:
    def reset_button_color(self): #pone todos los botones en el color que simboliza como NO precionado (gris).
        if(self.step <= 1):
            self.b_LP.configure(bg="light gray")
            self.b_HP.configure(bg="light gray")
            self.b_BP.configure(bg="light gray")
            self.b_BS.configure(bg="light gray")
            self.b_GD.configure(bg="light gray")
        if(self.step <= 2):
            self.b_butter.configure(bg="light gray")
            self.b_cheby_I.configure(bg="light gray")
            self.b_cheby_II.configure(bg="light gray")
            self.b_bess.configure(bg="light gray")
            self.b_graph.configure(bg="light gray")
            self.b_graph.configure(bg="light gray")
        if(self.step <= 3):
            self.b_attenuation.configure(bg="light gray")
            self.b_phase.configure(bg="light gray")
            self.b_zp.configure(bg="light gray")
            self.b_step.configure(bg="light gray")
            self.b_impulse.configure(bg="light gray")
            if(self.screen != 0):
                self.b_screen1.configure(bg="light gray")
            if(self.screen != 1):
                self.b_screen2.configure(bg="light gray")
            self.b_s_stage.configure(bg="light gray")
            self.b_s_stages.configure(bg="light gray")
            self.b_st_attenuation.configure(bg="light gray")
            self.b_sts_attenuation.configure(bg="light gray")
            self.b_data.configure(bg="light gray")
            self.b_delete.configure(bg="light gray")

    def clear_screen(self): #limpia la pantalla eliminando botones, labels, listboxes, etc.
        self.text1.place_forget()
        self.b_LP.place_forget()
        self.b_HP.place_forget()
        self.b_BP.place_forget()
        self.b_BS.place_forget()
        self.b_GD.place_forget()
        self.text2.place_forget()
        self.b_butter.place_forget()
        self.b_cheby_I.place_forget()
        self.b_cheby_II.place_forget()
        self.b_bess.place_forget()
        self.text3.place_forget()
        self.Ap.place_forget()
        self.Ap_val.place_forget()
        self.fp.place_forget()
        self.fp_val.place_forget()
        self.As.place_forget()
        self.As_val.place_forget()
        self.fs.place_forget()
        self.fs_val.place_forget()
        self.fp1.place_forget()
        self.fp1_val.place_forget()
        self.fs1.place_forget()
        self.fs1_val.place_forget()
        self.n.place_forget()
        self.n_val.place_forget()
        self.nmin.place_forget()
        self.nmin_val.place_forget()
        self.nmax.place_forget()
        self.nmax_val.place_forget()
        self.qmax.place_forget()
        self.qmax_val.place_forget()
        self.rank.place_forget()
        self.rank_val.place_forget()
        self.delay.place_forget()
        self.delay_val.place_forget()
        self.fgd.place_forget()
        self.fgd_val.place_forget()
        self.tol.place_forget()
        self.tol_val.place_forget()
        self.b_graph.place_forget()
        self.b_attenuation.place_forget()
        self.b_phase.place_forget()
        self.b_zp.place_forget()
        self.b_step.place_forget()
        self.b_impulse.place_forget()
        self.b_screen1.place_forget()
        self.b_screen2.place_forget()
        self.zp.place_forget()
        self.zlist.place_forget()
        self.zscroll.place_forget()
        self.plist.place_forget()
        self.pscroll.place_forget()
        self.b_s_stage.place_forget()
        self.b_s_stages.place_forget()
        self.st.place_forget()
        self.stlist.place_forget()
        self.stscroll.place_forget()
        self.b_st_attenuation.place_forget()
        self.b_sts_attenuation.place_forget()
        self.b_data.place_forget()
        self.b_delete.place_forget()
        self.st_data.place_forget()
        self.data.place_forget()

    def update_zp_listboxes(self): #actualiza los listboxes de los ceros y polos.
        #primero se limpian las listas
        self.zlist.delete(0,tk.END)
        self.plist.delete(0,tk.END)
        self.stage_z_str.clear()
        self.stage_p_str.clear()
        #luego se las rellena con los datos actualizados.
        k = 1
        for i in range(len(self.zlist_val)):
            if(self.zlist_val[i].imag != 0):
                self.stage_z_str.append("z"+str(2*i+k)+",z"+str(2*i+k+1))
                if(self.zlist_val[i].sel == 0):
                    self.zlist.insert(i,str(self.stage_z_str[i])+" f="+str(self.zlist_val[i].fo)+"Hz Q="+str(self.zlist_val[i].Q))
                else:
                    self.zlist.insert(i,str(self.stage_z_str[i])+" f="+str(self.zlist_val[i].fo)+"Hz Q="+str(self.zlist_val[i].Q)+" (used)")
            else:
                self.stage_z_str.append("z"+str(2*i+1))
                if(self.zlist_val[i].sel == 0):
                    self.zlist.insert(i,str(self.stage_z_str[i])+" f="+str(self.zlist_val[i].fo)+"Hz Q="+str(self.zlist_val[i].Q))
                else:
                    self.zlist.insert(i,str(self.stage_z_str[i])+" f="+str(self.zlist_val[i].fo)+"Hz Q="+str(self.zlist_val[i].Q)+" (used)")
                k = 0
        self.zlist.insert(tk.END,"none")
        k = 1
        for i in range(len(self.plist_val)):
            if(self.plist_val[i].imag != 0):
                self.stage_p_str.append("p"+str(2*i+k)+",p"+str(2*i+k+1))
                if(self.plist_val[i].sel == 0):
                    self.plist.insert(i,str(self.stage_p_str[i])+" f="+str(self.plist_val[i].fo)+"Hz Q="+str(self.plist_val[i].Q))
                else:
                    self.plist.insert(i,str(self.stage_p_str[i])+" f="+str(self.plist_val[i].fo)+"Hz Q="+str(self.plist_val[i].Q)+" (used)")
            else:
                self.stage_p_str.append("p"+str(2*i+1))
                if(self.plist_val[i].sel == 0):
                    self.plist.insert(i,str(self.stage_p_str[i])+" f="+str(self.plist_val[i].fo)+"Hz Q="+str(self.plist_val[i].Q))
                else:
                    self.plist.insert(i,str(self.stage_p_str[i])+" f="+str(self.plist_val[i].fo)+"Hz Q="+str(self.plist_val[i].Q)+" (used)")
                k = 0
        self.plist.insert(tk.END,"none")

    def update_state_listbox(self): #actualiza el listbox de los estados que se van seleccionando.
        self.stlist.delete(0,tk.END) #se borra el contenido viejo.
        for i in range(len(self.stage_list)):
            self.stlist.insert(i,"Stage"+str(i+1)+" ("+str(self.stage_zp_str[i])+")") #se coloca el contenido nuevo.

    def update_screen(self): #actualiza la pantalla mostrando los botones correspondientes al paso en el que el usuario se encuentra. 
        self.clear_screen()
        self.warning.place_forget()
        if(self.screen == 0):
            if(self.step < 3):
                self.plt.clear()
                self.fig.suptitle("")
                self.data_plt.draw()
            self.text1.place(x=700,y=15)
            self.b_LP.place(x=700,y=45)
            self.b_HP.place(x=762,y=45)
            self.b_BP.place(x=828,y=45)
            self.b_BS.place(x=895,y=45)
            self.b_GD.place(x=963,y=45)
            if(self.step > 0):
                self.text2.place(x=700,y=90)
                if(self.filter_type != "group delay"):
                    self.b_butter.place(x=700,y=120)
                    self.b_cheby_I.place(x=777,y=120)
                    self.b_cheby_II.place(x=855,y=120)
                else:
                    self.b_bess.place(x=700,y=120)
            if(self.step > 1):
                self.text3.place(x=700,y=165)
                if(self.filter_type != "group delay"):
                    self.Ap.place(x=700,y=195)
                    self.Ap_val.place(x=760,y=195)
                    self.As.place(x=700,y=225)
                    self.As_val.place(x=760,y=225)
                    self.rank.place(x=850,y=285)
                    self.rank_val.place(x=920,y=285)
                    if(self.filter_type == "low pass" or self.filter_type == "high pass"):
                        self.fp.configure(text = "fp(Hz) = ")
                        self.fp.place(x=850,y=195)
                        self.fp_val.place(x=920,y=195)
                        self.fs.configure(text = "fs(Hz) = ")
                        self.fs.place(x=850,y=225)
                        self.fs_val.place(x=920,y=225)
                    if(self.filter_type == "band pass" or self.filter_type == "band stop"):
                        self.fp.configure(text = "fp-(Hz) = ")
                        self.fp.place(x=850,y=195)
                        self.fp_val.place(x=920,y=195)
                        self.fs.configure(text = "fs-(Hz) = ")
                        self.fs.place(x=850,y=225)
                        self.fs_val.place(x=920,y=225)
                        self.fp1.place(x=1010,y=195)
                        self.fp1_val.place(x=1072,y=195)
                        self.fs1.place(x=1010,y=225)
                        self.fs1_val.place(x=1072,y=225)
                if(self.filter_type == "group delay"):
                    self.delay.place(x=700,y=195)
                    self.delay_val.place(x=760,y=195)
                    self.fgd.place(x=850,y=195)
                    self.fgd_val.place(x=920,y=195)
                    self.tol.place(x=1010,y=195)
                    self.tol_val.place(x=1072,y=195)
                self.b_graph.place(x=700,y=350)
                self.n.place(x=700,y=255)
                self.n_val.place(x=760,y=255)
                self.nmin.place(x=850,y=255)
                self.nmin_val.place(x=920,y=255)
                self.nmax.place(x=1010,y=255)
                self.nmax_val.place(x=1072,y=255)
                self.qmax.place(x=700,y=285)
                self.qmax_val.place(x=760,y=285)
            if(self.step > 2):
                self.b_attenuation.place(x=10, y=15)
                self.b_phase.place(x=125, y=15)
                self.b_zp.place(x=208, y=15)
                self.b_step.place(x=295, y=15)
                self.b_impulse.place(x=385, y=15)
                self.b_screen1.place(x=10, y=545)
                self.b_screen2.place(x=125, y=545)
        if(self.screen == 1 and self.step > 2):
            self.b_screen1.place(x=10, y=545)
            self.b_screen2.place(x=125, y=545)
            self.zp.place(x=700,y=15)
            self.b_zp.place(x=10, y=15)
            self.zlist.place(x=700,y=45)
            self.zscroll.place(x=903, y=45)
            self.plist.place(x=955,y=45)
            self.pscroll.place(x=1158, y=45)
            self.b_s_stage.place(x=700,y=200)
            self.b_s_stages.place(x=700,y=235)
            self.st.place(x=700,y=280)
            self.stlist.place(x=700,y=310)
            self.stscroll.place(x=825,y=310)
            if(len(self.stage_list) != 0):
                self.b_st_attenuation.place(x=100, y=15)
                self.b_sts_attenuation.place(x=250, y=15)
                self.b_data.place(x=850, y=310)
                self.b_delete.place(x=850, y=350)

    def plot_attenuation(self): #se plotea la atenuación en bode de la función transferencia junto con la plantilla.
        self.reset_button_color()
        self.b_attenuation.configure(bg="olive drab")
        self.plt.clear()
        self.plt.semilogx(self.f,(-1)*self.mag)
        self.fig.suptitle("Attenuation (Bode)")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Frequency (Hz)") #"$Frequency (Hz)$" -> con los '$' se cambia la letra a cursiva.
        self.plt.set_ylabel("Attenuation (dB)") #_{out} -> pone out en letra chica y abajo.

        #se plotea la plantilla.
        if(self.filter_type == "low pass"):
            self.plt.add_patch(patches.Rectangle((self.axes.get_xlim()[0], float(self.Ap_val.get())), float(self.fp_val.get())-self.axes.get_xlim()[0], self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))
            self.plt.add_patch(patches.Rectangle((float(self.fs_val.get()), self.axes.get_ylim()[0]), self.axes.get_xlim()[1]-float(self.fs_val.get()), float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))
        if(self.filter_type == "high pass"):
            self.plt.add_patch(patches.Rectangle((self.axes.get_xlim()[0], self.axes.get_ylim()[0]), float(self.fs_val.get())-self.axes.get_xlim()[0], float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))
            self.plt.add_patch(patches.Rectangle((float(self.fp_val.get()), float(self.Ap_val.get())), self.axes.get_xlim()[1]-float(self.fp_val.get()), self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))  
        if(self.filter_type == "band pass"):
            self.plt.add_patch(patches.Rectangle((self.axes.get_xlim()[0], self.axes.get_ylim()[0]), float(self.fs_val.get())-self.axes.get_xlim()[0], float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))
            self.plt.add_patch(patches.Rectangle((float(self.fp_val.get()), float(self.Ap_val.get())), float(self.fp1_val.get())-float(self.fp_val.get()), self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))      
            self.plt.add_patch(patches.Rectangle((float(self.fs1_val.get()), self.axes.get_ylim()[0]), self.axes.get_xlim()[1]-float(self.fs1_val.get()), float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))
        if(self.filter_type == "band stop"):
            self.plt.add_patch(patches.Rectangle((self.axes.get_xlim()[0], float(self.Ap_val.get())), float(self.fp_val.get())-self.axes.get_xlim()[0], self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))
            self.plt.add_patch(patches.Rectangle((float(self.fs_val.get()), self.axes.get_ylim()[0]), float(self.fs1_val.get())-float(self.fs_val.get()), float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))            
            self.plt.add_patch(patches.Rectangle((float(self.fp1_val.get()), float(self.Ap_val.get())), self.axes.get_xlim()[1]-float(self.fp1_val.get()), self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))            
        self.data_plt.draw()

    def plot_phase(self): #plotea la fase en bode de la función transferencia.
        self.reset_button_color()
        self.b_phase.configure(bg="olive drab")
        self.plt.clear()
        self.plt.semilogx(self.f,self.phase)
        self.fig.suptitle("Phase (Bode)")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Frequency (Hz)")
        self.plt.set_ylabel("Phase (Deg)")
        self.data_plt.draw()

    def plot_zp(self): #plotea los polos y ceros de la función transferencia y nombra cada uno de ellos.
        self.reset_button_color()
        self.b_zp.configure(bg="olive drab")
        self.plt.clear()
        self.plt.scatter(self.H.zeros.real,self.H.zeros.imag, marker = 'o', color = "red")
        for i in range(len(self.H.zeros)):
            self.plt.annotate("z"+str(i+1),xy=(self.H.zeros[i].real,self.H.zeros[i].imag))
        self.plt.scatter(self.H.poles.real,self.H.poles.imag, marker = 'x', color = "blue")
        for i in range(len(self.H.poles)):
            self.plt.annotate("p"+str(i+1),xy=(self.H.poles[i].real,self.H.poles[i].imag))
            
        self.fig.suptitle("Zeros & Poles")    
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Real Part")
        self.plt.set_ylabel("Imaginary Part")
        self.data_plt.draw()

    def plot_step(self): #plotea la respuesta al escalon u(t) de la señal.
        self.reset_button_color()
        self.b_step.configure(bg="olive drab")
        self.plt.clear() #simpre limpiar antes de plotear.
        self.plt.plot(self.stepT,self.stepMag) #stepT -> tiempo. stepMag -> tension de la respuesta al escalón.
        self.fig.suptitle("Step Response")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Time (sec)")
        self.plt.set_ylabel("Voltage (V)")
        self.data_plt.draw()

    def plot_impulse(self): #plotea la respuesta al impulso (delta de dirac) de la señal.
        self.reset_button_color()
        self.b_impulse.configure(bg="olive drab")
        self.plt.clear()
        self.plt.plot(self.impT,self.impMag) #impT -> tiempo. impMag -> tension de la respuesta al impulso
        self.fig.suptitle("Impulse Response")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Time (sec)")
        self.plt.set_ylabel("Voltage (V)")
        self.data_plt.draw() 

    def set_low_pass(self): #se selecciona el filtro pasa bajos y se completa el primer paso.
        self.step = 1
        self.reset_button_color()
        self.b_LP.configure(bg="olive drab")
        self.filter_type = "low pass"  
        self.update_screen()

    def set_high_pass(self): #se selecciona el filtro pasa altos y se completa el primer paso.
        self.step = 1
        self.reset_button_color()
        self.b_HP.configure(bg="olive drab")
        self.filter_type = "high pass"
        self.update_screen()

    def set_band_pass(self): #se selecciona el filtro pasa banda y se completa el primer paso.
        self.step = 1
        self.reset_button_color()
        self.b_BP.configure(bg="olive drab")
        self.filter_type = "band pass"
        self.update_screen()

    def set_band_stop(self): #se selecciona el filtro rechaza banda y se completa el primer paso.
        self.step = 1
        self.reset_button_color()
        self.b_BS.configure(bg="olive drab")
        self.filter_type = "band stop"
        self.update_screen()
    
    def set_group_delay(self): #se selecciona el filtro rechaza banda y se completa el primer paso.
        self.step = 1
        self.reset_button_color()
        self.b_GD.configure(bg="olive drab")
        self.filter_type = "group delay"
        self.update_screen()

    def set_butter(self): #se selecciona la aproximación de butterworth y se completa el segundo paso.
        self.step = 2
        self.reset_button_color()
        self.b_butter.configure(bg="olive drab")
        self.approx_type = "butterworth"  
        self.update_screen()

    def set_cheby_I(self): #se selecciona la aproximación de chebyshev y se completa el segundo paso.
        self.step = 2
        self.reset_button_color()
        self.b_cheby_I.configure(bg="olive drab")
        self.approx_type = "chebyshev I"
        self.update_screen()

    def set_cheby_II(self): #se selecciona la aproximación de chebychev inverso y se completa el segundo paso.
        self.step = 2
        self.approx_type = "chebyshev II"
        self.reset_button_color()
        self.b_cheby_II.configure(bg="olive drab")
        self.update_screen()

    def set_bess(self): #se selecciona la aproximación de bessel y se completa el segundo paso.
        self.step = 2
        self.reset_button_color()
        self.b_bess.configure(bg="olive drab")
        self.approx_type = "bessel"
        self.update_screen()

    def start_graph(self): #se verifica que las especificaciones ingresas son validas y plotea la aproximación en atenuación junto con la plantilla.
        if(self.filter_type != "band pass" and self.filter_type != "band stop"):
            self.fp1_val.delete(0, tk.END)
            self.fs1_val.delete(0, tk.END)
        if(len(self.fp1_val.get()) == 0 and len(self.fs1_val.get()) == 0):
            self.fp1_val.insert(0,"0")
            self.fs1_val.insert(0,"0")
        if(len(self.nmin_val.get()) == 0 and len(self.nmax_val.get()) == 0):
            self.nmin_val.insert(0,"0")
            self.nmax_val.insert(0,"0")
        if(len(self.n_val.get()) == 0):
            self.n_val.insert(0,"0")
        if(len(self.qmax_val.get()) == 0):
            self.qmax_val.insert(0,"0")
        if(len(self.rank_val.get()) == 0):
            self.rank_val.insert(0,"0")
        try: #se fija si alguna de las especificaciones está vacio o no es un número.
            float(self.n_val.get())
            float(self.nmin_val.get())
            float(self.nmax_val.get())
            float(self.qmax_val.get())
            float(self.rank_val.get())
            if(self.filter_type != "group delay"):
                float(self.Ap_val.get())
                float(self.As_val.get())
                float(self.fp_val.get())
                float(self.fs_val.get())
                if(self.filter_type == "band pass" or self.filter_type == "band stop"):
                    float(self.fp1_val.get())
                    float(self.fs1_val.get())
            else:
                float(self.delay_val.get())
                float(self.fgd_val.get())
                float(self.tol_val.get())
        except ValueError:
            self.warning.configure(text="WARNING: Fill all the specifications with valid numbers.")
            self.warning.place(x=700,y=520)
            return
        #se sigue testeando los datos ingresados por el usuario y si son erroneos, se muestra un WARNING.
        if(self.filter_type != "group delay"):
            if(float(self.Ap_val.get()) >= float(self.As_val.get())): #se fija si Ap >= AS.
                self.warning.configure(text="WARNING: Be sure that... Ap < As.")
                self.warning.place(x=700,y=520)
                return
            if(float(self.fp_val.get()) == 0 or float(self.fs_val.get()) == 0): #se fija si alguna frecuencia es nula.
                self.warning.configure(text="WARNING: Frequency must not be zero.")
                self.warning.place(x=700,y=520)
                return
            if(self.filter_type == "band pass" or self.filter_type == "band stop"):
                if(float(self.fp_val.get()) == 0 or float(self.fs_val.get()) == 0): #se fija si alguna frecuencia es nula. 
                    self.warning.configure(text="WARNING: Frecuency must not be zero.")
                    self.warning.place(x=700,y=520)
                    return
            if(self.filter_type == "low pass"):
                if(float(self.fp_val.get()) >= float(self.fs_val.get())): #se fija si en pasa bajos fp >= fs.
                    self.warning.configure(text="WARNING: Low Pass Filter: Be sure that... fp < fs.")
                    self.warning.place(x=700,y=520)
                    return
            if(self.filter_type == "high pass"): 
                if(float(self.fp_val.get()) <= float(self.fs_val.get())): #se fija si en pasa altos fs >= fp.
                    self.warning.configure(text="WARNING: High Pass Filter: Be sure that... fs < fp.")
                    self.warning.place(x=700,y=520)
                    return
            if(self.filter_type == "band pass"):
                if(not (float(self.fs_val.get()) < float(self.fp_val.get()) and float(self.fp_val.get()) < float(self.fp1_val.get()) and float(self.fp1_val.get()) < float(self.fs1_val.get()))):
                    self.warning.configure(text="WARNING: Band Pass Filter: Be sure that... fs- < fp- < fp+ < fs+.")
                    self.warning.place(x=700,y=520)
                    return
            if(self.filter_type == "band stop"):
                if(not (float(self.fp_val.get()) < float(self.fs_val.get()) and float(self.fs_val.get()) < float(self.fs1_val.get()) and float(self.fs1_val.get()) < float(self.fp1_val.get()))):
                    self.warning.configure(text="WARNING: Band Stop Filter: Be sure that... fp- < fs- < fs+ < fp+.")
                    self.warning.place(x=700,y=520)
                    return
        if(float(self.n_val.get()) != 0 and float(self.nmin_val.get()) != 0 and float(self.nmax_val.get()) != 0):
            self.warning.configure(text="WARNING: Especifications N, Nmin and Nmax can't be together.")
            self.warning.place(x=700,y=520)
            return
        if(float(self.n_val.get()) != 0 and float(self.nmax_val.get()) != 0):
            self.warning.configure(text="WARNING: Especifications N and Nmax can't be together.")
            self.warning.place(x=700,y=520)
            return
        if(float(self.n_val.get()) != 0 and float(self.nmin_val.get()) != 0):
            self.warning.configure(text="WARNING: Especifications N and Nmin can't be together.")
            self.warning.place(x=700,y=520)
            return
        if(float(self.nmin_val.get()) == 0 and float(self.nmax_val.get()) != 0 ):
            self.warning.configure(text="WARNING: Especifications Nmin and Nmax must be together.")
            self.warning.place(x=700,y=520)
            return
        if(float(self.nmin_val.get()) != 0 and float(self.nmax_val.get()) == 0 ):
            self.warning.configure(text="WARNING: Especifications Nmin and Nmax must be together.")
            self.warning.place(x=700,y=520)
            return

        #si todo esta bien en las especificaciones, se borra el mensaje de error y se completa el tercer paso.
        self.warning.place_forget()
        self.step = 3
        self.reset_button_color()
        self.b_graph.configure(bg="olive drab")
        self.b_screen1.configure(bg="olive drab")

        print(self.filter_type)

        #como las especificaciones del filtro retardo de grupo (group delay) son diferentes a las demás, se las separan.
        if(self.filter_type != "group delay"):
            self.approx_F.Datos(self.approx_type, float(self.Ap_val.get()), float(self.As_val.get()), float(self.fp_val.get())*2*math.pi, float(self.fs_val.get())*2*math.pi, float(self.fp1_val.get())*2*math.pi, float(self.fs1_val.get())*2*math.pi,float(self.rank_val.get()),float(self.qmax_val.get()),float(self.n_val.get()),float(self.nmin_val.get()),float(self.nmax_val.get()))
        else:
            self.approx_F.DatosRetard(self.approx_type, float(self.delay_val.get())/(10**6), float(self.fgd_val.get())*2*math.pi, float(self.tol_val.get())/100, float(self.qmax_val.get()),float(self.n_val.get()),float(self.nmin_val.get()),float(self.nmax_val.get()))

        num, den = self.approx_F.Aproximacion() #se realiza la aproximación

        numAux = []
        denAux = []
        
        #se asegura que la lista num y den sean tipo float.
        if(type(num) != float):
            for k in range(len(num)):
                numAux.append(float(num[k]))
        else:
            numAux.append(num)
        if(type(den) != float):
            for k in range(len(den)):
                denAux.append(float(den[k]))
        else:
            denAux.append(den)

        self.H = signal.TransferFunction(numAux, denAux) #se crea la función transferencia.
        w, self.mag, self.phase = signal.bode(self.H) #el w está en rad/seg.
        self.f = w/(2*math.pi) #convierto a Hz.
        self.stepT, self.stepMag = signal.step(self.H)
        self.impT, self.impMag = signal.impulse(self.H)

        #se limpia (resetea) las listas.
        self.zlist_val.clear()
        self.plist_val.clear()
        self.stlist.delete(0,tk.END)
        self.stage_zp_str.clear()
        self.stage_list.clear()

        #se obtienen los polos y ceros efectivos de la función transferencia y se actualizan los listboxes.
        self.zlist_val = sing(self.H.zeros)
        self.plist_val = sing(self.H.poles)
        self.update_zp_listboxes()

        self.plot_attenuation()
        self.update_screen() #refrezca la pantalla para que aparezcan los botones.
        
    def set_screen1(self): #actualiza la página para setear la página uno (donde estan las especificaciones y plots)
        if(self.screen != 0):
            self.screen = 0
            self.update_screen()
            self.reset_button_color()
            self.b_screen1.configure(bg="olive drab")    
            self.plot_attenuation()
            
    def set_screen2(self): #actualiza la página para setear la página dos (donde estan las etapas)
        if(self.screen != 1):
            self.screen = 1
            self.update_screen()
            self.reset_button_color()
            self.b_screen2.configure(bg="olive drab")
            self.plot_zp()

    def set_stage(self): #se crea una estapa con los polos y ceros seleccionados.
        #se testea si hay algún error en la elección de polos y ceros.
        if(self.zlist.curselection() == () or self.plist.curselection() == ()):
            self.warning.configure(text="WARNING: Select a valid item from the listboxes.")
            self.warning.place(x=700,y=520)
            return
        if(self.zlist.curselection()[0] == len(self.zlist_val) and self.plist.curselection()[0] == len(self.plist_val)):
            self.warning.configure(text="WARNING: Select a valid item from the listboxes.")
            self.warning.place(x=700,y=520)
            return
        if(self.zlist.curselection()[0] != len(self.zlist_val)):
            if(self.zlist_val[self.zlist.curselection()[0]].sel == 1):
                self.warning.configure(text="WARNING: An used item can't be selected.")
                self.warning.place(x=700,y=520)
                return
        if(self.plist.curselection()[0] != len(self.plist_val)):
            if(self.plist_val[self.plist.curselection()[0]].sel == 1):
                self.warning.configure(text="WARNING: An used item can't be selected.")
                self.warning.place(x=700,y=520)
                return

        #si todo esta bien, se borra el mensaje de error y se colocan como usados los polos y ceros selecionados.
        self.warning.place_forget()
        if(self.zlist.curselection()[0] != len(self.zlist_val)):
            self.zlist_val[self.zlist.curselection()[0]].sel = 1
        if(self.plist.curselection()[0] != len(self.plist_val)):
            self.plist_val[self.plist.curselection()[0]].sel = 1

        if(self.zlist.curselection()[0] == len(self.zlist_val)):
            self.stage_list.append(crearEtapa([self.plist_val[self.plist.curselection()[0]]], []))
            self.stage_zp_str.append(str(self.stage_p_str[self.plist.curselection()[0]]))
            self.stlist.insert(len(self.stage_list)-1,"Stage"+str(len(self.stage_list))+" ("+str(self.stage_zp_str[len(self.stage_list)-1])+")")
        elif(self.plist.curselection()[0] == len(self.plist_val)):
            self.stage_list.append(crearEtapa([], [self.zlist_val[self.zlist.curselection()[0]]]))
            self.stage_zp_str.append(str(self.stage_z_str[self.plist.curselection()[0]]))
            self.stlist.insert(len(self.stage_list)-1,"Stage"+str(len(self.stage_list))+" ("+str(self.stage_zp_str[len(self.stage_list)-1])+")")
        else:
            self.stage_list.append(crearEtapa([self.plist_val[self.plist.curselection()[0]]], [self.zlist_val[self.zlist.curselection()[0]]]))
            self.stage_zp_str.append(str(str(self.stage_z_str[self.plist.curselection()[0]])+"/"+str(self.stage_p_str[self.plist.curselection()[0]])))
            self.stlist.insert(len(self.stage_list)-1,"Stage"+str(len(self.stage_list))+" ("+str(self.stage_zp_str[len(self.stage_list)-1])+")")
        self.update_zp_listboxes()
        self.update_screen()

    def set_stages(self): #se crean las etapas que conforman el filtro automaticamente.
        self.stage_list.clear()

        self.stage_list = auto(self.zlist_val, self.plist_val)
        self.update_zp_listboxes()

        #se limpian las listas.
        self.stage_z_str.clear()
        self.stage_p_str.clear()
        self.stage_zp_str.clear()

        #se llenan las listas con los correspondientes datos.
        for j in range(len(self.stage_list)):
            print(len(self.zlist_val))
            k = 1
            for i in range(len(self.zlist_val)):
                if(round(self.zlist_val[i].real,5) == round(self.stage_list[j].H.zeros[0].real,5)):
                    if(round(self.zlist_val[i].imag,5) == round(self.stage_list[j].H.zeros[0].imag,5)):
                        if(self.zlist_val[i].imag != 0):
                            self.stage_z_str.append("z"+str(2*i+k)+",z"+str(2*i+k+1))
                        else:
                            self.stage_z_str.append("z"+str(2*i+1))
                            k = 0
            k = 1
            for i in range(len(self.plist_val)):
                if(round(self.plist_val[i].real,5) == round(self.stage_list[j].H.poles[0].real,5)):
                    if(round(self.plist_val[i].imag,5) == round(self.stage_list[j].H.poles[0].imag,5)):
                        if(self.plist_val[i].imag != 0):
                            self.stage_p_str.append("p"+str(2*i+k)+",p"+str(2*i+k+1))
                        else:
                            self.stage_p_str.append("p"+str(2*i+1))
                            k = 0
                        
                            
            if(len(self.stage_z_str) == 0):
                self.stage_zp_str.append(str(self.stage_p_str[j]))
            elif(len(self.stage_p_str) == 0):
                self.stage_zp_str.append(str(self.stage_z_str[j]))
            else:
                self.stage_zp_str.append(str(self.stage_z_str[j])+"/"+str(self.stage_p_str[j]))

        self.update_state_listbox()
        self.update_screen()
            
    def plot_stage_attenuation(self): #plotea la atenuación de la etapa seleccionada.
        #si no hay etapa seleccionada, WARNING.
        if(self.stlist.curselection() == ()):
            self.warning.configure(text="WARNING: No stage selected.")
            self.warning.place(x=700,y=520)
            return
        self.warning.place_forget()
        self.reset_button_color()
        self.b_st_attenuation.configure(bg="olive drab")
        self.plt.clear()
        w, mag, pha = signal.bode(self.stage_list[self.stlist.curselection()[0]].H)
        self.plt.semilogx(w/(2*math.pi),(-1)*mag)
        self.fig.suptitle("Stage"+str(self.stlist.curselection()[0]+1)+" Attenuation (Bode)")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Frequency (Hz)") #"$Frequency (Hz)$" -> con los '$' se cambia la letra a cursiva.
        self.plt.set_ylabel("Attenuation (dB)") #_{out} -> pone out en letra chica y abajo.
        self.data_plt.draw()

    def plot_stages_attenuation(self): #plotea la atenuación acumulada de las estapas que se encuentran en el listbox.
        self.reset_button_color()
        self.b_sts_attenuation.configure(bg="olive drab")
        self.plt.clear()
        w, mag = acum_bode(self.stage_list)
        self.plt.semilogx(w/(2*math.pi),(-1)*mag)
        self.fig.suptitle("Stages Attenuation (Bode)")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Frequency (Hz)") #"$Frequency (Hz)$" -> con los '$' se cambia la letra a cursiva.
        self.plt.set_ylabel("Attenuation (dB)") #_{out} -> pone out en letra chica y abajo.
        self.data_plt.draw()

    def show_state_data(self): #se muestran algunos datos de interés de la etapa.
        #si no hay etapa seleccionada, WARNING.
        if(self.stlist.curselection() == ()):
            self.warning.configure(text="WARNING: No stage selected.")
            self.warning.place(x=700,y=520)
            return
        self.warning.place_forget()
        self.st_data.configure(text="Stage"+str(self.stlist.curselection()[0]+1)+" Data")
        self.data.configure(text="Q = "+str(round(self.stage_list[self.stlist.curselection()[0]].Q,3))+"\nfo = "+str(round(self.stage_list[self.stlist.curselection()[0]].fo,3)))
        self.st_data.place(x=850,y=400)
        self.data.place(x=850,y=420)

    def delete_stage(self): #borra la estapa seleccionada.
        #si no hay etapa seleccionada, WARNING.
        if(self.stlist.curselection() == ()):
            self.warning.configure(text="WARNING: No stage selected.")
            self.warning.place(x=700,y=520)
            return
        self.warning.place_forget()
        for i in range(len(self.plist_val)):
            if(round(self.plist_val[i].real,5) == round(self.stage_list[self.stlist.curselection()[0]].H.poles[0].real,5)):
                if(round(self.plist_val[i].imag,5) == round(self.stage_list[self.stlist.curselection()[0]].H.poles[0].imag,5)):
                    self.plist_val[i].sel = 0
        for i in range(len(self.zlist_val)):
            if(round(self.zlist_val[i].real,5) == round(self.stage_list[self.stlist.curselection()[0]].H.zeros[0].real,5)):
                if(round(self.zlist_val[i].imag,5) == round(self.stage_list[self.stlist.curselection()[0]].H.zeros[0].imag,5)):
                    self.zlist_val[i].sel = 0
        self.stage_list.pop(self.stlist.curselection()[0])
        self.stage_zp_str.pop(self.stlist.curselection()[0])
        self.stlist.delete(self.stlist.curselection()[0])
        self.update_zp_listboxes()
        self.update_state_listbox()
        self.update_screen()

    def __init__(self): #función de inicialización. (constructor)
        #se inicializan varibles, botones, textos, labels, etc.
        self.step = 0
        self.filter_type = "none"
        self.approx_type = "none"
        self.screen = 0

        self.window = tk.Tk()
        self.window.title("CIRCUITS THEORY")
        self.window.geometry("1200x600+50+50")
        self.window.configure(bg="gray64")

        graph = tk.Canvas(self.window)
        graph.place(x=10, y=50) #plotea el plot.

        self.fig = Figure()
        self.plt = self.fig.add_subplot(1,1,1) #los dos primeros parámetros le da una escala a la figura (mientras más grandes son los parámetros, mas chico será la figura). El tercero le da la posición en el self.window.
        self.axes = self.fig.gca()
        self.data_plt = FigureCanvasTkAgg(self.fig, master=graph)
        self.data_plt._tkcanvas.pack(padx = 2, pady = 2) #plotea el plot.

        self.approx_F = AproximadorFiltro()
        self.stage_list = [] #la lista de las etapas
        self.stage_z_str = [] #representarán los ceros que contiene cada etapa.
        self.stage_p_str = [] #representarán los polos que contiene cada etapa.
        self.stage_zp_str = [] #representarán los zeros y polos que contiene cada etapa.
        self.zlist_val = [] #representarán los zeros del filtro.
        self.plist_val = [] #representarán los polos del filtro.

        self.text1 = tk.Label(self.window, font=("arial",10,"bold"), text="Choose a Filter:",bg="gray64")
        self.text2 = tk.Label(self.window, font=("arial",10,"bold"), text="Choose an Approximation:",bg="gray64")
        self.text3 = tk.Label(self.window, font=("arial",10,"bold"), text="Set the Specifications:",bg="gray64")

        self.Ap = tk.Label(self.window, font=("arial",10), text="Ap(dB) = ",bg="gray64")
        self.fp = tk.Label(self.window, font=("arial",10), bg="gray64")
        self.As = tk.Label(self.window, font=("arial",10), text="As(dB) = ",bg="gray64")
        self.fs = tk.Label(self.window, font=("arial",10), bg="gray64")
        self.fp1 = tk.Label(self.window, font=("arial",10), text="fp+(Hz) = ",bg="gray64")
        self.fs1 = tk.Label(self.window, font=("arial",10), text="fs+(Hz) = ",bg="gray64")
        self.n = tk.Label(self.window, font=("arial",10), text="N = ",bg="gray64")
        self.nmin = tk.Label(self.window, font=("arial",10), text="Nmin = ",bg="gray64")
        self.nmax = tk.Label(self.window, font=("arial",10), text="Nmax = ",bg="gray64")
        self.qmax = tk.Label(self.window, font=("arial",10), text="Qmax = ",bg="gray64")
        self.rank = tk.Label(self.window, font=("arial",10), text="Rank(%) = ",bg="gray64")
        self.delay = tk.Label(self.window, font=("arial",10), text="Del(us) = ",bg="gray64")
        self.fgd = tk.Label(self.window, font=("arial",10), text="fgd(Hz) = ",bg="gray64")
        self.tol = tk.Label(self.window, font=("arial",10), text="Tol(%) = ",bg="gray64")
        self.Ap_val = tk.Entry(self.window, width = 10)
        self.fp_val = tk.Entry(self.window, width = 10)
        self.fp1_val = tk.Entry(self.window, width = 10)
        self.As_val = tk.Entry(self.window, width = 10)
        self.fs_val = tk.Entry(self.window, width = 10)
        self.fs1_val = tk.Entry(self.window, width = 10)
        self.n_val = tk.Entry(self.window, width = 10)
        self.nmin_val = tk.Entry(self.window, width = 10)
        self.nmax_val = tk.Entry(self.window, width = 10)
        self.qmax_val = tk.Entry(self.window, width = 10)
        self.rank_val = tk.Entry(self.window, width = 10)
        self.delay_val = tk.Entry(self.window, width = 10)
        self.fgd_val = tk.Entry(self.window, width = 10)
        self.tol_val = tk.Entry(self.window, width = 10)
        
        self.warning = tk.Label(self.window, font=("arial",10,"bold"),bg="gray64",fg="red")        
        
        self.b_attenuation = tk.Button(self.window,text="Attenuation (Bode)",command=self.plot_attenuation)
        self.b_phase = tk.Button(self.window,text="Phase (Bode)",command=self.plot_phase)
        self.b_zp = tk.Button(self.window,text="Zeros & Poles",command=self.plot_zp)
        self.b_step = tk.Button(self.window,text="Step Response",command=self.plot_step)
        self.b_impulse = tk.Button(self.window,text="Impulse Response",command=self.plot_impulse)

        self.b_LP = tk.Button(self.window,text="Low Pass",command=self.set_low_pass)
        self.b_HP = tk.Button(self.window,text="High Pass",command=self.set_high_pass)
        self.b_BP = tk.Button(self.window,text="Band Pass",command=self.set_band_pass)
        self.b_BS = tk.Button(self.window,text="Band Stop",command=self.set_band_stop)
        self.b_GD = tk.Button(self.window,text="Group Delay",command=self.set_group_delay)

        self.b_butter = tk.Button(self.window,text="Butterworth",command=self.set_butter)
        self.b_cheby_I = tk.Button(self.window,text="Chebyshev I",command=self.set_cheby_I)
        self.b_cheby_II = tk.Button(self.window,text="Chebyshev II",command=self.set_cheby_II)
        self.b_bess = tk.Button(self.window,text="Bessel",command=self.set_bess)

        self.b_graph = tk.Button(self.window,text="GRAPH!",command=self.start_graph)
        self.b_screen1 = tk.Button(self.window,text="View Filter",command=self.set_screen1)
        self.b_screen2 = tk.Button(self.window,text="View Stages",command=self.set_screen2)

        self.zp = tk.Label(self.window, font=("arial",10,"bold"), text="Zeros\t\t\t\t\tPoles",bg="gray64")
        self.zlist = tk.Listbox(self.window, selectbackground="olive drab",width = 33,height=8,exportselection=0)
        self.zscroll = tk.Scrollbar(self.window, orient="vertical",command=self.zlist.yview)
        self.zlist.configure(yscrollcommand=self.zscroll.set)
        self.plist = tk.Listbox(self.window, selectbackground="olive drab",width = 33,height=8,exportselection=0)
        self.pscroll = tk.Scrollbar(self.window, orient="vertical",command=self.plist.yview)
        self.plist.configure(yscrollcommand=self.pscroll.set)
        self.st = tk.Label(self.window, font=("arial",10,"bold"), text="Stages",bg="gray64")
        self.stlist = tk.Listbox(self.window, selectbackground="olive drab",width = 20,height=10)
        self.stscroll = tk.Scrollbar(self.window, orient="vertical",command=self.stlist.yview)
        self.stlist.configure(yscrollcommand=self.stscroll.set)

        self.b_s_stage = tk.Button(self.window,text="Set Up Stage",command=self.set_stage)
        self.b_s_stages = tk.Button(self.window,text="Automatic Set Up",command=self.set_stages)
        self.b_st_attenuation = tk.Button(self.window,text="Stage Attenuation (Bode)",command=self.plot_stage_attenuation)
        self.b_sts_attenuation = tk.Button(self.window,text="Stages Attenuation (Bode)",command=self.plot_stages_attenuation)
        self.b_data = tk.Button(self.window,text="Stage Data",command=self.show_state_data)
        self.b_delete = tk.Button(self.window,text="Delete Stage",command=self.delete_stage)

        self.st_data = tk.Label(self.window, font=("arial",10,"bold"),bg="gray64")
        self.data = tk.Label(self.window, font=("arial",10),bg="gray64")

        self.reset_button_color()
        self.update_screen()
        
        self.window.mainloop() #sigue corriendo el programa hasta que se cierra la ventana.

if __name__ == "__main__":
    ex = Gui() #aca se llama la clase y se la ejecuta.
